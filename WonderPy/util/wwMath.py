# -*- coding: utf-8 -*-

import math


def lerp(a, b, t):
    range = b - a
    return (range * t) + a


def inverse_lerp(a, b, x):
    range = b - a
    return (x - a) / range


def clamp(min_v, max_v, value):
    return min(max_v, max(value, min_v))


def clamp01(value):
    return clamp(0.0, 1.0, value)


def clamp_with_warning(min_v, max_v, value, name):
    if value < min:
        print("warning: %s underflow. %s < %s." % (name, value, min_v))
        return min_v
    elif value > max:
        print("warning: %s overflow. %s > %s." % (name, value, max_v))
        return max_v
    else:
        return value


def polar_to_cartesian(theta, radius):
    x = math.cos(theta) * radius
    y = math.sin(theta) * radius
    return x, y


def sqrt_signed(a):
    return math.copysign(math.sqrt(math.fabs(a)))


def direction_to_angle_rads(unit_length_vector):
    return math.atan2(unit_length_vector[1], unit_length_vector[0])


# the json protocol uses a coordinate system where:
# "+X" is Forward, "+Y" is Left, and positive angles are degrees counter-clockwise for pan and down for tilt.
# for the Python API we're opting to have "+X" be Right, "+Y" be Forward,
# and positive angles are still counter-clockwise for pan, but up for tilt.
# Both systems are right-handed. The Python API simply rotates the coordinate axes 90º clockwise about +Z.


def coords_api_to_json_pos(x_cm_right, y_cm_forward):
    """converts from API coordinates to robot coordinates. returns x, y"""
    x_cm_forward =  y_cm_forward
    y_cm_left    = -x_cm_right
    return x_cm_forward, y_cm_left


def coords_json_to_api_pos(x_cm_forward, y_cm_left):
    """converts from robot coordinates to API coordinates. returns x, y"""
    x_cm_right   = -y_cm_left
    y_cm_forward =  x_cm_forward
    return x_cm_right, y_cm_forward


def coords_api_to_json_pan(ang_clockwise):
    """converts from API coordinates to robot coordinates."""
    return ang_clockwise


def coords_json_to_api_pan(ang_clockwise):
    """converts from robot coordinates to API coordinates."""
    return ang_clockwise


def coords_api_to_json_tilt(ang_up):
    """converts from API coordinates to robot coordinates."""
    ang_down = -ang_up
    return ang_down


def coords_json_to_api_tilt(ang_down):
    """converts from API coordinates to robot coordinates."""
    ang_up = -ang_down
    return ang_up

###########################################################


def vec2_add(va, vb):
    return va[0] + vb[0], va[1] + vb[1]


def vec2_sub(va, vb):
    return va[0] - vb[0], va[1] - vb[1]


def vec2_scale(va, s):
    return va[0] * s, va[1] * s


def vec2_length(va):
    return math.sqrt((va[0] * va[0]) + (va[1] * va[1]))


def vec2_normalize(va):
    length = vec2_length(va)
    return vec2_scale(va, 1.0 / length)

###########################################################
