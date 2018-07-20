from WonderPy.core.wwConstants import WWRobotConstants
from wwSensorBase import WWSensorBase

_rcv = WWRobotConstants.RobotComponentValues
_expected_json_fields = (
    _rcv.WW_SENSOR_VALUE_PING_ID,
    _rcv.WW_SENSOR_VALUE_PING_COUNT,
)


class WWSensorPing(WWSensorBase):

    def __init__(self, robot):
        super(WWSensorPing, self).__init__(robot)
        self._id    = 0
        self._count = 0

    @property
    def id(self):
        return self._id

    @property
    def count(self):
        return self._count

    def _important_field_names(self):
        return ('_id', '_count',)

    def parse(self, single_component_dictionary):
        if not self.check_fields_exist(single_component_dictionary, _expected_json_fields):
            return

        self._id    = single_component_dictionary[_rcv.WW_SENSOR_VALUE_PING_ID]
        self._count = single_component_dictionary[_rcv.WW_SENSOR_VALUE_PING_COUNT]
        self._valid = True
