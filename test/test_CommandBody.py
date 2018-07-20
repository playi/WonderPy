import unittest
from mock import Mock
from test.robotTestUtil import RobotTestUtil
from WonderPy.core.wwConstants import WWRobotConstants

_rc  = WWRobotConstants.RobotComponent
_rcv = WWRobotConstants.RobotComponentValues


class MyTestCase(unittest.TestCase):

    def test_body_pose(self):
        robot = RobotTestUtil.make_fake_dash()
        robot.stage_cmds = Mock()
        m = robot.stage_cmds

        robot.cmds.body.stage_pose(1.23, 4.56, 7.89, 1.0, WWRobotConstants.WWPoseMode.WW_POSE_MODE_GLOBAL)

        cmd = m.call_args_list[0][0][0]['205']
        self.assertEquals(m.call_count, 1)
        self.assertAlmostEquals(cmd['x'     ],  4.56)
        self.assertAlmostEquals(cmd['y'     ], -1.23)
        self.assertAlmostEquals(cmd['degree'], 7.89 )
        self.assertEquals      (cmd['mode'  ],  0   )
        self.assertAlmostEquals(cmd['time'  ],  1.0 )

    def test_body_linear_angular(self):
        robot = RobotTestUtil.make_fake_dash()
        robot.stage_cmds = Mock()
        m = robot.stage_cmds

        robot.commands.body.stage_linear_angular(12.3, 45.6, 7.8, 9.0)
        robot.commands.body.stage_wheel_speeds  (12.3, 45.6)

        self.assertEquals(m.call_count, 2)
        n = 0

        cmd = m.call_args_list[n][0][0]['204']
        n += 1
        self.assertAlmostEquals(cmd['angular_deg_s'      ],  45.6)
        self.assertAlmostEquals(cmd['angular_acc_deg_s_s'],   9.0)
        self.assertAlmostEquals(cmd['linear_cm_s'        ],  12.3)
        self.assertAlmostEquals(cmd['linear_acc_cm_s_s'  ],   7.8)

        cmd = m.call_args_list[n][0][0]['204']
        n += 1
        self.assertAlmostEquals(cmd['angular_deg_s'      ],  198.74473518)
        self.assertAlmostEquals(cmd['angular_acc_deg_s_s'],  900.0)
        self.assertAlmostEquals(cmd['linear_cm_s'        ],   28.95)
        self.assertAlmostEquals(cmd['linear_acc_cm_s_s'  ],   50.0)

    def test_body_stop(self):
        robot = RobotTestUtil.make_fake_dash()
        robot.stage_cmds = Mock()
        m = robot.stage_cmds

        robot.commands.body.stage_stop(12.3, 45.6)

        self.assertEquals(m.call_count, 1)
        n = 0

        cmd = m.call_args_list[n][0][0]['204']
        n += 1
        self.assertAlmostEquals(cmd['angular_deg_s'      ],   0.0)
        self.assertAlmostEquals(cmd['angular_acc_deg_s_s'],  45.6)
        self.assertAlmostEquals(cmd['linear_cm_s'        ],   0.0)
        self.assertAlmostEquals(cmd['linear_acc_cm_s_s'  ],  12.3)

    def test_body_wheels_naive(self):
        robot = RobotTestUtil.make_fake_dash()
        robot.stage_cmds = Mock()
        m = robot.stage_cmds

        robot.commands.body.stage_wheel_speeds_naive  (12.3, 45.6)

        self.assertEquals(m.call_count, 1)
        n = 0

        cmd = m.call_args_list[n][0][0]['211']
        n += 1
        self.assertAlmostEquals(cmd['left_cm_s' ],  12.3)
        self.assertAlmostEquals(cmd['right_cm_s'],  45.6)


if __name__ == '__main__':
    unittest.main()
