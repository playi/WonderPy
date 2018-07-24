import time

from WonderPy.core.wwConstants import WWRobotConstants
from wwCommandBase import WWCommandBase, do_not_call_within_connect_or_sensors


_rc  = WWRobotConstants.RobotComponent
_rcv = WWRobotConstants.RobotComponentValues
_rp  = WWRobotConstants.RobotProperties


class WWCommandAccessory(WWCommandBase):
    # These are the python API coordinate system, where positive values are head looking up / clockwise.
    SKETCH_PEN_DN_DEGREES_TLT     = 15
    SKETCH_PEN_DN_DEGREES_PAN     = 22
    SKETCH_PEN_UP_VOLTAGE_TLT     = 75
    SKETCH_PEN_UP_VOLTAGE_PAN     = 75

    def __init__(self, robot):
        super(WWCommandAccessory, self).__init__(robot)

    @do_not_call_within_connect_or_sensors
    def do_sketchkit_pen_down(self):
        self._robot.cmds.head.do_tilt_angle(self.SKETCH_PEN_DN_DEGREES_TLT)
        time.sleep(0.5)
        self._robot.cmds.head.do_pan_angle(self.SKETCH_PEN_DN_DEGREES_PAN)
        time.sleep(0.2)

    @do_not_call_within_connect_or_sensors
    def do_sketchkit_pen_up(self):
        self._robot.cmds.head.do_tilt_voltage(self.SKETCH_PEN_UP_VOLTAGE_TLT)
        time.sleep(0.5)
        self._robot.cmds.head.do_pan_voltage(self.SKETCH_PEN_UP_VOLTAGE_PAN)
        time.sleep(0.2)

    @do_not_call_within_connect_or_sensors
    def do_xylo_hit(self):
        self.stage_xylo_hit()
        time.sleep(0.2)

    def stage_xylo_hit(self):
        self._robot.stage_cmds({_rc.WW_COMMAND_MOTOR_HEAD_BANG : {}})

    @do_not_call_within_connect_or_sensors
    def do_launcher_launch(self, power):
        self.stage_launcher_launch(power)
        time.sleep(0.2)

    @do_not_call_within_connect_or_sensors
    def do_launcher_reload_left(self):
        self.stage_launcher_reload_left()
        time.sleep(0.2)

    @do_not_call_within_connect_or_sensors
    def do_launcher_reload_right(self):
        self.stage_launcher_reload_right()
        time.sleep(0.2)

    # noinspection PyDictCreation
    def stage_launcher_launch(self, power):
        """
        :param power: [0, 1]
        :return nothing
        """

        args = {}
        args[_rcv.WW_COMMAND_VALUE_SPEED] = power
        self._robot.stage_cmds({_rc.WW_COMMAND_LAUNCHER_FLING : args})

    # noinspection PyDictCreation
    def stage_launcher_reload_left(self):
        """
        :return nothing
        """

        args = {}
        args[_rcv.WW_COMMAND_VALUE_DIRECTION] = 0
        self._robot.stage_cmds({_rc.WW_COMMAND_LAUNCHER_RELOAD : args})

    # noinspection PyDictCreation
    def stage_launcher_reload_right(self):
        """
        :return nothing
        """

        args = {}
        args[_rcv.WW_COMMAND_VALUE_DIRECTION] = 1
        self._robot.stage_cmds({_rc.WW_COMMAND_LAUNCHER_RELOAD : args})
