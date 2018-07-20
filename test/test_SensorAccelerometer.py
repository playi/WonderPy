import unittest
from test.robotTestUtil import RobotTestUtil


class MyTestCase(unittest.TestCase):

    def test_accelerometer(self):
        robot = RobotTestUtil.make_fake_dash()

        packet = {}
        packet['2003'] = {
            'x' : 1.2,
            'y' : 3.4,
            'z' : 5.6,
        }

        robot.sensors.parse(packet)

        self.assertAlmostEquals(robot.sensors.accelerometer.x, -3.4)
        self.assertAlmostEquals(robot.sensors.accelerometer.y,  1.2)
        self.assertAlmostEquals(robot.sensors.accelerometer.z,  5.6)


if __name__ == '__main__':
    unittest.main()
