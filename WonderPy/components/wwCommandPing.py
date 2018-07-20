from WonderPy.core.wwConstants import WWRobotConstants
from wwCommandBase import WWCommandBase

_rc  = WWRobotConstants.RobotComponent
_rcv = WWRobotConstants.RobotComponentValues


class WWCommandPing(WWCommandBase):

    def __init__(self, robot):
        super(WWCommandPing, self).__init__(robot)

    def stage_ping(self, ping_id):
        self._robot.stage_cmds(self.compose_ping(ping_id))

    def compose_ping(self, ping_id):
        ret = {
            _rc.WW_COMMAND_SET_PING : {
                _rcv.WW_COMMAND_VALUE_PING_ID : ping_id
            }
        }
        return ret
