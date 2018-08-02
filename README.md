# WonderPy
[![Build status](https://travis-ci.org/playi/WonderPy.svg?master)](https://travis-ci.org/playi)

This is an alpha-status project to bring realtime control of the WonderWorkshop robots to Python.  
To get the most out of this, you should already have a beginner-level comfort with python and the command-line.
# Project Status
At an "Alpha" release. It's ready to be tried out by folks who are willing to live with a few more rough-edges than one would want, and ideally who can provide constructive criticism.  

Please see the ["Issues" in github](https://github.com/playi/WonderPy/issues) for an up-to-date list of known bugs and to-do items.  

# Setup
## Prerequisites
1. MacOS
2. Familiarity with python and command-line tools

## Create a new python virtual environment
1. `virtualenv --python=/usr/bin/python2.7 --no-site-packages venv`
2. `source venv/bin/activate`

## Install dependencies
1. XCode Command Line Tools must be installed. `xcode-select --install` should work.

You may need to install XCode from the App Store, then download and install Command Line Tools from the Apple Developer site (https://developer.apple.com/download/more/). There, you can search for Command Line Tools, find the appropriate file based on your version of OS X and XCode, download and install Command Line Tools.

Once installed, you may need to uninstall/reinstall Python 2.x.

```
$ rm -rf ~/.pyenv/versions/2.7.14
$ pyenv install 2.7.14
```

> Note: your setup might be slightly different if you have a different version or are using virtualenv.

2. Unfortunately, the AdaFruit BTLE package is not hosted on PyPi, which makes it difficult to automatically install when this package is installed via pip. Additionally, this project requires a fork of that project by WonderWorkshop, which as of this writing has not been merged back into the main project.

`pip install git+git://github.com/playi/Adafruit_Python_BluefruitLE@928669a#egg=Adafruit_BluefruitLE`

## Install WonderPy
`pip install WonderPy`

# Documentation
Documentation is still also in Alpha stage.

* [WonderPy readme](https://github.com/playi/WonderPy/blob/master/README.md)

* [WonderPy Robot Reference Manual](https://github.com/playi/WonderPy/blob/master/doc/WonderPy.md)

* [Tutorials and other examples](https://github.com/playi/WonderPyExamples)

# Getting Started
The steps above install the core library.  
There are many examples of using it separately in the github repository [playi/WonderPyExamples](https://github.com/playi/WonderPyExamples).  
**It is *highly* recommended to look at those examples.**

To test basic functionality, run these at the command-line, inside your fresh virtualenv:  

download the "01\_hello\_world.py" tutorial example:  
```curl -o 01_hello_world.py https://raw.githubusercontent.com/playi/WonderPyExamples/master/tutorial/01_hello_world.py```  

run it:  
```python 01_hello_world.py```

It should connect to any nearby robot and say hello !

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

# Known Issues and To-Do's
Please see the ["Issues" in github](https://github.com/playi/WonderPy/issues) for an up-to-date list of known bugs and to-do items.  
As of this writing, the open issues are:

* Only works with a single robot.
* Only works with Python2.7.  
  The limiting factor here is getting the AdaFruit BTLE package to run under Python3. There's evidence this is possible.
* Once under Python3, update the concurrency model.
* Flesh-out inline documentation.
* Make the pip installation more standard.
  Currently this requires a manual install of a github-based fork of the AdaFruit package.
* Port to Windows, Linux

# Contribute
Pull requests are welcome!  
Please check the list of issues and todo's at the [WonderPy repository on github](https://github.com/playi/WonderPy/issues).  

Additional examples in the [WonderPyExamples repository](https://github.com/WonderPyExamples) would also be great:

* Integrations with other cool packages
* IoT integrations
* Demos with the Sketch Kit accessory

Feature requests for the API should be sent as [new Issues in github](https://github.com/playi/WonderPy/issues).  

# Get Help
### Report Bugs
If there's a specific bug or problem with the API, please check the [outstanding issues in github](https://github.com/playi/WonderPy/issues) and if it's not already covered, create a new one.  

### Ask for Advice
If you have a more general question such as "how would I approach doing .." or you have a tip you'd like to share, please visit [stackoverflow](https://stackoverflow.com/) and be sure to tag your post with **wonderworkshop**.

### Request Features
Feature requests for the API should be sent as [new Issues in github](https://github.com/playi/WonderPy/issues).  


# Sharing your work ?
Made something cool ? We'd love to see it !  
Send your photos, videos, and links to developers@makewonder.com .

( Note, we can't promise a reply to all emails )

