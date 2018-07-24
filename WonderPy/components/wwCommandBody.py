import math
from WonderPy.core.wwConstants import WWRobotConstants
from wwCommandBase import WWCommandBase, do_not_call_within_connect_or_sensors
from WonderPy.util import wwMath

_rc  = WWRobotConstants.RobotComponent
_rcv = WWRobotConstants.RobotComponentValues
_rp  = WWRobotConstants.RobotProperties


class WWCommandBody(WWCommandBase):

    default_acceleration_linear_cm_s_s       = 50.0
    default_acceleration_angular_degrees_s_s = 900.0

    def __init__(self, robot):
        super(WWCommandBody, self).__init__(robot)

    @do_not_call_within_connect_or_sensors
    def do_forward(self, y_cm, speed_cm_s):
        """
        This is a somewhat naive drive command because it moves relative to the robot's measured position,
        which means error can accumulate.
        """
        self.do_pose(0, y_cm, 0, abs(float(y_cm)) / float(speed_cm_s),
                     WWRobotConstants.WWPoseMode.WW_POSE_MODE_RELATIVE_MEASURED)

    @do_not_call_within_connect_or_sensors
    def do_turn(self, deg, speed_deg_s):
        """
        This is a somewhat naive drive command because it moves relative to the robot's measured position,
        which means error can accumulate.
        """

        self.do_pose(0, 0, deg, abs(float(deg)) / float(speed_deg_s), True,
                     WWRobotConstants.WWPoseMode.WW_POSE_MODE_RELATIVE_MEASURED,
                     WWRobotConstants.WWPoseDirection.WW_POSE_DIRECTION_INFERRED,
                     False)

    @do_not_call_within_connect_or_sensors
    def do_pose(self, x_cm, y_cm, degrees, time, mode=WWRobotConstants.WWPoseMode.WW_POSE_MODE_RELATIVE_MEASURED, ease=True,
                direction=WWRobotConstants.WWPoseDirection.WW_POSE_DIRECTION_INFERRED,
                wrap_theta=True):
        self.stage_pose(x_cm, y_cm, degrees, time, mode, ease, direction, wrap_theta)
        self._robot.sensors.pose.block_until_idle(time + 10.0)

    def stage_pose(self, x_cm, y_cm, degrees, time, mode=WWRobotConstants.WWPoseMode.WW_POSE_MODE_RELATIVE_MEASURED, ease=True,
                   direction=WWRobotConstants.WWPoseDirection.WW_POSE_DIRECTION_INFERRED,
                   wrap_theta=True):
        cmds = self.compose_pose(x_cm, y_cm, degrees, time, mode, ease, direction, wrap_theta)
        # print("sending pose: %s" % str(cmds))
        self._robot.stage_cmds(cmds)

    # noinspection PyDictCreation
    def compose_pose(self, x_cm, y_cm, degrees, time, mode, ease, direction, wrap_theta):
        x_cm, y_cm = wwMath.coords_api_to_json_pos(x_cm, y_cm)
        degrees    = wwMath.coords_api_to_json_pan(degrees)

        args = {}
        args[_rcv.WW_COMMAND_VALUE_AXIS_X         ] = x_cm
        args[_rcv.WW_COMMAND_VALUE_AXIS_Y         ] = y_cm
        args[_rcv.WW_COMMAND_VALUE_ANGLE_DEGREE   ] = degrees
        args[_rcv.WW_COMMAND_VALUE_TIME           ] = time
        args[_rcv.WW_COMMAND_VALUE_POSE_EASE      ] = ease
        args[_rcv.WW_COMMAND_VALUE_POSE_MODE      ] = mode
        args[_rcv.WW_COMMAND_VALUE_POSE_WRAP_THETA] = wrap_theta
        args[_rcv.WW_COMMAND_VALUE_POSE_DIRECTION ] = direction
        return {_rc.WW_COMMAND_BODY_POSE : args}

    @staticmethod
    def convert_wheel_speeds_to_linear_angular_degrees(speed_left, speed_right, wheelbase):
        linear  = (speed_right + speed_left) / 2.0
        angular = (speed_right - speed_left) / wheelbase * math.degrees(1.0)
        return linear, angular

    def stage_stop(self, linear_acc_cm_s_s=None, angular_acc_deg_s_s=None):
        self.stage_linear_angular(0, 0, linear_acc_cm_s_s, angular_acc_deg_s_s)

    def stage_wheel_speeds(self, left_cm_s, right_cm_s):
        # we convert the wheel speeds into linear / angular form.
        # this is important because it is signficantly more accurate for all driving tasks.
        # for non-driving tasks, such as using the wheels as motors to control some device, use wheel_speeds_naive().
        linear, angular = WWCommandBody.convert_wheel_speeds_to_linear_angular_degrees(left_cm_s, right_cm_s,
                                                                                       self._robot.wheelbase_cm)
        self.stage_linear_angular(linear, angular)

    def stage_wheel_speeds_naive(self, left_cm_s, right_cm_s):
        self._robot.stage_cmds(self.compose_wheel_speeds_naive(left_cm_s, right_cm_s))

    # noinspection PyDictCreation
    def compose_wheel_speeds_naive(self, left_cm_s, right_cm_s):
        args = {}
        args[_rcv.WW_COMMAND_VALUE_LEFT_SPEED ] = left_cm_s
        args[_rcv.WW_COMMAND_VALUE_RIGHT_SPEED] = right_cm_s
        return {_rc.WW_COMMAND_BODY_WHEELS : args}

    def stage_linear_angular(self, linear_vel_cm_s, angular_vel_degrees_s,
                             linear_acc_cm_s_s=None, angular_acc_degrees_s_s=None):
        self._robot.stage_cmds(self.compose_linear_angular(linear_vel_cm_s, angular_vel_degrees_s,
                               linear_acc_cm_s_s, angular_acc_degrees_s_s))

    # noinspection PyDictCreation
    def compose_linear_angular(self, linear_vel_cm_s, angular_vel_degrees_s, lin_acc_cm_s_s=None,
                               ang_acc_degrees_s_s=None):
        lin_acc_cm_s_s      = WWCommandBody.default_acceleration_linear_cm_s_s       \
            if lin_acc_cm_s_s is None else lin_acc_cm_s_s
        ang_acc_degrees_s_s = WWCommandBody.default_acceleration_angular_degrees_s_s \
            if ang_acc_degrees_s_s is None else ang_acc_degrees_s_s

        args = {}
        args[_rcv.WW_COMMAND_VALUE_LINEAR_VELOCITY_CM_S        ] =                               linear_vel_cm_s
        args[_rcv.WW_COMMAND_VALUE_ANGULAR_VELOCITY_DEG_S      ] = wwMath.coords_api_to_json_pan(angular_vel_degrees_s)
        args[_rcv.WW_COMMAND_VALUE_LINEAR_ACCELERATION_CM_S_S  ] =                               lin_acc_cm_s_s
        args[_rcv.WW_COMMAND_VALUE_ANGULAR_ACCELERATION_DEG_S_S] = wwMath.coords_api_to_json_pan(ang_acc_degrees_s_s)
        return {_rc.WW_COMMAND_BODY_LINEAR_ANGULAR : args}
