from WonderPy.core.wwConstants import WWRobotConstants
from wwCommandBase import WWCommandBase

_rc  = WWRobotConstants.RobotComponent
_rcv = WWRobotConstants.RobotComponentValues


class WWCommandMonoLED(WWCommandBase):

    def __init__(self, robot):
        super(WWCommandMonoLED, self).__init__(robot)

    def stage_button_main(self, brightness):
        self._robot.stage_cmds(self.compose_button_main(brightness))

    def compose_button_main(self, brightness):
        return {_rc.WW_COMMAND_LIGHT_MONO_BUTTON_MAIN: self._compose_val_brightness(brightness)}

    def _compose_val_brightness(self, brightness):
        return {
            _rcv.WW_COMMAND_VALUE_COLOR_BRIGHTNESS: brightness,
        }
