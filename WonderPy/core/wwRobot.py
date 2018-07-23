import time
import sys

if sys.version_info > (3, 0):
    import queue
else:
    import Queue as queue

from WonderPy.core.wwConstants import WWRobotConstants
from WonderPy.core.wwCommands import WWCommands
from WonderPy.components.wwCommandBase import do_not_call_within_connect_or_sensors
from WonderPy.core.wwSensors import WWSensors
from WonderPy.util.wwPinger import WWPinger


def reverse_lookup(table, value):
    return table.keys()[table.values().index(value)]


_rc = WWRobotConstants.RobotComponent


class WWRobot(object):

    def __init__(self, btleDevice):
        self._btleDevice = btleDevice

        # note: device.manufacturerData is only present when ADAFruit has been patched
        #       with this: https://github.com/adafruit/Adafruit_Python_BluefruitLE/pull/33
        self.parseManufacturerData(btleDevice.manufacturerData)

        self._command_queue = queue.Queue()

        self._sensor_count = long(0)
        self._queues_waiting_for_sensors = set()

        self._sensors           = WWSensors (self)
        self._commands          = WWCommands(self)

        self._sensor_packet_1 = None
        self._sensor_packet_2 = None

        rt = WWRobotConstants.RobotType
        self._expect_sensor_packet_2 = self.robot_type in {rt.WW_ROBOT_DASH, rt.WW_ROBOT_CUE}

        # todo: move this into a 'properties' or 'constants' property
        # todo: this should be None for Dot.
        self._wheelbase_cm      =    9.6

        # todo: move into a 'properties' or 'constants' property
        # todo: these should be determined per-robot.
        self._head_pan_min_deg  = -120.0
        self._head_pan_max_deg  =  120.0
        self._head_tilt_min_deg =  -10.0      # note inverted from json format
        self._head_tilt_max_deg =   22.0      # note inverted from json format

        self.pinger       = WWPinger     (self)

    @property
    def name(self):
        return self._btleDevice.name

    @property
    def robot_type(self):
        return self._robot_type

    @property
    def robot_type_name(self):
        return WWRobotConstants.RobotTypeNames[self.robot_type]

    @property
    def expect_sensor_packet_2(self):
        return self._expect_sensor_packet_2

    @property
    def wheelbase_cm(self):
        return self._wheelbase_cm

    @property
    def head_pan_min_deg(self):
        return self._head_pan_min_deg

    @property
    def head_pan_max_deg(self):
        return self._head_pan_max_deg

    @property
    def head_tilt_min_deg(self):
        return self._head_tilt_min_deg

    @property
    def head_tilt_max_deg(self):
        return self._head_tilt_max_deg

    @property
    def sensors(self):
        return self._sensors

    @property
    def commands(self):
        """
        :rtype:WWCommands
        """
        return self._commands

    @property
    def cmds(self):
        """
        :rtype: WWCommands
        """
        return self._commands

    @property
    def sensor_count(self):
        return self._sensor_count

    def parseManufacturerData(self, manuData):
        """parse the manufacturer data portion of the BTLE advertisement"""

        self._robot_type = WWRobotConstants.RobotType.WW_ROBOT_UNKNOWN
        self._sendJson   = None
        self._mode       = WWRobotConstants.RobotMode.ROBOT_MODE_UNKNOWN

        if not manuData:
            print("error: no manufacturer data. robot: %s" % (self.name))
            return

        self._mode       = manuData[0] & 0x03
        self._robot_type = WWRobot.robot_type_from_manufacturer_data(manuData)

    @staticmethod
    def robot_type_from_manufacturer_data(manu_data):
        mode = manu_data[0] & 0x03
        if   manu_data[1] == 1 and mode == WWRobotConstants.RobotMode.ROBOT_MODE_APP:
            return WWRobotConstants.RobotType.WW_ROBOT_DASH
        elif manu_data[1] == 1 and mode == WWRobotConstants.RobotMode.ROBOT_MODE_BL:
            return WWRobotConstants.RobotType.WW_ROBOT_DASH_DFU
        elif manu_data[1] == 2 and mode == WWRobotConstants.RobotMode.ROBOT_MODE_APP:
            return WWRobotConstants.RobotType.WW_ROBOT_DOT
        elif manu_data[1] == 2 and mode == WWRobotConstants.RobotMode.ROBOT_MODE_BL:
            return WWRobotConstants.RobotType.WW_ROBOT_DOT_DFU
        elif manu_data[1] == 3 and mode == WWRobotConstants.RobotMode.ROBOT_MODE_APP:
            return WWRobotConstants.RobotType.WW_ROBOT_CUE
        elif manu_data[1] == 3 and mode == WWRobotConstants.RobotMode.ROBOT_MODE_BL:
            return WWRobotConstants.RobotType.WW_ROBOT_CUE_DFU

        return WWRobotConstants.RobotType.WW_ROBOT_UNKNOWN

    def stage_cmds(self, cmds):
        """takes a dictionary who's keys are command components and values are the parameters for each"""
        self._command_queue.put(cmds)

        # we do this here instead of in the send_staged() so that callers will see the effect synchronously.
        if self.sensors.pose is not None:
            self.sensors.pose.handle_staged_motion_commands(cmds)

    def send_staged(self):

        # merge the on-deck commands.
        # todo: deal with non-mergable commands. see APIJS.
        staged = {}
        while not self._command_queue.empty():
            cmds = self._command_queue.get()
            for key in cmds:
                staged[key] = cmds[key]

        # and then send them
        self._sendJson(staged)

    def _parse_sensors(self, sensor_dictionary):
        # make a copy of the set of waiters and then clear out the member set.
        # we do this because once we do a put() to the waiters,
        # we do this because once we do a put() to the waiters,
        # they may re-insert new items in the waiters list by re-calling block_until_sensors().
        waiters = self._queues_waiting_for_sensors
        self._queues_waiting_for_sensors = set()

        # parse json into python structs
        self._sensors.parse(sensor_dictionary)
        self._sensor_count += 1
        self.pinger.tick()

        # notify everyone who was waiting
        for q in waiters:
            q.put(None)

    @do_not_call_within_connect_or_sensors
    def block_until_sensors(self):
        """this blocks until the next sensor packet arrives"""
        # create a new queue and add it to the set of waiters.
        # this queue will only ever be used once.
        q = queue.Queue()
        self._queues_waiting_for_sensors.add(q)
        # block until our queue gets something in it.
        q.get()

    @do_not_call_within_connect_or_sensors
    def block_until_pose_idle(self):
        self.sensors.pose.block_until_idle()

    @do_not_call_within_connect_or_sensors
    def block_until_button_main_press_and_release(self):
        while not self.sensors.button_main.valid:
            self.block_until_sensors()

        btn_brightness = 0
        while not self.sensors.button_main.pressed:
            tmp = 1.0 if (int(time.time() * 2.0)) % 2 else 0
            if tmp != btn_brightness:
                btn_brightness = tmp
                self.cmds.monoLED.stage_button_main(btn_brightness)
            self.block_until_sensors()

        while self.sensors.button_main.pressed:
            tmp = 1.0 if (int(time.time() * 6.0)) % 2 else 0
            if tmp != btn_brightness:
                btn_brightness = tmp
                self.cmds.monoLED.stage_button_main(btn_brightness)
            self.block_until_sensors()

        self.cmds.monoLED.stage_button_main(0)

    def has_ability(self, ability, log_if_no):
        rav = WWRobotConstants.WWRobotAbilities.values()
        if ability not in rav:
            raise ValueError("Unknown robot ability: %s" % (str(ability)))

        ret = self.robot_type in rav[ability]
        if log_if_no and not ret:
            print("Robot '%s' does not have the ability '%s'" % (self.name, ability))

        return ret
