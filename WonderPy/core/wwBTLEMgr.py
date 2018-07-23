# -*- coding: utf-8 -*-

import uuid
import ctypes
import json
import sys
import argparse
import time
import os

try:
    import Adafruit_BluefruitLE
except ImportError:
    print("Unable to import module: Adafruit_BluefruitLE. You may need to install it manually. See the README.md for WonderPy.")
    raise


if sys.version_info > (3, 0):
    import queue
else:
    import Queue as queue

from wwRobot import WWRobot
from wwConstants import WWRobotConstants
from WonderPy.core import wwMain
from WonderPy.config import WW_ROOT_DIR


class WWException(Exception):
        pass


# Define service and characteristic UUIDs used by the WW devices.
WW_SERVICE_UUID_D1     = uuid.UUID('AF237777-879D-6186-1F49-DECA0E85D9C1')   # dash and dot
WW_SERVICE_UUID_D2     = uuid.UUID('AF237778-879D-6186-1F49-DECA0E85D9C1')   # cue
WW_SERVICE_IDS         = [WW_SERVICE_UUID_D1, WW_SERVICE_UUID_D2]

CHAR_UUID_CMD          = uuid.UUID('AF230002-879D-6186-1F49-DECA0E85D9C1')   # command channel
CHAR_UUID_SENSOR0      = uuid.UUID('AF230003-879D-6186-1F49-DECA0E85D9C1')   # sensor channel 0 (all robots)
CHAR_UUID_SENSOR1      = uuid.UUID('AF230006-879D-6186-1F49-DECA0E85D9C1')   # sensor channel 1 (dash and cue)

# this is used to renegotiate the BTLE connection interval exactly once after establishing connection.
# this value should be as large as possible while being less than about 50ms
# and also without accumulating ping latency.
# typically we're able to just use the default of about 30ms,
# but with the python/osx version we find that a smaller value is needed.
CONNECTION_INTERVAL_MS  = 12


class WWBTLEManager(object):

    def __init__(self, delegate, arguments=None):

        if arguments is None:
            parser = argparse.ArgumentParser(description='Options.')
            WWBTLEManager.setup_argument_parser(parser)
            arguments = parser.parse_args()

        self._args = arguments

        self.delegate = delegate

        self._load_HAL()

        self.robot = None

        self._sensor_queue = queue.Queue()

        # Initialize the BLE system.  MUST be called before other BLE calls!
        self.ble = Adafruit_BluefruitLE.get_provider()
        self.ble.initialize()

    @staticmethod
    def setup_argument_parser(parser):
        parser.add_argument('--connect-name', metavar='a_robot_name', type=str, nargs='+',
                            help='only connect to robots of this name')
        parser.add_argument('--connect-type', metavar='(dash | dot | cue)', type=str, nargs='+',
                            help='only connect to robots of this name')
        parser.add_argument('--connect-eager', action='store_true',
                            help='immediately connect upon finding any qualifying robot')
        parser.add_argument('--connect-patient', action='store_true',
                            help='always wait the full scan period before looking at what we\'ve caught')
        parser.add_argument('--connect-ask', action='store_true',
                            help='interactively ask which of the qualifying robots you\'d like to connect to')

    class two_packet_wrappers(ctypes.Structure):
        _fields_ = [
            ('packet1_bytes_num', ctypes.c_byte),
            ('packet1_bytes'    , ctypes.c_byte * 20),
            ('packet2_bytes_num', ctypes.c_byte),
            ('packet2_bytes'    , ctypes.c_byte * 20),
        ]

    def _load_HAL(self):

        HAL_path = os.path.join(WW_ROOT_DIR, 'lib/WonderWorkshop/osx/libWWHAL.dylib')
        self.libHAL = ctypes.cdll.LoadLibrary(HAL_path)
        self.libHAL.packets2Json.restype  = (ctypes.c_char_p)
        # self.libHAL.json2Packets.argtypes = (c_char_p, WWBTLEManager.two_packet_wrappers)

    @staticmethod
    def byteArrayToCharArray(ba):
        char_array = [ctypes.c_char] * len(ba)
        return char_array.from_buffer(ba)

    @staticmethod
    def string_into_c_byte_array(str, cba):
        n = 0
        for c in str:
            cba[n] = ord(c)
            n += 1

    def scan_and_connect(self):
        # Clear any cached data because both bluez and CoreBluetooth have issues with
        # caching data and it going stale.
        self.ble.clear_cached_data()

        # Get the first available BLE network adapter and make sure it's powered on.
        self.adapter = self.ble.get_default_adapter()
        self.adapter.power_on()
        # print('Using adapter: {0}'.format(self.adapter.name))

        # Disconnect any currently connected devices.
        # Good for cleaning up and starting from a fresh state.
        print('Disconnecting any connected robots..')
        self.ble.disconnect_devices(WW_SERVICE_IDS)

        # Scan for WW devices.
        filter_types = "(all)"
        if self._args.connect_type is not None:
            filter_types = ', '.join(self._args.connect_type)
        filter_names = "(any)"
        if self._args.connect_name is not None:
            filter_names = ', '.join(self._args.connect_name)
        print('Searching for robot types: %s with names: %s.' % (filter_types, filter_names))
        try:
            self.adapter.start_scan()
            # Search for the first WW device found (will time out after 60 seconds
            # but you can specify an optional timeout_sec parameter to change it).

            ticks_min = 5
            ticks_max = 20
            ticks     = 0
            devices    = set()
            devices_no = set()
            while (ticks < ticks_max):
                time.sleep(1)
                ticks += 1
                sys.stdout.write('\rmatching robots: %d  non-matching robots: %d %s%s' %
                                 (len(devices), len(devices_no), '.' * ticks, ' ' * 8))
                sys.stdout.flush()
                for d in self.ble.find_devices(service_uuids=WW_SERVICE_IDS):
                    rob = WWRobot(d)

                    # filters
                    it_passes = True

                    # filter by name
                    if (self._args.connect_name is not None):
                        p = False
                        for n in  self._args.connect_name:
                            if n.lower() == rob.name.lower():
                                p = True
                        it_passes = it_passes and p

                    # filter by type
                    if (self._args.connect_type is not None):
                        p = False
                        for t in self._args.connect_type:
                            t = t.lower()
                            if t == "cue":
                                rt = WWRobotConstants.RobotType.WW_ROBOT_CUE
                            elif t == "dash":
                                rt = WWRobotConstants.RobotType.WW_ROBOT_DASH
                            elif t == "dot":
                                rt = WWRobotConstants.RobotType.WW_ROBOT_DOT
                            else:
                                raise RuntimeError("unhandled robot type option: %s" % (t))

                            if rob.robot_type == rt:
                                p = True

                        it_passes = it_passes and p

                    if it_passes:
                        devices.add(d)
                    else:
                        devices_no.add(d)

                    try_right_now = False
                    try_right_now = try_right_now or ((self._args.connect_eager  ) and (len(devices) > 0))
                    try_right_now = try_right_now or ((ticks > ticks_min         ) and (len(devices) > 0))
                    try_right_now = try_right_now and not self._args.connect_patient

                    if try_right_now:
                        ticks = ticks_max

            sys.stdout.write('\r')

        finally:
            # Make sure scanning is stopped before exiting.
            self.adapter.stop_scan()

        if len(devices_no) > 0:
            sys.stdout.write("found but skipping: ")
            delim = ""
            for d in devices_no:
                r = WWRobot(d)
                sys.stdout.write("%s%s '%s'" % (delim, r.robot_type_name, r.name))
                delim = ', '
            sys.stdout.write('.\n')

        device = None
        sys.stdout.write('\n')
        sys.stdout.flush()


        if len(devices) == 0:
            print("no suitable robots found!")
            quit()

        # find device with loudest signal
        loudest_device = None
        for d in devices:
            if (loudest_device is None) or (d.rssi_last > loudest_device.rssi_last):
                loudest_device = d

        if len(devices) == 1:
            device = devices.pop()
        else:
            if self._args.connect_ask:
                print("Suitable robots:")
                map = {}
                for d in devices:
                    r = WWRobot(d)
                    n = len(map) + 1
                    map[str(n)] = d
                    icon = u'📶' if d == loudest_device else u'⏹'
                    print("%2d. %s %14s '%s'" % (n, icon, r.robot_type_name, r.name))

                device = None
                while device is None:
                    user_choice = raw_input("Enter [%d - %d]: " % (1, len(devices)))
                    if user_choice in map:
                        device = map[user_choice]
                    elif user_choice == '':
                        device = loudest_device
                    else:
                        print("bzzzt")
            else:
                device = loudest_device

                print("found %d suitable robots, choosing the best signal" % (len(devices)))

        self.robot = WWRobot(device)
        self.robot._sendJson = self.sendJson

        print('Connecting to ' + self.robot.robot_type_name + ' "%s"' % (self.robot.name))

        # Will time out after 60 seconds, specify timeout_sec parameter to change the timeout.
        device.connect()

        # Wait for service discovery to complete for at least the specified
        # service and characteristic UUID lists.  Will time out after 60 seconds
        # (specify timeout_sec parameter to override).
        # print('Discovering services...')
        device.discover(WW_SERVICE_IDS, [CHAR_UUID_CMD, CHAR_UUID_SENSOR0, CHAR_UUID_SENSOR1])

        # Find the WW service and its characteristics.
        dService = None
        if dService is None:
            dService = device.find_service(WW_SERVICE_UUID_D1)
        if dService is None:
            dService = device.find_service(WW_SERVICE_UUID_D2)
        if dService is None:
            raise WWException("could not find expected serviceID")

        self.char_cmd     = dService.find_characteristic(CHAR_UUID_CMD)
        self.char_sensor0 = dService.find_characteristic(CHAR_UUID_SENSOR0)
        self.char_sensor1 = dService.find_characteristic(CHAR_UUID_SENSOR1)

        self._send_connection_interval_renegotiation()

        # print('Discovering services...')
        # DeviceInformation.discover(device)

        # Once service discovery is complete create an instance of the service
        # and start interacting with it.

        def cp_data_into_c_byte_array(dst, src):
            n = 0
            for c in src:
                dst[n] = ord(c)

        # Function to receive RX characteristic changes.  Note that this will
        # be called on a different thread so be careful to make sure state that
        # the function changes is thread safe.  Use queue or other thread-safe
        # primitives to send data to other threads.
        def on_data_sensor0(data):
            self.robot._sensor_packet_1 = data
            if not self.robot.expect_sensor_packet_2:
                p1 = self.robot._sensor_packet_1
                pw = WWBTLEManager.two_packet_wrappers()
                WWBTLEManager.string_into_c_byte_array(self.robot._sensor_packet_1, pw.packet1_bytes)
                pw.packet1_bytes_num = len(p1)
                pw.packet2_bytes_num =      0
                json_string = self.libHAL.packets2Json(pw)
                self._sensor_queue.put(json.loads(json_string))
                self.robot._sensor_packet_1 = None

        def on_data_sensor1(data):
            self.robot._sensor_packet_2 = data
            if self.robot._sensor_packet_1 is not None:
                p1 = self.robot._sensor_packet_1
                p2 = self.robot._sensor_packet_2
                pw = WWBTLEManager.two_packet_wrappers()
                WWBTLEManager.string_into_c_byte_array(self.robot._sensor_packet_1, pw.packet1_bytes)
                pw.packet1_bytes_num = len(p1)
                WWBTLEManager.string_into_c_byte_array(self.robot._sensor_packet_2, pw.packet2_bytes)
                pw.packet2_bytes_num = len(p2)
                json_string = self.libHAL.packets2Json(pw)
                self._sensor_queue.put(json.loads(json_string))
                self.robot._sensor_packet_1 = None
                self.robot._sensor_packet_2 = None

        # Turn on notification of RX characteristics using the callback above.
        # print('Subscribing to characteristics...')
        self.char_sensor0.start_notify(on_data_sensor0)
        if self.robot.expect_sensor_packet_2:
            self.char_sensor1.start_notify(on_data_sensor1)

        print('Connected to \'%s\'!' % (self.robot.name))

        if hasattr(self.delegate, 'on_connect') and callable(getattr(self.delegate, 'on_connect')):
            wwMain.thread_local_data.in_on_connect = True
            self.delegate.on_connect(self.robot)
            wwMain.thread_local_data.in_on_connect = False

        while True:
            # blocks until there's something in the queue
            jsonDict = self._sensor_queue.get()
            self.robot._parse_sensors(jsonDict)
            # todo oxe: this delegate should be on the robot

            if hasattr(self.delegate, 'on_sensors') and callable(getattr(self.delegate, 'on_sensors')):
                wwMain.thread_local_data.in_on_sensors = True
                self.delegate.on_sensors(self.robot)
                wwMain.thread_local_data.in_on_sensors = False

            # actually send the commands which have queued up via stage_foo()
            self.robot.send_staged()

    def _send_connection_interval_renegotiation(self):
        # print('Sending renegotiation request for %dms' % (CONNECTION_INTERVAL_MS))
        ba = bytearray(3)
        ba[0] = 0xc9
        ba[1] = CONNECTION_INTERVAL_MS
        ba[2] = CONNECTION_INTERVAL_MS
        self.char_cmd.write_value(ba)

    def sendJson(self, dict):
        if (len(dict) == 0):
            return

        json_str = json.dumps(dict)

        packets = WWBTLEManager.two_packet_wrappers()

        self.libHAL.json2Packets(json_str, ctypes.byref(packets))

        if (packets.packet1_bytes_num > 0):
            self.char_cmd.write_value(packets.packet1_bytes)
        if (packets.packet2_bytes_num > 0):
            self.char_cmd.write_value(packets.packet2_bytes)

    def run(self):
        # Start the mainloop to process BLE events, and run the provided function in
        # a background thread.  When the provided main function stops running, returns
        # an integer status code, or throws an error the program will exit.
        self.ble.run_mainloop_with(self.scan_and_connect)
