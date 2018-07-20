from WonderPy.core.wwConstants import WWRobotConstants
from wwSensorBase import WWSensorBase

_rcv = WWRobotConstants.RobotComponentValues
_expected_json_fields = (
    _rcv.WW_SENSOR_VALUE_BUTTON_STATE,
)


class WWSensorButton(WWSensorBase):

    def __init__(self, robot):
        super(WWSensorButton, self).__init__(robot)
        self._pressed = False

    @property
    def pressed(self):
        return self._pressed

    def _important_field_names(self):
        return ('_pressed',)

    def parse(self, single_component_dictionary):
        if not self.check_fields_exist(single_component_dictionary, _expected_json_fields):
            return

        # "not not" converts truthy things into True or False.  eg 0 and 1 etc.
        self._pressed = not not single_component_dictionary[_rcv.WW_SENSOR_VALUE_BUTTON_STATE]
        self._valid   = True
