# Crazyflie PC client for testing and additional improvements
[![Build Status](https://api.travis-ci.org/bitcraze/crazyflie-clients-python.svg)](https://travis-ci.org/bitcraze/crazyflie-clients-python) [![Build status](https://ci.appveyor.com/api/projects/status/u2kejdbc9wrexo31?svg=true)](https://ci.appveyor.com/project/bitcraze/crazyflie-clients-python)


The Crazyflie PC client enables flashing and controlling the Crazyflie.
It implements the user interface and high-level control (for example gamepad handling).
The communication with Crazyflie and the implementation of the CRTP protocol to control the Crazflie is handled by the [cflib](https://github.com/bitcraze/crazyflie-lib-python) project.

For more info see our [documentation](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/).

# Running from source

Uninstall cfclient if exists with ```python3 -m pip uninstall cfclient``` and install it in development mode by navigating into the repos root folder and installing the client in edit mode: ```python3 -m pip install -e .```
or  ```pip3 install -r requirements.txt```
Now you can edit and change codes. 
Run source with  ```./run_cfclient.sh start``` or ```python3 bin/cfclient```


