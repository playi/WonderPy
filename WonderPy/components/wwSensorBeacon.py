from WonderPy.core.wwConstants import WWRobotConstants
from wwSensorBase import WWSensorBase

_rcv = WWRobotConstants.RobotComponentValues
_rt  = WWRobotConstants.RobotType
_expected_json_fields = (
    # the beacon sensor is a bit special, as we may invent empty ones.
)


class WWSensorBeacon(WWSensorBase):

    def __init__(self, robot):
        super(WWSensorBeacon, self).__init__(robot)
        self._robot_type_left_raw  = None
        self._robot_type_right_raw = None
        self._robot_type_left      = None
        self._robot_type_right     = None
        self._filter_left          = WWSensorBeacon.BeaconFilter()
        self._filter_right         = WWSensorBeacon.BeaconFilter()
        self.data_window_size      = 25

    @property
    def robot_type_left_raw(self):
        """
        what type of robot is seen via the left-facing beacon sensor.
        this is the raw or most recent data received.
        the beacon sensor is 'sparse', meaning the robot only emits it periodically, and only when it sees something.
        the robot does not emit a beacon sensor when it does not see something.
        for this reason it is recommended to use the non-raw version of this sensor, as it includes some data filtering.
        """
        return self._robot_type_left_raw

    @property
    def robot_type_right_raw(self):
        """
        what type of robot is seen via the right-facing beacon sensor.
        this is the raw or most recent data received.
        the beacon sensor is 'sparse', meaning the robot only emits it periodically, and only when it sees something.
        the robot does not emit a beacon sensor when it does not see something.
        for this reason it is recommended to use the non-raw version of this sensor, as it includes some data filtering.
         """
        return self._robot_type_right_raw

    @property
    def robot_type_left(self):
        """
        what type of robot is seen via the left-facing beacon sensor, with filtering.
        """
        return self._robot_type_left

    @property
    def robot_type_right(self):
        """
        what type of robot is seen via the right-facing beacon sensor, with filtering.
        """
        return self._robot_type_right

    @property
    def data_window_size(self):
        return self._filter_left.data_window_size

    @data_window_size.setter
    def data_window_size(self, value):
        self._filter_left .data_window_size = value
        self._filter_right.data_window_size = value

    def _important_field_names(self):
        return ('_robot_type_left_raw', '_robot_type_right_raw', '_robot_type_left', '_robot_type_right')

    def parse(self, single_component_dictionary):
        if not self.check_fields_exist(single_component_dictionary, _expected_json_fields):
            return

        rt_l   = None
        rt_r   = None

        if _rcv.WW_SENSOR_VALUE_BEACON_DATA_LEFT in single_component_dictionary:
            data = single_component_dictionary[_rcv.WW_SENSOR_VALUE_BEACON_DATA_LEFT ]
            rt_l = WWSensorBeacon.data_to_robot_type(data)

        if _rcv.WW_SENSOR_VALUE_BEACON_DATA_RIGHT in single_component_dictionary:
            data = single_component_dictionary[_rcv.WW_SENSOR_VALUE_BEACON_DATA_RIGHT ]
            rt_r = WWSensorBeacon.data_to_robot_type(data)

        self._filter_left .add_robot_type_value(rt_l)
        self._filter_right.add_robot_type_value(rt_r)

        self._robot_type_left_raw  = rt_l
        self._robot_type_right_raw = rt_r
        self._robot_type_left      = self._filter_left .get_robot_type()
        self._robot_type_right     = self._filter_right.get_robot_type()

        self._valid   = True

    _beacon_value_to_robot_type = {
        0x55 : _rt.WW_ROBOT_DASH,
        0xAA : _rt.WW_ROBOT_DOT,
        0x33 : _rt.WW_ROBOT_CUE,
    }

    @staticmethod
    def data_to_robot_type(value):
        if value is None:
            return None

        if value == 4095:
            return None

        if value in WWSensorBeacon._beacon_value_to_robot_type:
            return WWSensorBeacon._beacon_value_to_robot_type[value]
        else:
            return _rt.WW_ROBOT_UNKNOWN

    class BeaconFilter(object):
        def __init__(self):
            self._data_buffer       = [None] * 1
            self._data_buffer_index = 0

        @property
        def data_window_size(self):
            return len(self._data_buffer)

        @data_window_size.setter
        def data_window_size(self, value):
            old_db  = self._data_buffer
            old_dbi = self._data_buffer_index
            self._data_buffer = [None] * value
            self._data_buffer_index = 0
            for n in xrange(min(len(old_db), value)):
                self.add_robot_type_value(old_db[n])
            self._data_buffer_index = old_dbi % value

        def add_robot_type_value(self, value):
            self._data_buffer[self._data_buffer_index] = value
            self._data_buffer_index = (self._data_buffer_index + 1) % len(self._data_buffer)

        def get_robot_type(self):
            value_counts  = {}
            highest_count = 0
            ret           = None
            for value in self._data_buffer:
                if value is not None:
                    if value not in value_counts:
                        value_counts[value] = 0
                    new_count = value_counts[value] + 1
                    value_counts[value] = new_count
                    if new_count > highest_count:
                        ret           = value
                        highest_count = new_count

            return ret
