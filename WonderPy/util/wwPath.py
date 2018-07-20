# -*- coding: utf-8 -*-

import math
from datetime                  import datetime
from WonderPy.util             import wwMath
from WonderPy.core.wwConstants import WWRobotConstants

_queue_max = 5


class WWPath(object):

    class Pose(object):
        def __init__(self):
            self.x_cm     = 0
            self.y_cm     = 0
            self.degrees  = 0
            self.duration = 0
            self.apt      = 0

        def __str__(self):
            return "%7.2fcm, %7.2fcm, %7.2fº, %7.2fs" % (self.x_cm, self.y_cm, self.degrees, self.duration)

    def __init__(self, points=None):
        self.points              = points if points is not None else []
        self.speed_linear_cm_s   =  20.0
        self.speed_angular_deg_s = 120.0
        self._t0                 = None
        self.stop_continuous_pose = False
        self.is_pose_running = False

    def add_point(self, pt):
        self.points.append(pt)

    def add_points(self, pts):
        self.points.extend(pts)

    def set_max_radius(self, rad):

        # find maximum
        max_len = 0.0
        for point in self.points:
            pt_len = wwMath.vec2_length(point)
            max_len = max(max_len, pt_len)

        # scale
        scale_factor = float(rad) / max_len
        for n in xrange(len(self.points)):
            self.points[n] = wwMath.vec2_scale(self.points[n], scale_factor)

    # take self.points and return a corresponding list of poses.
    # theta is computed for you,
    # and the speed is piecewise linear
    # initial pose is assumed to be the origin.
    # the times are relative to the start, not relative to the time the command is sent:
    # that will have to be calculated when the command is sent.
    def generate_poses(self):
        ret = []

        pos_prev = (0, 0)
        deg_prev = 0
        apt_prev = 0

        # create quadruples. just populating position for now.
        for n in xrange(len(self.points)):
            # pos and angle for this point
            pos_curr = self.points[n]
            deg_curr = self._calc_theta_index_deg(n)

            # calculate linear and angular distance
            dist_deg = deg_curr - deg_prev
            while(dist_deg > 180):
                dist_deg -= 360
            while(dist_deg < -180):
                dist_deg += 360
            dist_pos = wwMath.vec2_length(wwMath.vec2_sub(pos_curr, pos_prev))

            # there's probably a better metric than just the max of the linear & angular distances.
            # maybe something like cartesian length of the linear & angular distances, with some scale.
            # but whatev's.
            dt_deg   = abs(dist_deg) / self.speed_angular_deg_s
            dt_pos   = abs(dist_pos) / self.speed_linear_cm_s
            dt       = max(dt_deg, dt_pos)
            apt_curr = apt_prev + dt

            pose = WWPath.Pose()
            pose.x_cm     = pos_curr[0]
            pose.y_cm     = pos_curr[1]
            pose.degrees  = deg_curr
            pose.duration = dt
            pose.apt      = apt_curr

            ret.append(pose)

            pos_prev = pos_curr
            deg_prev = deg_curr
            apt_prev = apt_curr

        return ret

    def print_poses(self):
        poses = self.generate_poses()
        for p in poses:
            print(str(p))

    def _calc_theta_index_deg(self, point_index):
        nrm = self._calc_direction_index(point_index)
        x, y = wwMath.coords_api_to_json_pos(nrm[0], nrm[1])
        nrm = (x, y)
        return math.degrees(wwMath.direction_to_angle_rads(nrm))

    # calculate a unit-length direction vector for a given point in self.points.
    # this attempts to be the tangent to the path at the vertex.
    def _calc_direction_index(self, point_index):
        # special case: too few points
        if len(self.points) < 2:
            raise Exception("too few points in path")

        # special case: first index
        if point_index == 0:
            vec = wwMath.vec2_sub(self.points[point_index + 1], self.points[point_index    ])
            return wwMath.vec2_normalize(vec)
        # special case: last index
        elif point_index == len(self.points) - 1:
            vec = wwMath.vec2_sub(self.points[point_index    ], self.points[point_index - 1])
            return wwMath.vec2_normalize(vec)
        # general case
        else:
            v1  = wwMath.vec2_sub(self.points[point_index    ], self.points[point_index - 1])
            v2  = wwMath.vec2_sub(self.points[point_index + 1], self.points[point_index    ])
            vn1 = wwMath.vec2_normalize(v1)
            vn2 = wwMath.vec2_normalize(v2)
            v   = wwMath.vec2_add(vn1, vn2)
            vn  = wwMath.vec2_normalize(v)
            return vn

    def do_piecewise(self, robot):
        poses = self.generate_poses()

        robot.block_until_sensors()

        for pose in poses:
            print("pose: %s" % (str(pose)))
            robot.cmds.body.do_pose(pose.x_cm, pose.y_cm, pose.degrees, pose.duration,
                                    WWRobotConstants.WWPoseMode.WW_POSE_MODE_GLOBAL)

    @staticmethod
    def interval_to_seconds(i):
        return (i.days * 24 * 60 * 60) + (i.seconds) + (i.microseconds / 1000000.0)

    def do_go_to_start(self, robot):
        poses = self.generate_poses()
        if len(poses) == 0:
            return

        pose = poses[0]
        robot.cmds.body.do_pose(pose.x_cm, pose.y_cm, pose.degrees, pose.duration * 2.0,
                                WWRobotConstants.WWPoseMode.WW_POSE_MODE_GLOBAL)

    def do_continuous_watermark(self, robot):

        poses = self.generate_poses()

        t_prev = 0
        times = []
        # convert pose durations to times
        for pose in poses:
            t = t_prev + pose.duration
            times.append(t)
            t_prev = t

        next_pose_index = 0

        t0 = None

        while next_pose_index < len(poses):

            # calculate time from now
            if t0 is None:
                t0 = datetime.now()
            s_base = WWPath.interval_to_seconds(datetime.now() - t0)
            # print("%7.2f ewm %2d wm %2d" % (s_base, estimated_poses_in_queue, robot.sensors.pose.watermark))

            wmi = robot.sensors.pose.watermark_inferred

            if (wmi == 255) or (wmi < _queue_max):
                pose = poses[next_pose_index]
                s = times[next_pose_index] - s_base
                # print("sending pose %4d: %s %7.3fs" % (next_pose_index, str(pose), s))
                robot.cmds.body.stage_pose(
                    pose.x_cm,
                    pose.y_cm,
                    pose.degrees,
                    s,
                    WWRobotConstants.WWPoseMode.WW_POSE_MODE_GLOBAL,
                    False,
                    WWRobotConstants.WWPoseDirection.WW_POSE_DIRECTION_FORWARD
                )
                next_pose_index += 1

            robot.block_until_sensors()

        robot.block_until_pose_idle()

    def t_now(self):
        if self._t0 is None:
            self._t0 = datetime.now()

        return WWPath.interval_to_seconds(datetime.now() - self._t0)

    def is_continuous_time_running(self):
        return self.is_pose_running

    def stop_continuous_time(self):
        self.stop_continuous_pose = True
