# WonderPy
This is an alpha-status project to bring realtime control of the WonderWorkshop robots to Python.  
To get the most out of this, you should already have a beginner-level comfort with python and the command-line.
# Project Status
At an "Alpha" release. It's ready to be tried out by folks who are willing to live with a few more rough-edges than one would want, and ideally who can provide constructive criticism.

## Known Issues and To-Do's
* Only works with a single robot.
* Only works with Python2.7.  
  The limiting factor here is getting the AdaFruit BTLE package to run under Python3. There's evidence this is possible.
* Once under Python3, update the concurrency model.
* Flesh-out inline documentation.
* Make the pip installation more standard.
  Currently this requires a manual install of a github-based fork of the AdaFruit package.
* Port to Windows, Linux

# Setup
## Prerequisites
1. MacOS
2. Familiarity with python and command-line tools

## Create a new python virtual environment
1. `virtualenv --python=/usr/bin/python2.7 --no-site-packages venv`
2. `source venv/bin/activate`

## Install dependencies
Unfortunately the AdaFruit BTLE package is not hosted on PyPi, which makes it difficult to automatically install when this package is installed via pip. Additionally, this project requires a fork of that project by WonderWorkshop, which as of this writing has not been merged back into the main project.
1. `pip install git+git://github.com/playi/Adafruit_Python_BluefruitLE@928669a#egg=Adafruit_BluefruitLE`

## Install WonderPy
`pip install WonderPy`

# Getting Started
The steps above install the core library.  
There are many examples of using it separately in the github repository [playi/WonderPyExamples](https://github.com/playi/WonderPyExamples).  
**It is *highly* recommended to look at those examples.**

Additional documentation is in the source code and also in [doc/WonderPy.md](doc/WonderPy.md).

One of the examples is this "hello world" example. Copy this file into "hello_world.py" and run it.

```
from threading import Thread
import time

import WonderPy.core.wwMain
from WonderPy.core.wwConstants import WWRobotConstants
from WonderPy.components.wwMedia import WWMedia


"""
This example shows very basic connecting to a robot and sending some simple commands.
Basic steps:

1. add the imports
2. create a Class (in this case named "MyClass").
3. create a method named "on_connect" which accepts self and a robot parameter.
     eg on_connect(self, robot).
     This will be called when the program connects to a robot.
4. kick things off my passing an instance of your Class to WonderPy.wwMain.start():
     WonderPy.wwMain.start(MyClass())
5. Try it! Your on_connect method should be called.
6. on_connect() itself should not block - ie, it should return control as soon as possible.
     However, on_connect() can launch some asynchronous processes, which can block.
     So do that. In this example we spawn a thread on method thread_hello().
7. In the thread, try out some robot commands!
     * Commands of the flavour "stage_foo()" simply send the command to the robot and return.
         ie, they do not block.
     * Commands of the flavour "do_foo()" send the commands and block until the command completes.
"""


class MyClass(object):

    def on_connect(self, robot):
        """
        Called when we connect to a robot. This method is optional. Do not Block in this method !
        """

        print("Starting a thread for %s." % (robot.name))
        Thread(target=self.thread_hello, args=(robot,)).start()

    def thread_hello(self, robot):
        """
        :param robot: WWRobot
        """

        # dictionary mapping robot types to a few sounds for that robot
        hello_sounds = {
            WWRobotConstants.RobotType.WW_ROBOT_DASH : [WWMedia.WWSound.WWSoundDash.HOWDY,
                                                        WWMedia.WWSound.WWSoundDash.HOWSGOING       ],
            WWRobotConstants.RobotType.WW_ROBOT_DOT  : [WWMedia.WWSound.WWSoundDot .HOWDY,
                                                        WWMedia.WWSound.WWSoundDot .HOLD_ME         ],
            WWRobotConstants.RobotType.WW_ROBOT_CUE  : [WWMedia.WWSound.WWSoundCue .zest_HEYWHSU,
                                                        WWMedia.WWSound.WWSoundCue .charge_BORESTNOC],
        }

        if robot.robot_type not in hello_sounds:
            raise ValueError("unhandled robot type: %s on %s" % (str(robot.robot_type), robot.name))

        for sound_name in hello_sounds[robot.robot_type]:

            print("On %s, setting all RGB lights to white." % (robot.name))
            robot.cmds.RGB.stage_all(1, 1, 1)

            print("On %s, playing '%s'." % (robot.name, sound_name))
            robot.cmds.media.do_audio(sound_name)

            print("On %s, setting all RGB lights to off." % (robot.name))
            robot.cmds.RGB.stage_all(0, 0, 0)

            print("Waiting a little bit.")
            time.sleep(1)

        print("That's all for now.")


# kick off the program !
if __name__ == "__main__":
    WonderPy.core.wwMain.start(MyClass())
```
		
## Robot Connection Options
Upon launching any of the examples, the app will scan for robots for at least 5 and at most 20 seconds.  After scanning, whichever robot had the highest signal strength (RSSI) will be connected to.  This is a reasonable approximation of connecting to the closest robot.

### Connection Options:
```
[--connect-type cue | dot | dash]
  filter for robots of the specified type/s

[--connect-name MY_ROBOT | MY_OTHER_ROBOT | ...]
  filter for robots with the specified name/s
  
[--connect-eager]
  connect as soon as a qualified robot is discovered.  
  do not wait the full scanning period.
  if there are more than one robot with matching criteria,
  the one with the best signal is still selected
  
[--connect-ask]  
  show a list of available robots, and interactively ask for input.
  indicates which has the highest signal strength.
  
``` 

### Connection  Examples:
* Spend 5 seconds looking for all Cue and Dash robots which are named either "sammy" or "sally", and connect to the one with the best signal strength:  
`python demos/roboFun.py --connect-type cue dash --connect-name sammy blippy sally`  

* Connect ASAP to any robot named 'orions robot', no matter what type of robot it is.  
`python demos/roboFun.py --connect-eager --connect-name "orions robot"`  

# Documentation
Documentation is still also in Alpha stage, but some basics of working with the robot are [here](doc/WonderPy.md).

# Contribute
Please check the list of issues and todo's at the [WonderPy repository on github](https://github.com/playi/WonderPy/issues).  
Pull-Requests are welcome.

# Get Help
If there's a specific bug or problem with the API, please check the [outstanding issues](https://github.com/playi/WonderPy/issues) and if it's not already covered, create a new one.  
If you have a more general question such as "how do I..." or "has anyone done ..." or you have a tip you'd like to share, please visit [robotics.stackexchange.com](https://robotics.stackexchange.com) and use the tag **wonderworkshop** .

# Share your work !
Got a great picture or video ?  
Share your Dash, Dot or Cue work on [Twitter](https://twitter.com/WonderWorkshop) or [Instagram](https://www.instagram.com/wonderworkshop/) and tag **@WonderWorkshop** !


