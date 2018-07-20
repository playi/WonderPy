
from WonderPy.core.wwRobot import WWRobot

kManuData_Dot  = [3, 2, 1, 0, 2, 3, 2, 119, 28, 0, 0, 0, 0, 0, 0, 0, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
kManuData_Dash = [3, 1, 1, 0, 2, 1, 13, 216, 73, 0, 0, 0, 0, 0, 0, 0, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
kManuData_Cue  = [3, 3, 2, 3, 1, 7, 4, 4, 0, 0, 0, 0, 221, 246, 103, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]


class FakeBTLEDevice(object):
    def __init__(self, md, name):
        self.manufacturerData = md
        self.name             = name


class RobotTestUtil(object):

    @staticmethod
    def make_fake_dot():
        return WWRobot(FakeBTLEDevice(kManuData_Dot, "fake dot"))

    @staticmethod
    def make_fake_dash():
        return WWRobot(FakeBTLEDevice(kManuData_Dash, "fake dash"))

    @staticmethod
    def make_fake_cue():
        return WWRobot(FakeBTLEDevice(kManuData_Cue, "fake cue"))
