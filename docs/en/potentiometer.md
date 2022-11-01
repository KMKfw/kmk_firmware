# Potentiometer module
Do you want to add joystick sor faders to your keyboard?

The potentiometer module reads analog signals from you ADC pins and gives you a value in 7 bit base.

## Enabling the extension
Enabling Potentiometer gives you access to the following keycodes and can simply be
added to the modules list.

```python
from kmk.modules.potentiometer import PotentiometerHandler
potentiometer = PotentiometerHandler()

keyboard.modules.append(potentiometer)
```


## How to use
Here is all you need to use this module in your `main.py` / `code.py` file.

###### 1. Load the module: import the potentiometer handler and add it to keyboard modules.

```python
from kmk.modules.potentiometer import PotentiometerHandler
potentiometer = PotentiometerHandler()
keyboard.modules.append(potentiometer)
```

###### 2. Define the pins for each potentiometer: `pin_a` for the signal pin and `defname` for the name of the controlling defenition. If you want to invert the direction of the potentiometer, set the 3rd (optional) parameter `is_inverted` to `True`.

```python
potentiometer.pins = (
    (board."pin_a", "defname", "is_inverted")
)
```

 Example:
```python
# Regular GPIO potentiometer
potentiometer.pins = (
    # regular direction potentiometer
    (board.A0, potentiometer_1_handler),
    # reversed direction potentiometer
    (board.A1, potentiometer_2_handler, False),
)
```

###### 3. Define the mapping of keys to be called.

here we convert the incoming base values into a value 0-127 for ease of use.
This example is for a joystick mapped to WASD with a deadzone in the center. The exact deadzone values might vary depending on the potentiometers used.
    *Note: this uses `keyboard.add_key` and `keyboard.remove_key` which could be considered legacy.*

```python
def potentiometer_1_handler(state):
    joy1 = int((state.position / 127) * 127)
    if joy1 >= 0 and joy1 <= 56:
        keyboard.add_key(KC.S)
    if joy1 >= 65 and joy1 <= 127:
        keyboard.add_key(KC.W)
    if joy1 >= 57 and joy1 <= 64:
        keyboard.remove_key(KC.S)
        keyboard.remove_key(KC.W)

def potentiometer_2_handler(state):
    joy2 = int((state.position / 127) * 127)
    if joy2 >= 0 and joy2 <= 58:
        keyboard.add_key(KC.A)
    if joy2 >= 67 and joy2 <= 127:
        keyboard.add_key(KC.D)
    if joy2 >= 59 and joy2 <= 66:
        keyboard.remove_key(KC.A)
        keyboard.remove_key(KC.D)
```

## Other examples

###### Computer volume

You can use a potentiometer to control the system volume easily. Here an example from [ZFR_KBD's RP2.65-F](https://github.com/KMKfw/kmk_firmware/blob/master/user_keymaps/ZFR_KBD/RP2.65-F.py)

```python
def set_sys_vol(state):
    # convert to 0-100
    new_pos = int((state.position / 127) * 64)
    level = level_lut[new_pos]
    # print(f"new vol level: {level}")
    # print(f"last: {keyboard.last_level}")

    # check if uninitialized
    if keyboard.last_level == -1:
        keyboard.last_level = level
        return

    level_diff = abs(keyboard.last_level - level)
    if level_diff > 0:
        # set volume to new level
        # vol_direction = "unknown"
        if level > keyboard.last_level:
            # vol_direction = "up"
            cmd = KC.VOLU
        else:
            # vol_direction = "down"
            cmd = KC.VOLD

        # print(f"Setting system volume {vol_direction} by {level_diff} to reach {level}")
        for i in range(int(level_diff / level_inc_step)):
            hid_report = keyboard._hid_helper.create_report([cmd])
            hid_report.send()
            hid_report.clear_all()
            hid_report.send()

        keyboard.last_level = level
    return

def potentiometer_1_handler(state):
    set_sys_vol(state)
```

###### LED brightness

You can also use a potentiometer to control the LED brightness of your keyboard. Another example from [ZFR_KBD's RP2.65-F](https://github.com/KMKfw/kmk_firmware/blob/master/user_keymaps/ZFR_KBD/RP2.65-F.py)

```python
def get_kb_rgb_obj(keyboard):
    rgb = None
    for ext in keyboard.extensions:
        if type(ext) is RGB:
            rgb = ext
            break
    return rgb

def set_led_brightness(state):
    rgb = get_kb_rgb_obj(keyboard)
    if rgb is None:
        return

    rgb.val = int((state.position / 127) * rgb.val_limit)
    rgb._do_update()
    return

def potentiometer_3_handler(state):
    set_led_brightness(state)
```