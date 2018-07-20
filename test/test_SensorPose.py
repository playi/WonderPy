import unittest
from test.robotTestUtil import RobotTestUtil


class MyTestCase(unittest.TestCase):

    def test_pose(self):
        robot = RobotTestUtil.make_fake_dash()

        packet = {}
        packet['2002'] = {
            'x'     : 1.2,
            'y'     : 3.4,
            'degree': 5.6,
        }

        robot.sensors.parse(packet)
        sensor = robot.sensors.pose

        self.assertAlmostEquals(sensor.x      , -3.4)
        self.assertAlmostEquals(sensor.y      ,  1.2)
        self.assertAlmostEquals(sensor.degrees,  5.6)
        self.assertTrue        (sensor.watermark_measured is None)
        self.assertAlmostEquals(sensor.watermark_inferred, 0.0)

        packet['2002'] = {
            'x'        : 1.2,
            'y'        : 3.4,
            'degree'   : 5.6,
            'watermark': 3,
        }

        robot.sensors.parse(packet)
        sensor = robot.sensors.pose

        self.assertAlmostEquals(sensor.x                 , -3.4)
        self.assertAlmostEquals(sensor.y                 ,  1.2)
        self.assertAlmostEquals(sensor.degrees           ,  5.6)
        self.assertAlmostEquals(sensor.watermark_measured,  3)
        self.assertAlmostEquals(sensor.watermark_inferred,  3)


if __name__ == '__main__':
    unittest.main()
