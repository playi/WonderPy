from WonderPy.core.wwConstants import WWRobotConstants
from wwSensorBase import WWSensorBase

_rcv = WWRobotConstants.RobotComponentValues
_expected_json_fields = (
    _rcv.WW_SENSOR_VALUE_ANGLE_DEGREE,
)


class WWSensorAngle(WWSensorBase):

    def __init__(self, robot, fn_unit_converter):
        super(WWSensorAngle, self).__init__(robot)
        self._degrees          = None
        self._fn_unit_converter = fn_unit_converter

    @property
    def degrees(self):
        return self._degrees

    def _important_field_names(self):
        return ('_degrees',)

    def parse(self, single_component_dictionary):
        if not self.check_fields_exist(single_component_dictionary, _expected_json_fields):
            return

        self._degrees = self._fn_unit_converter(float(single_component_dictionary[_rcv.WW_SENSOR_VALUE_ANGLE_DEGREE]))
        self._valid   = True
