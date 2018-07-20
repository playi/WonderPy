from WonderPy.core.wwConstants import WWRobotConstants
from wwSensorBase import WWSensorBase

_rcv = WWRobotConstants.RobotComponentValues
_expected_json_fields = (
    _rcv.WW_SENSOR_VALUE_REFLECTANCE,
    _rcv.WW_SENSOR_VALUE_DISTANCE,
)


class WWSensorDistance(WWSensorBase):
    """
    Mechanism:
    Each distance sensor is an infrared-emitting LED paired with an infrared-detector.
    The LED shines light out into the world, and then the detector measures how much bounces back.
    This is a very approximate measure of distance, and should not be considered precise.
    The HAL layer converts the measured reflectance into approximate distance via a table of values
    determined in laboratory conditions.
    Outside of laboratory conditions, the reflectance->distance conversion may be skewed by several factors:
        * strong ambient light, such as direct sunlight
        * the specularity of the reflecting surface: a very shiny surface such as a mirror
            will reflect more or less than a diffuse surface such as paper, depending on the surface's orientation.
        * the color of the surface: black will reflect less than white.

    Geometry:
    In Dash and Cue, the two sensors in the front are each angled in towards each other a bit.
    So the distance sensor which is on the left side of the robot actually faces to the right.
    For this reason we refer to them as "right-facing" or "left-facing" rather than "left" or "right".
    """

    def __init__(self, robot):
        super(WWSensorDistance, self).__init__(robot)
        self._distance_approximate = None
        self._reflectance          = None

    @property
    def distance_approximate(self):
        return self._distance_approximate

    @property
    def reflectance(self):
        return self._reflectance

    def _important_field_names(self):
        return ('_distance_approximate', '_reflectance')

    def parse(self, single_component_dictionary):

        if not self.check_fields_exist(single_component_dictionary, _expected_json_fields):
            return

        self._reflectance          = single_component_dictionary[_rcv.WW_SENSOR_VALUE_REFLECTANCE      ]
        self._distance_approximate = single_component_dictionary[_rcv.WW_SENSOR_VALUE_DISTANCE         ]

        self._valid   = True
