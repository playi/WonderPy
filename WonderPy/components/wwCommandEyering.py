from wwCommandBase import WWCommandBase
from WonderPy.core.wwConstants import WWRobotConstants

_ea  = WWRobotConstants.WWEyeAnimation
_rc  = WWRobotConstants.RobotComponent
_rcv = WWRobotConstants.RobotComponentValues
_rp  = WWRobotConstants.RobotProperties


class WWCommandEyering(WWCommandBase):

    def __init__(self, robot):
        super(WWCommandEyering, self).__init__(robot)

    def stage_eyering(self, pattern, brightness):
        s = self.compose_eyering(pattern, brightness)
        self._robot.stage_cmds(s)

    def compose_eyering(self, pattern, brightness):
        """
        :param pattern can be one of WWEyeAnimation or a list of 12 booleans:
        :param brightness the overall brightness of all the LEDs. [0, 1]:
        :return: None
        """
        anim  = _ea.WW_EYEANIM_BITMAP

        args = {}

        if pattern in (_ea.WW_EYEANIM_FULL_BLINK, _ea.WW_EYEANIM_SWIRL, _ea.WW_EYEANIM_WINK):
            anim = pattern
        else:
            args[_rcv.WW_COMMAND_VALUE_ORDER_INDEX     ] = pattern

        args[_rcv.WW_COMMAND_VALUE_EYE_RING_ANIMATION] = anim
        args[_rcv.WW_COMMAND_VALUE_COLOR_BRIGHTNESS  ] = brightness

        return {_rc.WW_COMMAND_EYE_RING : args}
