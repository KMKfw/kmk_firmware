# BLE HID
Bluetooth connections help clean up the wire mess!

## CircuitPython
If not running KMKPython, this does require the [adafruit_ble library from Adafruit](https://github.com/adafruit/Adafruit_CircuitPython_BLE/tree/master/adafruit_ble).
It's part of the Adafruit CircuitPython Bundle, which can be downloaded [here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/tag/20220715).
Get the bundle version that corresponds to the CircuitPython version installed on your device. Unzip the bundle and open the "lib" folder to locate the "adafruit_ble" library. Selectively copy that library (the entire "adafruit_ble" folder) and place it into the "lib" folder located at the root of your CIRCUITPY device. If unsure, the root is the main device storage folder where your main.py (or code.py) file is located. The "lib" folder should have been created when you installed CircuitPython. If not, just create one to place the ble library.

## Enabling BLE

To enable BLE hid, change the keyboard.go(). By default, the advertised name
will be the name of the "flash drive". By default this is CIRCUITPY

```python
from kmk.hid import HIDModes

if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.BLE)
```

## Changing the advertise name
There are two ways to change the advertising name. The first would be to
[change the name of the drive](https://learn.adafruit.com/welcome-to-circuitpython/renaming-circuitpy).
The second would be to change the keyboard.go() like this.

```python
if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.BLE, ble_name='KMKKeyboard')
```
