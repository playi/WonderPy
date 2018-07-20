from WonderPy.core.wwConstants import WWRobotConstants
from wwSensorBase import WWSensorBase
from WonderPy.util import wwMath


_rcv = WWRobotConstants.RobotComponentValues
_expected_json_fields = (
    _rcv.WW_SENSOR_VALUE_AXIS_X,
    _rcv.WW_SENSOR_VALUE_AXIS_Y,
    _rcv.WW_SENSOR_VALUE_AXIS_Z,
)


class WWSensorBaseXYZ(WWSensorBase):

    def __init__(self, robot):
        super(WWSensorBaseXYZ, self).__init__(robot)
        self._x = 0
        self._y = 0
        self._z = 0

    def _important_field_names(self):
        return 'x', 'y', 'z'

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def parse(self, single_component_dictionary):
        if not self.check_fields_exist(single_component_dictionary, _expected_json_fields):
            return

        x = single_component_dictionary[_rcv.WW_SENSOR_VALUE_AXIS_X]
        y = single_component_dictionary[_rcv.WW_SENSOR_VALUE_AXIS_Y]
        z = single_component_dictionary[_rcv.WW_SENSOR_VALUE_AXIS_Z]

        x, y = wwMath.coords_json_to_api_pos(x, y)

        self._x = x
        self._y = y
        self._z = z

        self._valid   = True
