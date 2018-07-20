import math
from WonderPy.core.wwConstants import WWRobotConstants
from wwSensorBase import WWSensorBase
from WonderPy.util import wwMath

_rcv = WWRobotConstants.RobotComponentValues
_expected_json_fields = (
    _rcv.WW_SENSOR_VALUE_AXIS_YAW,
    _rcv.WW_SENSOR_VALUE_AXIS_PITCH,
    _rcv.WW_SENSOR_VALUE_AXIS_ROLL,
)


class WWSensorGyroscope(WWSensorBase):
    """
    Measures rotational velocity around the 3 primary axes.
    Note that the update frequency of this sensor is not high enough for accurate dead-reckoning.
    If you would like to track the robot's current orientation (around the Z (up) axis),
    the "Pose" sensor includes that value as reckoned by the robot at much higher frequencies.
    """

    def __init__(self, robot):
        super(WWSensorGyroscope, self).__init__(robot)
        self._x = 0
        self._y = 0
        self._z = 0

    def _important_field_names(self):
        return ('x', 'y', 'z')

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

        x = single_component_dictionary[_rcv.WW_SENSOR_VALUE_AXIS_ROLL ]
        y = single_component_dictionary[_rcv.WW_SENSOR_VALUE_AXIS_PITCH]
        z = single_component_dictionary[_rcv.WW_SENSOR_VALUE_AXIS_YAW  ]

        x, y = wwMath.coords_json_to_api_pos(x, y)

        self._x = math.degrees(x)
        self._y = math.degrees(y)
        self._z = math.degrees(z)

        self._valid   = True
