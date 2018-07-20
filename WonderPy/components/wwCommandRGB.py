from wwCommandBase import WWCommandBase
from WonderPy.core.wwConstants import WWRobotConstants

_rc  = WWRobotConstants.RobotComponent
_rcv = WWRobotConstants.RobotComponentValues


class WWCommandRGB(WWCommandBase):

    def __init__(self, robot):
        super(WWCommandRGB, self).__init__(robot)

    def stage_all(self, r, g, b):
        self.stage_front    (r, g, b)
        self.stage_ear_left (r, g, b)
        self.stage_ear_right(r, g, b)
        if self.robot.robot_type in {WWRobotConstants.RobotType.WW_ROBOT_CUE}:
            self.stage_top    (r, g, b)

    def stage_ears_front(self, r, g, b):
        self.stage_front    (r, g, b)
        self.stage_ear_left (r, g, b)
        self.stage_ear_right(r, g, b)

    def stage_ear_left(self, r, g, b):
        self._robot.stage_cmds(self.compose_ear_left     (r, g, b))

    def stage_ear_right(self, r, g, b):
        self._robot.stage_cmds(self.compose_led_ear_right(r, g, b))

    def stage_front(self, r, g, b):
        self._robot.stage_cmds(self.compose_led_front    (r, g, b))

    def stage_top(self, r, g, b):
        self._robot.stage_cmds(self.compose_led_top      (r, g, b))

    def compose_ear_left(self, r, g, b):
        return {_rc.WW_COMMAND_LIGHT_RGB_LEFT_EAR    : self._compose_val_rgb(r, g, b)}

    def compose_led_ear_right(self, r, g, b):
        return {_rc.WW_COMMAND_LIGHT_RGB_RIGHT_EAR   : self._compose_val_rgb(r, g, b)}

    def compose_led_front(self, r, g, b):
        return {_rc.WW_COMMAND_LIGHT_RGB_CHEST       : self._compose_val_rgb(r, g, b)}

    def compose_led_top(self, r, g, b):
        return {_rc.WW_COMMAND_LIGHT_RGB_BUTTON_MAIN : self._compose_val_rgb(r, g, b)}

    def _compose_val_rgb(self, r, g, b):
        return {
            _rcv.WW_COMMAND_VALUE_COLOR_RED  : r,
            _rcv.WW_COMMAND_VALUE_COLOR_GREEN: g,
            _rcv.WW_COMMAND_VALUE_COLOR_BLUE : b,
        }
