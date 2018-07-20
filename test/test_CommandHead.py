import unittest
from mock import Mock
from test.robotTestUtil import RobotTestUtil


class MyTestCase(unittest.TestCase):

    def test_head_turn(self):
        robot = RobotTestUtil.make_fake_dash()
        robot.stage_cmds = Mock()
        m = robot.stage_cmds

        robot.commands.head.do_pan_angle       (90)
        robot.commands.head.do_tilt_angle      (10)
        robot.commands.head.do_pan_voltage     (75)
        robot.commands.head.do_tilt_voltage    (85)
        robot.commands.head.do_pan_tilt_angle  (-45.3, -30.3)
        robot.commands.head.do_pan_tilt_voltage(-10.3, -11.3)

        self.assertEquals(m.call_count, 8)
        self.assertAlmostEquals(m.call_args_list[0][0][0]['203']['degree'],  90)
        self.assertAlmostEquals(m.call_args_list[1][0][0]['202']['degree'], -10)
        self.assertAlmostEquals(m.call_args_list[2][0][0]['213']['prcnt' ],  75)
        self.assertAlmostEquals(m.call_args_list[3][0][0]['214']['prcnt' ], -85)
        self.assertAlmostEquals(m.call_args_list[4][0][0]['203']['degree'], -45.3)
        self.assertAlmostEquals(m.call_args_list[5][0][0]['202']['degree'],  30.3)
        self.assertAlmostEquals(m.call_args_list[6][0][0]['213']['prcnt' ], -10.3)
        self.assertAlmostEquals(m.call_args_list[7][0][0]['214']['prcnt' ],  11.3)


if __name__ == '__main__':
    unittest.main()
