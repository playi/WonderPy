from WonderPy.core.wwConstants import WWRobotConstants
from WonderPy.components.wwCommandEyering import WWCommandEyering
from WonderPy.components.wwCommandPing import WWCommandPing
from WonderPy.components.wwCommandBody import WWCommandBody
from WonderPy.components.wwCommandRGB import WWCommandRGB
from WonderPy.components.wwCommandMonoLED import WWCommandMonoLED
from WonderPy.components.wwCommandMedia import WWCommandMedia
from WonderPy.components.wwCommandAccessory import WWCommandAccessory
from WonderPy.components.wwCommandHead import WWCommandHead

_rc  = WWRobotConstants.RobotComponent
_rcv = WWRobotConstants.RobotComponentValues
_rp  = WWRobotConstants.RobotProperties


class WWCommands(object):

    def __init__(self, robot):
        self._robot = robot
        self.eyering    = WWCommandEyering  (robot)
        self.head       = WWCommandHead     (robot)
        self.media      = WWCommandMedia    (robot)
        self.monoLED    = WWCommandMonoLED  (robot)
        self.ping       = WWCommandPing     (robot)
        self.body       = WWCommandBody     (robot)
        self.RGB        = WWCommandRGB      (robot)
        self.accessory  = WWCommandAccessory(robot)
