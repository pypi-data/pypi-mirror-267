import sys
from datetime import datetime

import gevent
from importlib import import_module, reload

from ats_base.common import func
from ats_base.common.enum import Payload
from ats_base.log.logger import logger
from ats_base.service import msg

from ats_case.case import asb, base, translator, command
from ats_case.case.context import Context
from ats_case.common.enum import *
from ats_case.common.error import *


def execute(context: Context):
    if context.mode == WorkMode.FORMAL:
        FormalExecutor(context).exec()
    else:
        DebugExecutor(context).exec()


class Executor(object):
    def __init__(self, context: Context):
        self._context = context
        self._model = None
        self._steps = []

    def exec(self):
        self.handle()

        index = self._load()  # 加载在断点续测时所需关键变量
        while index < len(self._steps):
            self._context.runtime.step = self._steps[index]
            if self.if_meet():
                if self.loop_meet():
                    self.loop_exec()
                else:
                    self.step_exec()

            # step_jump只有执行到跳步的步骤, 才会赋为True
            if self._context.runtime.step_jump:
                index = self._steps.index(self._context.runtime.step)
                self._context.runtime.step_jump = False
            else:
                index = self._steps.index(self._context.runtime.step) + 1

    def handle(self):
        pass

    def _load(self):
        if self._context.renew == 1:
            self._context.runtime.loop_index = asb.BreakPoint.get(self._context, 'loop_index')
            if self._context.runtime.loop_index == 'NULL':
                self._context.runtime.loop_index = 0

            self._context.runtime.loop_sn = asb.BreakPoint.get(self._context, 'loop_sn')
            if self._context.runtime.loop_sn == 'NULL':
                self._context.runtime.loop_sn = 0

            try:
                return self._steps.index(asb.BreakPoint.get(self._context, 'step'))
            except:
                pass

        return 0

    def _flush(self):
        asb.BreakPoint.set(self._context, 'step', self._context.runtime.step)
        asb.BreakPoint.set(self._context, 'loop_sn', self._context.runtime.loop_sn)
        asb.BreakPoint.set(self._context, 'loop_index', self._context.runtime.loop_index)

    def _err_msg_notify(self, err: str):
        """
        异常消息通知
        :param err:
        :return:
        """
        msg.send('dingding', func.to_dict(payload=Payload.ERROR.value, workmode=self._context.mode.value,
                                          project=self._context.project, case_name=self._context.case.name,
                                          meter_pos=self._context.meter.pos, step=self._context.runtime.step,
                                          test_sn=self._context.test_sn,
                                          start_time=self._context.start_time.strftime('%Y.%m.%d %H:%M:%S'),
                                          end_time=datetime.now().strftime('%Y.%m.%d %H:%M:%S'),
                                          msg=err))

    def is_exec(self):
        if base.offbench(self._context, self._context.offbench):
            return False

        return True

    def step_exec(self):
        if self._context.mode == WorkMode.FORMAL:  # 项目测试 - 协程切换
            gevent.sleep(0.05)

        logger.info('~ @TCC-STEP-> steps[#{}] execute'.format(self._context.runtime.step))

        self._flush()  # 缓存在断点续测时所需关键变量
        if self.is_exec():
            try:
                getattr(self._model, 'step_{}'.format(self._context.runtime.step))(self._context)
            except APIError as ae:
                logger.info(str(ae))
                self._err_msg_notify(str(ae))

                raise AssertionError(str(ae))
            except Exception as e:
                self._context.runtime.sas[self._context.runtime.step] = '{} - {} '.format(base.CODE_ERROR, str(e))
                if isinstance(e, BenchReadNoneError):
                    asb.Application.set(self._context.test_sn, "meter:quantity",
                                        int(asb.Application.get(self._context.test_sn, "meter:quantity")) - 1)
                command.client().message(str(e)).error(self._context)
                logger.error(str(e))
                self._err_msg_notify(str(e))

                raise AssertionError(str(e))

    def if_meet(self):
        ifs = self._context.case.control.get('ifs')
        if isinstance(ifs, dict):
            try:
                ifs.pop('offbench')
            except:
                pass

            if len(ifs) > 0:
                for ranges, condition in ifs.items():
                    step_start = int(ranges.split(':')[0])
                    step_end = int(ranges.split(':')[1])

                    if step_start <= self._context.runtime.step <= step_end:
                        try:
                            ci = int(condition)
                        except:
                            ci = int(self._context.runtime.glo.get(condition, 1))

                        if ci == 0:  # 条件判断False
                            self._context.runtime.step = step_end
                            for i in range(step_start, step_end + 1):
                                self._context.runtime.sos.update({i: func.to_dict(result=None)})
                            return False

        return True

    def loop_meet(self):
        loops = self._context.case.control.get('loops')

        if loops is None or type(loops) is not list or len(loops) <= 0:
            return False

        if self._context.runtime.loop_sn >= len(loops):
            return False
        loop = loops[self._context.runtime.loop_sn]
        ranges = loop.get('range')
        count = loop.get('count')

        step_start = int(ranges.split(':')[0])
        step_end = int(ranges.split(':')[1])

        if step_start <= self._context.runtime.step <= step_end:
            self._context.runtime.loop_start_step = step_start
            self._context.runtime.loop_end_step = step_end
            if self._context.runtime.loop_count <= 0:
                self._context.runtime.loop_count = int(count)
            return True

        return False

    def loop_exec(self):
        logger.info('~ @TCC-LOOP-> loops[#{}] start. -range {}:{}  -count {}'.format(
            self._context.runtime.loop_sn, self._context.runtime.loop_start_step,
            self._context.runtime.loop_end_step, self._context.runtime.loop_count))

        command.client().message('[#{}]循环开始 - 步骤范围[{}-{}], 共{}次'.format(
            self._context.runtime.loop_sn, self._context.runtime.loop_start_step,
            self._context.runtime.loop_end_step, self._context.runtime.loop_count)).show(self._context)

        while self._context.runtime.loop_index < self._context.runtime.loop_count:
            logger.info('~ @TCC-LOOP-> loops[#{}], -count {}, -index {}'.format(
                self._context.runtime.loop_sn, self._context.runtime.loop_count,
                self._context.runtime.loop_index + 1))
            command.client().message('[#{}]循环 - 共{}次, 当前执行第{}次'.format(
                self._context.runtime.loop_sn, self._context.runtime.loop_count,
                self._context.runtime.loop_index + 1)).show(self._context)

            s = self._context.runtime.loop_start_step
            while s <= self._context.runtime.loop_end_step:
                index = -1
                try:
                    index = self._steps.index(s)
                    self._context.runtime.step = s
                except ValueError as e:
                    pass

                if index >= 0:
                    if self.if_meet():
                        self.step_exec()
                    else:
                        s = self._context.runtime.step

                s += 1

            self._context.runtime.loop_index += 1

        self._context.runtime.loop_start_step = 0
        self._context.runtime.loop_end_step = 0
        self._context.runtime.loop_count = 0
        self._context.runtime.loop_index = 0

        command.client().message("[#{}]循环结束...".format(self._context.runtime.loop_sn)).show(self._context)
        logger.info('~ @TCC-LOOP-> loops[#{}] end.'.format(self._context.runtime.loop_sn))

        self._context.runtime.loop_sn += 1


def extract_steps(content: list):
    n_s = []
    for s in content:
        if s.upper().find('STEP_') >= 0:
            num = func.extract_digit(s)
            n_s.append(int(num))

    return sorted(n_s)


def import_script(clazz: ScriptClazz, context: Context, manual_dir: str = 'debug'):
    # 分为两种情况: 0. 手动编写脚本 1.自动编写脚本
    if clazz == ScriptClazz.AUTO:
        steps = translator.translate(context)
        a_name = 'script.auto.{}.tsm_{}'.format(context.tester.username.lower(), context.meter.pos)
        try:
            model = sys.modules[a_name]
            model = reload(model)
        except:
            model = import_module(a_name)

    else:
        m_name = 'script.manual.{}.{}'.format(manual_dir, context.case.steps)
        try:
            model = sys.modules[m_name]
            model = reload(model)
        except:
            model = import_module(m_name)

        steps = extract_steps(dir(model))

    return model, steps


class FormalExecutor(Executor):
    def handle(self):
        self._model, self._steps = import_script(self._context.case.script, self._context, 'formal')


class DebugExecutor(Executor):
    def handle(self):
        self._model, self._steps = import_script(self._context.case.script, self._context)
