#Bluetooth
Tired of the wires cluttering your desk? This is what you are looking for then!
This does require the Adafruit_CircuitPython_BLE library from Adafruit. This can be downloaded [here](https://github.com/adafruit/Adafruit_CircuitPython_BLE).
It is part of the [Adafruit CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle). Just drop the `adafruit_ble`

Simply put the `adafruit_ble` folder in the "root" of your circuitpython device. If unsure, it's the folder with main.py in it, and should be the first folder you see when you open the device.

## Enabling Bluetooth
To enable the bluetooth to run at boot simply add it to keyboard.go(). It will show up as `KMK Keyboard`
```python
if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.BLE)
```

## Naming the keyboard
If you want to give your keyboard a name, simply change the name like this.
```python
if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.BLE, ble_name='My Name Here')
```

## Split keyboards
If you want to connect the parts of the keyboard with bluetooth, see [this](https://github.com/KMKfw/kmk_firmware/blob/master/docs/split_keyboards.md)

## [Keycodes]

|Key                          |Aliases            |Description                       |
|-----------------------------|-------------------|----------------------------------|
|`KC.BT_CLEAR_BONDS`          |`KC.BT_CLR`        |Clears all stored bondings        |
|`KC.BT_NEXT_CONN`            |`KC.BT_NXT`        |Selects the next BT connection    |
|`KC.BT_PREV_CONN`            |`KC.BT_PRV`        |Selects the previous BT connection|
