from datetime import datetime, timedelta

from WonderPy.core.wwConstants import WWRobotConstants
from wwCommandBase import WWCommandBase, do_not_call_within_connect_or_sensors

_rc  = WWRobotConstants.RobotComponent
_rcv = WWRobotConstants.RobotComponentValues


class WWCommandMedia(WWCommandBase):

    def __init__(self, robot):
        super(WWCommandMedia, self).__init__(robot)

    @do_not_call_within_connect_or_sensors
    def do_audio(self, filename, volume=1.0, timeout=None):
        """blocks via time.sleep() until sound is completed, or timeout is met"""

        self.stage_audio(filename, volume)
        if timeout == 0:
            return

        timeout_moment = None
        if timeout:
            timeout_moment = datetime.now() + timedelta(seconds=timeout)

        # wait 3 sensor packets
        for _ in range(3):
            self._robot.block_until_sensors()

        # wait for sound playing to go high
        while not self._robot.sensors.speaker.playing:
            self._robot.block_until_sensors()
            if timeout_moment and (datetime.now() < timeout_moment):
                return

        # wait for sound playing to go low
        while self._robot.sensors.speaker.playing:
            self._robot.block_until_sensors()
            if timeout_moment and (datetime.now() < timeout_moment):
                return

    def stage_audio(self, filename, volume=1.0):
        self._robot.stage_cmds(self.compose_audio(filename, volume))

    def compose_audio(self, filename, volume=1.0):
        # todo validate this filename against the robot type

        ret = {
            _rc.WW_COMMAND_SPEAKER : {
                _rcv.WW_COMMAND_VALUE_FILE         : filename,
                _rcv.WW_COMMAND_VALUE_SOUND_VOLUME : volume,
            }
        }

        return ret
