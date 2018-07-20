import math
from WonderPy.core.wwConstants import WWRobotConstants
from wwSensorBase import WWSensorBase
from WonderPy.util import wwMath

_rcv = WWRobotConstants.RobotComponentValues
_expected_json_fields = (
    _rcv.WW_SENSOR_VALUE_AXIS_X,
    _rcv.WW_SENSOR_VALUE_AXIS_Y,
    _rcv.WW_SENSOR_VALUE_AXIS_Z,
)


class WWSensorAccelerometer(WWSensorBase):
    """
    Measures linear acceleration along the 3 primary axes. Units are in gravities (9.8m/s/s).
    A robot sitting flat and at rest will have an acceleration of positive 1 on the Z axis.
    A robot being pushed suddenly forward will register a positive acceleration on the Y axis.
    (followed by a negative acceleration when it stops accelerating)

    This sensor can be fairly noisy, and naturally includes the 'acceleration' due to gravity.
    Extensions to this might include low-pass filtering to smooth the data,
    and possibly subtracting out the low-pass value to subtract out gravity.
    """

    def __init__(self, robot):
        super(WWSensorAccelerometer, self).__init__(robot)
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

    @staticmethod
    def one_gravity_cm_s_s():
        return 980.665

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

        self._valid = True

    def degrees_z_yz(self):
        """
        degrees away from z axis in the yz plane. note undefined if yz is horizontal
        """
        return math.atan2(self.y, self.z) * math.degrees(1)

    def degrees_y_yz(self):
        """
        degrees away from y axis in the yz plane. note undefined if yz is horizontal
        """
        return math.atan2(self.z, self.y) * math.degrees(1)

    def degrees_z_xz(self):
        """
        degrees away from z axis in the xz plane. note undefined if xz is horizontal
        """
        return math.atan2(self.x, self.z) * math.degrees(1)

    def degrees_x_xz(self):
        """
        degrees away from x axis in the xz plane. note undefined if xz is horizontal
        """
        return math.atan2(self.z, self.x) * math.degrees(1)

    def degrees_y_xy(self):
        """
        degrees away from y axis in the xy plane. note undefined if xy is horizontal
        """
        return math.atan2(self.x, self.y) * math.degrees(1)

    def degrees_x_xy(self):
        """
        degrees away from y axis in the xy plane. note undefined if xy is horizontal
        """
        return math.atan2(self.y, self.x) * math.degrees(1)
