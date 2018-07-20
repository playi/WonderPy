from WonderPy.core.wwConstants import WWRobotConstants
from wwSensorBase import WWSensorBase

_rcv = WWRobotConstants.RobotComponentValues
_expected_json_fields = (
    _rcv.WW_SENSOR_VALUE_FLAG,
)


class WWSensorMedia(WWSensorBase):

    def __init__(self, robot):
        super(WWSensorMedia, self).__init__(robot)
        self._playing = False

    @property
    def playing(self):
        return self._playing

    def _important_field_names(self):
        return ('_playing',)

    def parse(self, single_component_dictionary):
        if not self.check_fields_exist(single_component_dictionary, _expected_json_fields):
            return

        # "not not" converts truthy things into True or False.  eg 0 and 1 etc.
        self._playing = not not single_component_dictionary[_rcv.WW_SENSOR_VALUE_FLAG]

        self._valid   = True
