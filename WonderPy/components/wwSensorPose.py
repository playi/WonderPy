from datetime import datetime, timedelta
import time
from WonderPy.core.wwConstants import WWRobotConstants
from wwSensorBase import WWSensorBase
from WonderPy.util import wwMath

_rc  = WWRobotConstants.RobotComponent
_rcv = WWRobotConstants.RobotComponentValues
_expected_json_fields = (
    _rcv.WW_SENSOR_VALUE_AXIS_X,
    _rcv.WW_SENSOR_VALUE_AXIS_Y,
    _rcv.WW_SENSOR_VALUE_ANGLE_DEGREE,
)

_non_pose_commands = {
    _rc.WW_COMMAND_BODY_WHEELS,
    _rc.WW_COMMAND_BODY_LINEAR_ANGULAR,
    _rc.WW_COMMAND_BODY_COAST,
    _rc.WW_COMMAND_POWER,
}

_watermark_all_done = 255


_t0 = time.time()


class WWSensorPose(WWSensorBase):

    def __init__(self, robot):
        super(WWSensorPose, self).__init__(robot)
        self._x                  = 0
        self._y                  = 0
        self._degrees            = 0
        self._watermark_measured = None
        self._watermark_inferred = 0

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def degrees(self):
        return self._degrees

    @property
    def watermark_measured(self):
        return self._watermark_measured

    @property
    def watermark_inferred(self):
        return self._watermark_inferred

    def _important_field_names(self):
        return '_x', '_y', '_degrees', '_watermark_measured', '_watermark_inferred'

    def parse(self, single_component_dictionary):

        if not self.check_fields_exist(single_component_dictionary, _expected_json_fields):
            return

        x       = single_component_dictionary[_rcv.WW_SENSOR_VALUE_AXIS_X      ]
        y       = single_component_dictionary[_rcv.WW_SENSOR_VALUE_AXIS_Y      ]
        degrees = single_component_dictionary[_rcv.WW_SENSOR_VALUE_ANGLE_DEGREE]

        x, y    = wwMath.coords_json_to_api_pos(x, y)
        degrees = wwMath.coords_api_to_json_pan(degrees)

        self._x       = x
        self._y       = y
        self._degrees = degrees

        if _rcv.WW_SENSOR_VALUE_POSE_WATERMARK in single_component_dictionary:
            self._watermark_measured = single_component_dictionary[_rcv.WW_SENSOR_VALUE_POSE_WATERMARK]
            self._watermark_inferred = self._watermark_measured

        self._valid   = True

    def handle_staged_motion_commands(self, command_dictionary):
        if any(k in command_dictionary for k in _non_pose_commands):
            self._did_stage_non_pose_drive_command()

        if _rc.WW_COMMAND_BODY_POSE in command_dictionary:
            pose_cmd = command_dictionary[_rc.WW_COMMAND_BODY_POSE]
            self._did_stage_pose_command(pose_cmd[_rcv.WW_COMMAND_VALUE_POSE_MODE])

    def _did_stage_pose_command(self, mode):
        if mode == WWRobotConstants.WWPoseMode.WW_POSE_MODE_SET_GLOBAL:
            self._watermark_inferred = 0
        else:
            if self._watermark_inferred == 255:
                self._watermark_inferred = 1
            else:
                self._watermark_inferred += 1

    def _did_stage_non_pose_drive_command(self):
        self._watermark_inferred = 0

    def block_until_idle(self, timeout=10):
        timeout_moment = datetime.now() + timedelta(seconds=timeout)
        while (self.watermark_inferred != 255) and (datetime.now() < timeout_moment):
            self._robot.block_until_sensors()
