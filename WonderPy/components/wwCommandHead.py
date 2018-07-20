from WonderPy.core.wwConstants import WWRobotConstants
from wwCommandBase import WWCommandBase, do_not_call_within_connect_or_sensors
from WonderPy.util import wwMath

_rc  = WWRobotConstants.RobotComponent
_rcv = WWRobotConstants.RobotComponentValues
_rp  = WWRobotConstants.RobotProperties


class WWCommandHead(WWCommandBase):

    _TIME_ANGLE   = 0.2
    _TIME_VOLTAGE = 0.6

    def __init__(self, robot):
        super(WWCommandHead, self).__init__(robot)

    def stage_pan_angle(self, pan_degrees):
        self._robot.stage_cmds(self.compose_angle(_rc.WW_COMMAND_HEAD_POSITION_PAN ,
                                                  wwMath.coords_api_to_json_pan(pan_degrees)))

    def stage_tilt_angle(self, tilt_degrees):
        self._robot.stage_cmds(self.compose_angle(_rc.WW_COMMAND_HEAD_POSITION_TILT,
                                                  wwMath.coords_api_to_json_tilt(tilt_degrees)))

    def stage_pan_tilt_angle(self, pan_degrees, tilt_degrees):
        self.stage_pan_angle(pan_degrees)
        self.stage_tilt_angle(tilt_degrees)

    def stage_pan_voltage(self, pan_voltage_percent):
        self._robot.stage_cmds(self.compose_voltage(_rc.WW_COMMAND_HEAD_PAN_VOLTAGE ,
                                                    wwMath.coords_api_to_json_pan(pan_voltage_percent)))

    def stage_tilt_voltage(self, tilt_voltage_percent):
        self._robot.stage_cmds(self.compose_voltage(_rc.WW_COMMAND_HEAD_TILT_VOLTAGE ,
                                                    wwMath.coords_api_to_json_tilt(tilt_voltage_percent)))

    def stage_pan_tilt_voltage(self, pan_voltage_percent, tilt_voltage_percent):
        self.stage_pan_voltage(pan_voltage_percent)
        self.stage_tilt_voltage(tilt_voltage_percent)

    @do_not_call_within_connect_or_sensors
    def do_pan_angle(self, pan_degrees, timeout=None):
        self.stage_pan_angle(pan_degrees)
        self._block_for_simple_timeout(self._TIME_ANGLE, timeout)

    @do_not_call_within_connect_or_sensors
    def do_tilt_angle(self, tilt_degrees, timeout=None):
        self.stage_tilt_angle(tilt_degrees)
        self._block_for_simple_timeout(self._TIME_ANGLE, timeout)

    @do_not_call_within_connect_or_sensors
    def do_pan_tilt_angle(self, pan_degrees, tilt_degrees, timeout=None):
        self.stage_pan_tilt_angle(pan_degrees, tilt_degrees)
        self._block_for_simple_timeout(0.2, timeout)

    @do_not_call_within_connect_or_sensors
    def do_pan_voltage(self, pan_voltage_percent, timeout=None):
        self.stage_pan_voltage(pan_voltage_percent)
        self._block_for_simple_timeout(self._TIME_VOLTAGE, timeout)

    @do_not_call_within_connect_or_sensors
    def do_tilt_voltage(self, tilt_voltage_percent, timeout=None):
        self.stage_tilt_voltage(tilt_voltage_percent)
        self._block_for_simple_timeout(self._TIME_VOLTAGE, timeout)

    @do_not_call_within_connect_or_sensors
    def do_pan_tilt_voltage(self, pan_voltage_percent, tilt_voltage_percent, timeout=None):
        self.stage_pan_tilt_voltage(pan_voltage_percent, tilt_voltage_percent)
        self._block_for_simple_timeout(self._TIME_VOLTAGE, timeout)

    def compose_angle(self, component_id, degrees):
        args = {}
        args[_rcv.WW_COMMAND_VALUE_ANGLE_DEGREE] = degrees
        return {component_id : args}

    def compose_voltage(self, component_id, voltage_percent):
        args = {}
        args[_rcv.WW_COMMAND_VALUE_PERCENTAGE] = voltage_percent
        return {component_id : args}
