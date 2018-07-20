from WonderPy.core.wwConstants import WWRobotConstants
from WonderPy.util import wwMath
from WonderPy.components.wwSensorButton import WWSensorButton
from WonderPy.components.wwSensorAccelerometer import WWSensorAccelerometer
from WonderPy.components.wwSensorPose import WWSensorPose
from WonderPy.components.wwSensorPing import WWSensorPing
from WonderPy.components.wwSensorMedia import WWSensorMedia
from WonderPy.components.wwSensorAngle import WWSensorAngle
from WonderPy.components.wwSensorDistance import WWSensorDistance
from WonderPy.components.wwSensorBeacon import WWSensorBeacon
from WonderPy.components.wwSensorWheel import WWSensorWheel
from WonderPy.components.wwSensorGyroscope import WWSensorGyroscope

_rc = WWRobotConstants.RobotComponent


class WWSensors(object):

    def __init__(self, robot):
        self.setup_all_sensors(robot)

    # the approach here is to have an object for ALL POSSIBLE sensors.
    # each packet which comes in will mark each contained sensor as "valid".
    # so client code should check `if WWSensors.whatever.valid` .
    # there are a couple cases where the sensors might not contain a given sensor:
    # * if the sensor is not supported by a particular robot.
    #   for example, Dot has no gyroscope or wheel sensors.
    # * some sensors are 'sparse', meaning the robot only sends them periodically.
    #   for example, the battery level sensor is only sent every 10 packets or so.
    # * some sensors are 'events', meaning they're only sent when an event is detected.
    #   an example is voice- or clap-detection.

    def setup_all_sensors(self, robot):
        self._sensor_dict                 = None

        # common
        self._accelerometer               = WWSensorAccelerometer(robot)
        self._animation                   = WWSensorMedia        (robot)
        self._button_main                 = WWSensorButton       (robot)
        self._button_1                    = WWSensorButton       (robot)
        self._button_2                    = WWSensorButton       (robot)
        self._button_3                    = WWSensorButton       (robot)
        self._ping                        = WWSensorPing         (robot)
        self._speaker                     = WWSensorMedia        (robot)
        self._voice                       = None

        # dash & cue
        self._beacon                      = WWSensorBeacon       (robot)
        self._distance_front_left_facing  = WWSensorDistance     (robot)
        self._distance_front_right_facing = WWSensorDistance     (robot)
        self._distance_rear               = WWSensorDistance     (robot)
        self._gyroscope                   = WWSensorGyroscope    (robot)
        self._head_pan                    = WWSensorAngle        (robot, wwMath.coords_api_to_json_pan )
        self._head_tilt                   = WWSensorAngle        (robot, wwMath.coords_api_to_json_tilt)
        self._pose                        = WWSensorPose         (robot)
        self._wheel_left                  = WWSensorWheel        (robot)
        self._wheel_right                 = WWSensorWheel        (robot)

        self._component_look_up = {
            _rc.WW_SENSOR_ACCELEROMETER               : self._accelerometer,
            _rc.WW_SENSOR_ANIMATION_PLAYING           : self._animation,
            _rc.WW_SENSOR_BEACON                      : self._beacon,
            _rc.WW_SENSOR_BODY_POSE                   : self._pose,
            _rc.WW_SENSOR_BUTTON_1                    : self._button_1,
            _rc.WW_SENSOR_BUTTON_2                    : self._button_2,
            _rc.WW_SENSOR_BUTTON_3                    : self._button_3,
            _rc.WW_SENSOR_BUTTON_MAIN                 : self._button_main,
            _rc.WW_SENSOR_DISTANCE_BACK               : self._distance_rear,
            _rc.WW_SENSOR_DISTANCE_FRONT_LEFT_FACING  : self._distance_front_left_facing,
            _rc.WW_SENSOR_DISTANCE_FRONT_RIGHT_FACING : self._distance_front_right_facing,
            _rc.WW_SENSOR_ENCODER_LEFT_WHEEL          : self._wheel_left,
            _rc.WW_SENSOR_ENCODER_RIGHT_WHEEL         : self._wheel_right,
            _rc.WW_SENSOR_HEAD_POSITION_PAN           : self._head_pan,
            _rc.WW_SENSOR_HEAD_POSITION_TILT          : self._head_tilt,
            _rc.WW_SENSOR_GYROSCOPE                   : self._gyroscope,
            _rc.WW_SENSOR_PING_RESPONSE               : self._ping,
            _rc.WW_SENSOR_SOUND_PLAYING               : self._speaker,
        }

    @property
    def accelerometer(self):
        return self._accelerometer

    @property
    def animation(self):
        return self._animation

    @property
    def beacon(self):
        return self._beacon

    @property
    def button_1(self):
        return self._button_1

    @property
    def button_2(self):
        return self._button_2

    @property
    def button_3(self):
        return self._button_3

    @property
    def button_main(self):
        return self._button_main

    @property
    def distance_front_left_facing(self):
        return self._distance_front_left_facing

    @property
    def distance_front_right_facing(self):
        return self._distance_front_right_facing

    @property
    def distance_rear(self):
        return self._distance_rear

    @property
    def head_pan(self):
        return self._head_pan

    @property
    def head_tilt(self):
        return self._head_tilt

    @property
    def gyroscope(self):
        return self._gyroscope

    @property
    def ping(self):
        return self._ping

    @property
    def pose(self):
        return self._pose

    @property
    def speaker(self):
        return self._speaker

    @property
    def wheel_left(self):
        return self._wheel_left

    @property
    def wheel_right(self):
        return self._wheel_right

    def parse(self, sensorDict):
        for component_id in sensorDict:
            if component_id not in self._component_look_up:
                # print("error: unhandled sensor component id: %s" % (component_id))
                continue
            else:
                component = self._component_look_up[component_id]
                if component is not None:
                    component.parse(sensorDict[component_id])

        self._backfill_beacon(sensorDict)

    def _backfill_beacon(self, sensor_dict):
        # we only get beacon sensors if something is seen, and not if something is not seen.
        if _rc.WW_SENSOR_BEACON in sensor_dict:
            return

        if self._beacon is not None:
            self._beacon.parse({})

    def description(self):
        ret = ""
        delim = ""
        for component_id in self._component_look_up:
            component = self._component_look_up[component_id]
            if (component is not None) and (component.valid):
                ret   = ret + delim + "%-40s: %s" % (WWRobotConstants.RobotComponent.names[component_id],
                                                     component.description())
                delim = "\n"
        return ret
