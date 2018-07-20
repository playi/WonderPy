import unittest
from test.robotTestUtil import RobotTestUtil


class MyTestCase(unittest.TestCase):

    def test_head(self):
        robot = RobotTestUtil.make_fake_dash()

        packet = {}
        packet['2000'] = {
            'degree': 1.2,
        }
        packet['2001'] = {
            'degree': 3.4,
        }

        robot.sensors.parse(packet)
        sensors = robot.sensors

        self.assertAlmostEquals(sensors.head_pan .degrees,  1.2)
        self.assertAlmostEquals(sensors.head_tilt.degrees, -3.4)


if __name__ == '__main__':
    unittest.main()
