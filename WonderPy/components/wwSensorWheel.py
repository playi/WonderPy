from WonderPy.core.wwConstants import WWRobotConstants
from wwSensorBase import WWSensorBase

_rcv = WWRobotConstants.RobotComponentValues
_expected_json_fields = (
    _rcv.WW_SENSOR_VALUE_DISTANCE,
)


class WWSensorWheel(WWSensorBase):

    def __init__(self, robot):
        super(WWSensorWheel, self).__init__(robot)
        self._distance_raw       = None
        self._distance_reference = None

    @property
    def distance(self):
        return self._distance_raw - self._distance_reference

    def _important_field_names(self):
        return 'distance',

    def parse(self, single_component_dictionary):

        if not self.check_fields_exist(single_component_dictionary, _expected_json_fields):
            return

        # todo: handle wrap at about +/-9000cm.
        self._distance_raw = single_component_dictionary[_rcv.WW_SENSOR_VALUE_DISTANCE]

        if self._distance_reference is None:
            self.tare()

        self._valid = True

    def tare(self):
        """
        Reset the reference distance
        """
        self._distance_reference = self._distance_raw
