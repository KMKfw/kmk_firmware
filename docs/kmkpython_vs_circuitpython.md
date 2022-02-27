# THIS IS OUT OF DATE. DO NOT USE. ONLY FOR REFERENCE

## Firmware of choice
### KMKPython
KMKPython is a fork of Circuitpython, but with libraries for most extensions 
built in. This saves you from having to get them all and keep them updated 
yourself. There may be other features added in the future that are exclusive to 
KMKPython. For the nice!nano, this is highly recommended, and used in place of 
Circuitpython.  
Notable differences include
- Built in libraries for bluetooth, RGB, and more
- Saves space as builds are optimized for keyboards
- Microcontrollers like the nice!nano will be able to access all features out of
the box.

### Circuitpython
Circuitpython can be installed by following this guide using the guide 
[here](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython). 
It's recommended to run the latest stable version that is at least 5.0 or higher.
Beta versions may work, but expect limited support.
#### Notable differences include
 - Supports more devices
 - Less built in libraries. If using RGB, bluetooth, and more, you will have to 
 add these libraries yourself
 - Some devices such as the nice!nano don't have much free space, so not all 
 features can be installed at the same time
