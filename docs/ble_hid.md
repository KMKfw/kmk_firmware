# BLE HID
Bluetooth connections help clean up the wire mess!

## Circuitpython
If not running KMKpython, this does require the adafruit_ble library from Adafruit.
This can be downloaded
[here](https://github.com/adafruit/Adafruit_CircuitPython_BLE/tree/master/adafruit_ble).
It is part of the [Adafruit CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle).
Simply put this in the "root" of your circuitpython device. If unsure, it's the folder with main.py in it, and should be the first folder you see when you open the device.

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
[change the name of the drive](https://learn.adafruit.com/welcome-to-circuitpython/the-circuitpy-drive).
The second would be to change the keyboard.go() like this.

```python
if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.BLE, ble_name='KMKeyboard')
```


