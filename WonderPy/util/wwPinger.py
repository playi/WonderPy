from datetime import datetime

# pinger
# this class manages sending and receiving Pings with a WW Robot.
# this is useful for testing the round-trip time of sending something to a robot and getting a response.
# the robot calls tick() after processing each sensor payload.


class WWPinger(object):
    def __init__(self, robot):
        self.active                  = False
        self._outstanding_id         = None
        self._outstanding_time_sent  = None
        self._robot                  = robot
        self._last_id                = None
        self._last_roundtrip_time    = 0
        self._got_ping_this_tick     = False
        self._average_window_size    = 20
        self._average_record         = []
        self._average_roundtrip_time = 0

    @property
    def last_id(self):
        return self._last_id

    @property
    def last_roundtrip_time(self):
        return self._last_roundtrip_time

    @property
    def average_roundtrip_time(self):
        return self._average_roundtrip_time

    @property
    def got_ping_this_tick(self):
        return self._got_ping_this_tick

    def tick(self):
        self._got_ping_this_tick = False

        if not self.active:
            return

        if not self._outstanding_id:
            self._send(1)
        else:
            if self._robot.sensors.ping.id > self._outstanding_id:
                print("warning: missed some pings")
            if self._robot.sensors.ping.id >= self._outstanding_id:
                self._got_ping_this_tick  = True
                self._last_id             = self._robot.sensors.ping.id
                self._last_roundtrip_time = (datetime.now() - self._outstanding_time_sent).total_seconds()
                self._send(self._last_id + 1)
                if len(self._average_record) >= self._average_window_size:
                    self._average_record.pop()
                self._average_record.insert(0, self._last_roundtrip_time)
                self._average_roundtrip_time = sum(self._average_record) / float(len(self._average_record))

    def _send(self, ping_id):
        self._robot.cmds.ping.stage_ping(ping_id)
        self._outstanding_id = ping_id
        self._outstanding_time_sent = datetime.now()
