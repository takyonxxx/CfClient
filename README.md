# Crazyflie PC client for testing and additional improvements
[![Build Status](https://api.travis-ci.org/bitcraze/crazyflie-clients-python.svg)](https://travis-ci.org/bitcraze/crazyflie-clients-python) [![Build status](https://ci.appveyor.com/api/projects/status/u2kejdbc9wrexo31?svg=true)](https://ci.appveyor.com/project/bitcraze/crazyflie-clients-python)


The Crazyflie PC client enables flashing and controlling the Crazyflie.
It implements the user interface and high-level control (for example gamepad handling).
The communication with Crazyflie and the implementation of the CRTP protocol to control the Crazflie is handled by the [cflib](https://github.com/bitcraze/crazyflie-lib-python) project.

For more info see our [documentation](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/).

# Running from source
Linux:
```sudo apt-get install python3 python3-pip python3-pyqt5 python3-pyqt5.qtsvg```</br>

Mac Brew:
```brew install python3 sdl sdl2 sdl_image sdl_mixer sdl_ttf libusb portmidi pyqt5```

Uninstall cfclient if exists with ```pip3 uninstall cfclient``` and install it in development mode by navigating into the repos root folder 

Installing the client in edit mode: ```pip3 install -e .```
or  ```pip3 install -r requirements.txt```

Now you can edit and change codes. </br>
Run source code with  ```./run_cfclient.sh start``` or ```python3 bin/cfclient```

For GoPro ```sudo apt install ffmpeg```
