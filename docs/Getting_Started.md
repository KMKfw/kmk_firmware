# Getting Started
 
 ## Microcontrollers
 KMK will run on most microcontrollers supported by [Circuitpython](https://circuitpython.org/downloads). Our recommended microcontrollers are found [here](Officially_Supported_Microcontrollers.md)
 
 ## Firmware
 ### Circuitpython
Circuitpython is what KMK will run on top of. Make sure that Circuitpython is installed on your 
device using the guide [here](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython). 
It's recommended to run the latest stable version that is at least 5.0 or higher. Beta versions may work, but expect limited support.
 
 ### KMKPython
KMKPython is a fork of Circuitpython, but with libraries for most extensions built in. This saves you from having to get them all 
and keep them updated yourself. There may be other features added in the future that are exclusive to KMKPython.
 
 ## Getting KMK
 You can always find the latest releases on our CDN, in [compiled and optimized](https://cdn.kmkfw.io/kmk-latest.zip) and 
 [raw, hackable text file](https://cdn.kmkfw.io/kmk-latest.unoptimized.zip) forms. These follow the `master` branch here on GitHub. 
 Just get the KMK folder and drop this directly in the CIRCUITPYTHON directory (not in a sub folder). Make sure to extract the zip, 
 and put the `kmk` folder on the root of the CIRCUITPY drive on the microcontroller

## Turning a controller into a keyboard
### Supported keyboards
If your keyboard and microcontroller are officially supported, it's as easy as visiting the page for your files, and dropping them 
on the root of the "flash drive". Those pages can be found [here](https://github.com/KMKfw/boards). You will need the `kb.py` and `main.py`. More advanced instructions
can be found [here](config_and_keymap.md)

### Porting a keyboard
If you are porting a board to KMK, check the page [here](porting_to_kmk.md). 

### Handwired Keyboard
If you are doing a hand wire, check [here](handwiring.md)

## Additional features
Want to have fun features such as RGB, split keyboards and more? Check out what extensions can do [here](extensions.md)

## Debugging
Debugging help can be found [here](debugging.md)

## Additional help and support
 If you need support with KMK or just want to say hi, find us in [#kmkfw:klar.sh on Matrix](https://matrix.to/#/#kmkfw:klar.sh).  This channel is bridged to Discord [here](https://discordapp.com/widget?id=493256121075761173&theme=dark) for convenience.
