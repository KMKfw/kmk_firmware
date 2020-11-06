# Getting Started
 
 ## Microcontrollers
 KMK will run on most microcontrollers supported by
 [Circuitpython](https://circuitpython.org/downloads). Our recommended
 microcontrollers are found [here](Officially_Supported_Microcontrollers.md)
 
## Firmware
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
 
## Getting KMK
You can always find the latest releases on our CDN, in 
[compiled and optimized](https://cdn.kmkfw.io/kmk-latest.zip) and 
[raw, hackable text file](https://cdn.kmkfw.io/kmk-latest.unoptimized.zip) 
forms. These follow the `master` branch here on GitHub. Just get the KMK folder
and drop this directly in the CIRCUITPYTHON directory (not in a sub folder).
Make sure to extract the zip, and put the `kmk` folder on the root of the
CIRCUITPY drive on the microcontroller

## Turning a controller into a keyboard
### Supported keyboards
If your keyboard and microcontroller are officially supported, simply visit the 
page for your files, and dropping them on the root of the "flash drive". Those 
pages can be found [here](https://github.com/KMKfw/boards). You will need the 
`kb.py` and `main.py`. More advanced instructions can be found 
[here](config_and_keymap.md). If using Curcuitpython and NOT KMKPython, you will
also need [boot.py](https://github.com/KMKfw/kmk_firmware/blob/master/boot.py)

### Porting a keyboard
If you are porting a board to KMK, check the page [here](porting_to_kmk.md). 

### Handwired Keyboard
If you are doing a hand wire, check [here](handwiring.md)

## Additional features
Want to have fun features such as RGB, split keyboards and more? Check out what 
extensions can do [here](extensions.md)

## Debugging
Debugging help can be found [here](debugging.md)

## Additional help and support
If you need support with KMK or just want to say hi, find us in 
[#kmkfw:klar.sh on Matrix](https://matrix.to/#/#kmkfw:klar.sh).  This channel is 
bridged to Discord [here](https://discordapp.com/widget?id=493256121075761173&theme=dark) 
for convenience. If you ask for help on chat or open a bug report, if possible 
please give us your commit SHA, found by running 
`from kmk.consts import KMK_RELEASE;  print(KMK_RELEASE)` in the REPL on your 
controller.
