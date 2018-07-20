class WWComponentBase(object):

    def __init__(self, robot):
        self._robot = robot

    @property
    def robot(self):
        return self._robot
