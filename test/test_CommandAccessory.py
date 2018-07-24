import unittest
from mock import Mock
from WonderPy.core.wwConstants import WWRobotConstants
from test.robotTestUtil import RobotTestUtil
from WonderPy.components.wwCommandAccessory import WWCommandAccessory

_rc = WWRobotConstants.RobotComponent


class MyTestCase(unittest.TestCase):

    def test_sketch_kit(self):
        robot = RobotTestUtil.make_fake_dash()
        robot.stage_cmds = Mock()
        m = robot.stage_cmds

        robot.commands.accessory.do_sketchkit_pen_down()
        robot.commands.accessory.do_sketchkit_pen_up  ()

        self.assertEquals(m.call_count, 4)
        self.assertAlmostEquals(m.call_args_list[0][0][0]['202']['degree'],
                                -WWCommandAccessory.SKETCH_PEN_DN_DEGREES_TLT)
        self.assertAlmostEquals(m.call_args_list[1][0][0]['203']['degree'],
                                 WWCommandAccessory.SKETCH_PEN_DN_DEGREES_PAN)
        self.assertAlmostEquals(m.call_args_list[2][0][0]['214']['prcnt' ],
                                -WWCommandAccessory.SKETCH_PEN_UP_VOLTAGE_TLT)
        self.assertAlmostEquals(m.call_args_list[3][0][0]['213']['prcnt' ],
                                 WWCommandAccessory.SKETCH_PEN_UP_VOLTAGE_PAN)

    def test_xylo(self):
        robot = RobotTestUtil.make_fake_dash()
        robot.stage_cmds = Mock()
        m = robot.stage_cmds

        robot.commands.accessory.do_xylo_hit()

        self.assertEquals(m.call_count, 1)
        self.assertTrue(len(m.call_args_list[0][0][0]['210']) == 0)

    def test_launcher(self):
        robot = RobotTestUtil.make_fake_dash()
        robot.stage_cmds = Mock()
        m = robot.stage_cmds

        robot.commands.accessory.do_launcher_launch      (0.3)
        robot.commands.accessory.do_launcher_reload_left ()
        robot.commands.accessory.do_launcher_reload_right()

        self.assertEquals(m.call_count, 3)
        self.assertAlmostEquals(m.call_args_list[0][0][0]['400']['cm_s'],  0.3)
        self.assertAlmostEquals(m.call_args_list[1][0][0]['401']['dir' ],  0  )
        self.assertAlmostEquals(m.call_args_list[2][0][0]['401']['dir' ],  1  )


if __name__ == '__main__':
    unittest.main()
