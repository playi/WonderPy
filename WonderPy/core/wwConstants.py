class WWRobotConstants(object):

    class RobotType:
        WW_ROBOT_UNKNOWN  = 1000
        WW_ROBOT_DASH     = 1001
        WW_ROBOT_DOT      = 1002
        WW_ROBOT_CUE      = 1003
        WW_ROBOT_DASH_DFU = 2001
        WW_ROBOT_DOT_DFU  = 2002
        WW_ROBOT_CUE_DFU  = 2003

    class RobotProperties(object):
        EYE_LED_COUNT     = 12

    RobotTypeNames = {
        RobotType.WW_ROBOT_UNKNOWN : "WW_ROBOT_UNKNOWN",
        RobotType.WW_ROBOT_DASH    : "WW_ROBOT_DASH",
        RobotType.WW_ROBOT_DOT     : "WW_ROBOT_DOT",
        RobotType.WW_ROBOT_CUE     : "WW_ROBOT_CUE",
        RobotType.WW_ROBOT_DASH_DFU: "WW_ROBOT_DASH_DFU",
        RobotType.WW_ROBOT_DOT_DFU : "WW_ROBOT_DOT_DFU",
        RobotType.WW_ROBOT_CUE_DFU : "WW_ROBOT_CUE_DFU",
    }

    class RobotMode(object):
        ROBOT_MODE_UNKNOWN = 0x0
        ROBOT_MODE_BL      = 0x1
        ROBOT_MODE_DIAG    = 0x2
        ROBOT_MODE_APP     = 0x3

    class RobotComponent(object):
        WW_COMMAND_POWER                      =    '1'
        WW_COMMAND_EYE_RING                   =  '100'
        WW_COMMAND_LIGHT_RGB_EYE              =  '101'
        WW_COMMAND_LIGHT_RGB_LEFT_EAR         =  '102'
        WW_COMMAND_LIGHT_RGB_RIGHT_EAR        =  '103'
        WW_COMMAND_LIGHT_RGB_CHEST            =  '104'
        WW_COMMAND_LIGHT_MONO_TAIL            =  '105'
        WW_COMMAND_LIGHT_MONO_BUTTON_MAIN     =  '106'
        WW_COMMAND_LIGHT_RGB_BUTTON_MAIN      =  '107'
        WW_COMMAND_LIGHT_MONO_BUTTONS         =  '108'
        WW_COMMAND_LIGHT_MONO_BUTTON_1        =  '109'  # cue button light - circle
        WW_COMMAND_LIGHT_MONO_BUTTON_2        =  '110'  # cue button light - square
        WW_COMMAND_LIGHT_MONO_BUTTON_3        =  '111'  # cue button light - triangle
        WW_COMMAND_HEAD_POSITION_TILT         =  '202'
        WW_COMMAND_HEAD_POSITION_PAN          =  '203'
        WW_COMMAND_BODY_LINEAR_ANGULAR        =  '204'
        WW_COMMAND_BODY_POSE                  =  '205'
        WW_COMMAND_MOTOR_HEAD_BANG            =  '210'
        WW_COMMAND_BODY_WHEELS                =  '211'
        WW_COMMAND_BODY_COAST                 =  '212'
        WW_COMMAND_HEAD_PAN_VOLTAGE           =  '213'
        WW_COMMAND_HEAD_TILT_VOLTAGE          =  '214'
        WW_COMMAND_SPEAKER                    =  '300'
        WW_COMMAND_ON_ROBOT_ANIM              =  '301'
        WW_COMMAND_LAUNCHER_FLING             =  '400'
        WW_COMMAND_LAUNCHER_RELOAD            =  '401'
        WW_COMMAND_LED_MESSAGE                =  '410'
        WW_COMMAND_SET_PING                   = '9000'

        WW_SENSOR_BUTTON_MAIN                 = '1000'
        WW_SENSOR_BUTTON_1                    = '1001'
        WW_SENSOR_BUTTON_2                    = '1002'
        WW_SENSOR_BUTTON_3                    = '1003'
        WW_SENSOR_HEAD_POSITION_PAN           = '2000'
        WW_SENSOR_HEAD_POSITION_TILT          = '2001'
        WW_SENSOR_BODY_POSE                   = '2002'  # global position & orientation of the robot
        WW_SENSOR_ACCELEROMETER               = '2003'
        WW_SENSOR_GYROSCOPE                   = '2004'
        WW_SENSOR_DISTANCE_FRONT_LEFT_FACING  = '3000'
        WW_SENSOR_DISTANCE_FRONT_RIGHT_FACING = '3001'
        WW_SENSOR_DISTANCE_BACK               = '3002'
        WW_SENSOR_ENCODER_LEFT_WHEEL          = '3003'
        WW_SENSOR_ENCODER_RIGHT_WHEEL         = '3004'
        WW_SENSOR_MICROPHONE                  = '3005'
        WW_SENSOR_BATTERY                     = '3006'
        WW_SENSOR_BEACON                      = '3007'  # seeing another dash or dot
        WW_SENSOR_BEACON_V2                   = '3009'
        WW_SENSOR_PICKED_UP                   = '4001'  # note= has significant false negatives
        WW_SENSOR_BUMP_STALL                  = '4002'  # note= has significant false negatives
        WW_SENSOR_SOUND_PLAYING               = '4003'  # on-robot sound     is playing
        WW_SENSOR_ANIMATION_PLAYING           = '4006'  # on-robot animation is playing
        WW_SENSOR_CHARACTERISTIC_1            = '5101'  # raw data
        WW_SENSOR_CHARACTERISTIC_2            = '5102'  # raw data
        WW_SENSOR_PING_RESPONSE               = '9000'

        WW_SENSOR_TIMESTAMP                   = 'tm'    # which one of these things is not like the others ?

        names = {
            WW_COMMAND_POWER                      : 'WW_COMMAND_POWER',
            WW_COMMAND_EYE_RING                   : 'WW_COMMAND_EYE_RING',
            WW_COMMAND_LIGHT_RGB_EYE              : 'WW_COMMAND_LIGHT_RGB_EYE',
            WW_COMMAND_LIGHT_RGB_LEFT_EAR         : 'WW_COMMAND_LIGHT_RGB_LEFT_EAR',
            WW_COMMAND_LIGHT_RGB_RIGHT_EAR        : 'WW_COMMAND_LIGHT_RGB_RIGHT_EAR',
            WW_COMMAND_LIGHT_RGB_CHEST            : 'WW_COMMAND_LIGHT_RGB_CHEST',
            WW_COMMAND_LIGHT_MONO_TAIL            : 'WW_COMMAND_LIGHT_MONO_TAIL',
            WW_COMMAND_LIGHT_MONO_BUTTON_MAIN     : 'WW_COMMAND_LIGHT_MONO_BUTTON_MAIN',
            WW_COMMAND_LIGHT_RGB_BUTTON_MAIN      : 'WW_COMMAND_LIGHT_RGB_BUTTON_MAIN',
            WW_COMMAND_LIGHT_MONO_BUTTONS         : 'WW_COMMAND_LIGHT_MONO_BUTTONS',
            WW_COMMAND_LIGHT_MONO_BUTTON_1        : 'WW_COMMAND_LIGHT_MONO_BUTTON_1',
            WW_COMMAND_LIGHT_MONO_BUTTON_2        : 'WW_COMMAND_LIGHT_MONO_BUTTON_2',
            WW_COMMAND_LIGHT_MONO_BUTTON_3        : 'WW_COMMAND_LIGHT_MONO_BUTTON_3',
            WW_COMMAND_HEAD_POSITION_TILT         : 'WW_COMMAND_HEAD_POSITION_TILT',
            WW_COMMAND_HEAD_POSITION_PAN          : 'WW_COMMAND_HEAD_POSITION_PAN',
            WW_COMMAND_BODY_LINEAR_ANGULAR        : 'WW_COMMAND_BODY_LINEAR_ANGULAR',
            WW_COMMAND_BODY_POSE                  : 'WW_COMMAND_BODY_POSE',
            WW_COMMAND_MOTOR_HEAD_BANG            : 'WW_COMMAND_MOTOR_HEAD_BANG',
            WW_COMMAND_BODY_WHEELS                : 'WW_COMMAND_BODY_WHEELS',
            WW_COMMAND_BODY_COAST                 : 'WW_COMMAND_BODY_COAST',
            WW_COMMAND_HEAD_PAN_VOLTAGE           : 'WW_COMMAND_HEAD_PAN_VOLTAGE',
            WW_COMMAND_HEAD_TILT_VOLTAGE          : 'WW_COMMAND_HEAD_TILT_VOLTAGE',
            WW_COMMAND_SPEAKER                    : 'WW_COMMAND_SPEAKER',
            WW_COMMAND_ON_ROBOT_ANIM              : 'WW_COMMAND_ON_ROBOT_ANIM',
            WW_COMMAND_LAUNCHER_FLING             : 'WW_COMMAND_LAUNCHER_FLING',
            WW_COMMAND_LAUNCHER_RELOAD            : 'WW_COMMAND_LAUNCHER_RELOAD',
            WW_SENSOR_BUTTON_MAIN                 : 'WW_SENSOR_BUTTON_MAIN',
            WW_SENSOR_BUTTON_1                    : 'WW_SENSOR_BUTTON_1',
            WW_SENSOR_BUTTON_2                    : 'WW_SENSOR_BUTTON_2',
            WW_SENSOR_BUTTON_3                    : 'WW_SENSOR_BUTTON_3',
            WW_SENSOR_HEAD_POSITION_PAN           : 'WW_SENSOR_HEAD_POSITION_PAN',
            WW_SENSOR_HEAD_POSITION_TILT          : 'WW_SENSOR_HEAD_POSITION_TILT',
            WW_SENSOR_BODY_POSE                   : 'WW_SENSOR_BODY_POSE',
            WW_SENSOR_ACCELEROMETER               : 'WW_SENSOR_ACCELEROMETER',
            WW_SENSOR_GYROSCOPE                   : 'WW_SENSOR_GYROSCOPE',
            WW_SENSOR_DISTANCE_FRONT_LEFT_FACING  : 'WW_SENSOR_DISTANCE_FRONT_LEFT_FACING',
            WW_SENSOR_DISTANCE_FRONT_RIGHT_FACING : 'WW_SENSOR_DISTANCE_FRONT_RIGHT_FACING',
            WW_SENSOR_DISTANCE_BACK               : 'WW_SENSOR_DISTANCE_BACK',
            WW_SENSOR_ENCODER_LEFT_WHEEL          : 'WW_SENSOR_ENCODER_LEFT_WHEEL',
            WW_SENSOR_ENCODER_RIGHT_WHEEL         : 'WW_SENSOR_ENCODER_RIGHT_WHEEL',
            WW_SENSOR_MICROPHONE                  : 'WW_SENSOR_MICROPHONE',
            WW_SENSOR_BATTERY                     : 'WW_SENSOR_BATTERY',
            WW_SENSOR_BEACON                      : 'WW_SENSOR_BEACON',
            WW_SENSOR_BEACON_V2                   : 'WW_SENSOR_BEACON_V2',
            WW_SENSOR_PICKED_UP                   : 'WW_SENSOR_PICKED_UP',
            WW_SENSOR_BUMP_STALL                  : 'WW_SENSOR_BUMP_STALL',
            WW_SENSOR_SOUND_PLAYING               : 'WW_SENSOR_SOUND_PLAYING',
            WW_SENSOR_ANIMATION_PLAYING           : 'WW_SENSOR_ANIMATION_PLAYING',
            WW_SENSOR_CHARACTERISTIC_1            : 'WW_SENSOR_CHARACTERISTIC_1',
            WW_SENSOR_CHARACTERISTIC_2            : 'WW_SENSOR_CHARACTERISTIC_2',
            WW_SENSOR_TIMESTAMP                   : 'WW_SENSOR_TIMESTAMP',
        }

    class RobotComponentValues(object):
        WW_COMMAND_VALUE_1                               = "1"
        WW_COMMAND_VALUE_2                               = "2"
        WW_COMMAND_VALUE_3                               = "3"
        WW_COMMAND_VALUE_ACCELERATION_ANGULAR            = "angular_acc_deg_s_s"
        WW_COMMAND_VALUE_ACCELERATION_LINEAR             = "linear_acc_cm_s_s"
        WW_COMMAND_VALUE_AMPLITUDE_CM_PER_S              = "amp_cm_s"
        WW_COMMAND_VALUE_AMPLITUDE_DEG                   = "amp_deg"
        WW_COMMAND_VALUE_ANGLE_DEGREE                    = "degree"
        WW_COMMAND_VALUE_ANGLE_RADIAN                    = "radian"
        WW_COMMAND_VALUE_ANIM_ID                         = "anim"
        WW_COMMAND_VALUE_AVATAR_ENTROPY                  = "entr"
        WW_COMMAND_VALUE_AVATAR_ID                       = "avatar"
        WW_COMMAND_VALUE_AVATAR_PERSIST                  = "s"
        WW_COMMAND_VALUE_AXIS_X                          = "x"
        WW_COMMAND_VALUE_AXIS_Y                          = "y"
        WW_COMMAND_VALUE_BACKUP                          = "bkup"
        WW_COMMAND_VALUE_COLOR_BLUE                      = "b"
        WW_COMMAND_VALUE_COLOR_BRIGHTNESS                = "brightness"
        WW_COMMAND_VALUE_COLOR_GREEN                     = "g"
        WW_COMMAND_VALUE_COLOR_RED                       = "r"
        WW_COMMAND_VALUE_CONTENT_TAGS                    = "tags"
        WW_COMMAND_VALUE_DIRECTION                       = "dir"
        WW_COMMAND_VALUE_DURATION                        = "duration"
        WW_COMMAND_VALUE_EYE_RING_ANIMATION              = "animation"
        WW_COMMAND_VALUE_FILE                            = "file"
        WW_COMMAND_VALUE_FREQUENCY                       = "freq"
        WW_COMMAND_VALUE_HOLD                            = "hold"
        WW_COMMAND_VALUE_ID                              = "id"
        WW_COMMAND_VALUE_LEFT_SPEED                      = "left_cm_s"
        WW_COMMAND_VALUE_MAX_SCALE                       = "max_scl"
        WW_COMMAND_VALUE_MEAN_DEG                        = "avg_deg"
        WW_COMMAND_VALUE_ORDER_INDEX                     = "index"
        WW_COMMAND_VALUE_PARAMETERS                      = "params"
        WW_COMMAND_VALUE_PERCENTAGE                      = "prcnt"   # [-100, 100]
        WW_COMMAND_VALUE_PERIOD_S                        = "prd_s"
        WW_COMMAND_VALUE_PERSISTENT_EYE_BRIGHTNESS       = "peyebright"
        WW_COMMAND_VALUE_PERSISTENT_SOUND_VOLUME         = "pvolume"
        WW_COMMAND_VALUE_PERSONALITY_ANIMATION_ID        = "anim"
        WW_COMMAND_VALUE_PERSONALITY_COLOR_ID            = "color"
        WW_COMMAND_VALUE_PHASE                           = "phase"
        WW_COMMAND_VALUE_PING_ID                         = "pingID"
        WW_COMMAND_VALUE_POSE_DIRECTION                  = "dir"
        WW_COMMAND_VALUE_POSE_EASE                       = "ease"
        WW_COMMAND_VALUE_POSE_MODE                       = "mode"
        WW_COMMAND_VALUE_POSE_WRAP_THETA                 = "wrap_theta"
        WW_COMMAND_VALUE_POWER                           = "pwr"
        WW_COMMAND_VALUE_REPEAT                          = "rpt"
        WW_COMMAND_VALUE_RIGHT_SPEED                     = "right_cm_s"
        WW_COMMAND_VALUE_SET_ROBOT_NAME                  = "name"
        WW_COMMAND_VALUE_SIDE_LENGTH_CM                  = "sidelen_cm"
        WW_COMMAND_VALUE_SIDE_TIME_S                     = "sidetm_s"
        WW_COMMAND_VALUE_SOUND_VOLUME                    = "volume"
        WW_COMMAND_VALUE_SPEED                           = "cm_s"
        WW_COMMAND_VALUE_SPEED_ANGULAR_DEG               = "angular_deg_s"
        WW_COMMAND_VALUE_SPEED_ANGULAR_RAD               = "angular_cm_s"
        WW_COMMAND_VALUE_SPEED_LINEAR                    = "linear_cm_s"
        WW_COMMAND_VALUE_STOP_SOUND                      = "STOPSOUND"
        WW_COMMAND_VALUE_SYNTH_PERC1                     = "perc1"
        WW_COMMAND_VALUE_SYNTH_PERC2                     = "perc2"
        WW_COMMAND_VALUE_SYNTH_TONE1                     = "tone1"
        WW_COMMAND_VALUE_SYNTH_TONE2                     = "tone2"
        WW_COMMAND_VALUE_SYNTH_TONE3                     = "tone3"
        WW_COMMAND_VALUE_SYNTH_TONE4                     = "tone4"
        WW_COMMAND_VALUE_SYNTH_TONE_PREFIX               = "tone"
        WW_COMMAND_VALUE_TAG_AVATAR                      = "avatar"
        WW_COMMAND_VALUE_TAG_EVENT                       = "event"
        WW_COMMAND_VALUE_TAG_MOOD                        = "mood"
        WW_COMMAND_VALUE_TIME                            = "time"
        WW_COMMAND_VALUE_TURN_TIME_S                     = "turntm_s"
        WW_COMMAND_VALUE_TYPE                            = "type"
        WW_COMMAND_VALUE_USE_POSE                        = "pose"
        WW_COMMAND_VALUE_WEIGHT                          = "weight"
        WW_SENSOR_VALUE_ANGLE_DEGREE                     = "degree"
        WW_SENSOR_VALUE_ANGLE_RADIAN                     = "radian"
        WW_SENSOR_VALUE_AXIS_PITCH                       = "p"
        WW_SENSOR_VALUE_AXIS_ROLL                        = "r"
        WW_SENSOR_VALUE_AXIS_X                           = "x"
        WW_SENSOR_VALUE_AXIS_Y                           = "y"
        WW_SENSOR_VALUE_AXIS_YAW                         = "y"
        WW_SENSOR_VALUE_AXIS_Z                           = "z"
        WW_SENSOR_VALUE_BATTERY_CHARGING                 = "chg"
        WW_SENSOR_VALUE_BATTERY_LEVEL                    = "level"
        WW_SENSOR_VALUE_BATTERY_VOLTAGE                  = "volt"
        WW_SENSOR_VALUE_BEACON_DATA                      = "data"
        WW_SENSOR_VALUE_BEACON_DATA_LEFT                 = "dataL"
        WW_SENSOR_VALUE_BEACON_DATA_LENGTH_BITS          = "dataLnBits"
        WW_SENSOR_VALUE_BEACON_DATA_RIGHT                = "dataR"
        WW_SENSOR_VALUE_BEACON_DATA_TYPE                 = "dataType"
        WW_SENSOR_VALUE_BEACON_RECEIVERS                 = "rcvrs"
        WW_SENSOR_VALUE_BEACON_ROBOT_ID                  = "rbtID"
        WW_SENSOR_VALUE_BEACON_ROBOT_TYPE                = "rbtType"
        WW_SENSOR_VALUE_BUTTON_STATE                     = "s"
        WW_SENSOR_VALUE_DATA                             = "data"
        WW_SENSOR_VALUE_DISTANCE                         = "cm"
        WW_SENSOR_VALUE_DISTANCE_SECONDARY               = "cm2"
        WW_SENSOR_VALUE_FLAG                             = "flag"
        WW_SENSOR_VALUE_MIC_AMPLITUDE                    = "amp"
        WW_SENSOR_VALUE_MIC_CLAP_DETECTED                = "clap"
        WW_SENSOR_VALUE_MIC_TRIANGULATION_ANGLE          = "mictdir"
        WW_SENSOR_VALUE_MIC_TRIANGULATION_CONF           = "mictconf"
        WW_SENSOR_VALUE_PING_COUNT                       = "pingCount"
        WW_SENSOR_VALUE_PING_ID                          = "pingID"
        WW_SENSOR_VALUE_POSE_WATERMARK                   = "watermark"
        WW_SENSOR_VALUE_REFLECTANCE                      = "refl"
        WW_SENSOR_VALUE_REFLECTANCE_SECONDARY            = "refl2"
        WW_SENSOR_VALUE_ROBOT_CLACULATED_EVENTS          = "evts"
        WW_SENSOR_VALUE_SOUND_AMPLITUDE                  = "amp"
        WW_SENSOR_VALUE_SPEED                            = "cm/s"
        WW_SENSOR_VALUE_SUBTYPE                          = "type"
        WW_COMMAND_VALUE_LINEAR_VELOCITY_CM_S            = "linear_cm_s"
        WW_COMMAND_VALUE_ANGULAR_VELOCITY_DEG_S          = "angular_deg_s"
        WW_COMMAND_VALUE_LINEAR_ACCELERATION_CM_S_S      = "linear_acc_cm_s_s"
        WW_COMMAND_VALUE_ANGULAR_ACCELERATION_DEG_S_S    = "angular_acc_deg_s_s"
        WW_COMMAND_VALUE_LEDS                            = "LEDs"
        WW_COMMAND_VALUE_MESSAGE                         = "message"

    class WWEyeAnimation:
        WW_EYEANIM_SWIRL      = 0
        WW_EYEANIM_FULL_BLINK = 1
        WW_EYEANIM_WINK       = 2
        WW_EYEANIM_BITMAP     = 0xffff

    class WWPoseMode:
        # interpret the pose as relative to the global coordinate system.
        # this is the most accurate mode.
        WW_POSE_MODE_GLOBAL            = 0

        # interpret the pose as relative to where the robot _should_ be, according to the previous pose command.
        WW_POSE_MODE_RELATIVE_COMMAND  = 1

        # interpret the pose as relative to the robot's current measured position.
        # this is the most common use-case, but can accumulate error over time.
        WW_POSE_MODE_RELATIVE_MEASURED = 2

        # do not actually drive the robot, instead tell the robot to reset its global coordinate to this.
        # typically this is used with x, y, theta = 0.
        WW_POSE_MODE_SET_GLOBAL        = 3

    class WWPoseDirection:
        WW_POSE_DIRECTION_FORWARD      = 0
        WW_POSE_DIRECTION_BACKWARD     = 1
        WW_POSE_DIRECTION_INFERRED     = 2

    class WWRobotAbilities:
        ACCELEROMETER   = 'accelerometer'
        BEACON_EMIT     = 'beacon_emit'
        BEACON_SENSE    = 'beacon_sense'
        BODY_MOVE       = 'body_move'
        DISTANCE_DETECT = 'distance_detect'
        GYROSCOPE       = 'gyroscope'
        HEAD_MOVE       = 'head_move'

        _values         = None

        @staticmethod
        def values():
            _v = WWRobotConstants.WWRobotAbilities._values
            if _v is None:
                WWRobotConstants.WWRobotAbilities._values = {}
                _ra = WWRobotConstants.WWRobotAbilities
                _v = _ra._values
                _rt = WWRobotConstants.RobotType

                cue_dash     = {_rt.WW_ROBOT_DASH, _rt.WW_ROBOT_CUE, }
                cue_dash_dot = {_rt.WW_ROBOT_DASH, _rt.WW_ROBOT_DOT, _rt.WW_ROBOT_CUE, }

                _v[_ra.ACCELEROMETER  ] = cue_dash_dot
                _v[_ra.BODY_MOVE      ] = cue_dash
                _v[_ra.BEACON_SENSE   ] = cue_dash
                _v[_ra.BEACON_EMIT    ] = cue_dash_dot
                _v[_ra.DISTANCE_DETECT] = cue_dash
                _v[_ra.GYROSCOPE      ] = cue_dash
                _v[_ra.HEAD_MOVE      ] = cue_dash

            return _v
