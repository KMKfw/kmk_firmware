# LED (Mono color backlight)
Want your keyboard to shine? Add some lights!
 
## [Keycodes]

|Key                          |Aliases            |Description                 |
|-----------------------------|-------------------|----------------------------|
|`KC.LED_TOG`                 |                   |Toggles LED's               |
|`KC.LED_INC`                 |                   |Increase Brightness         |
|`KC.LED_DEC`                 |                   |Decrease Brightness         |
|`KC.LED_ANI`                 |                   |Increase animation speed    |
|`KC.LED_AND`                 |                   |Decrease animation speed    |
|`KC.LED_MODE_PLAIN`          |`LED_M_P`          |Static LED's                |
|`KC.LED_MODE_BREATHE`        |`LED_M_B`          |Breathing animation         |

## Configuration
|Define                                   |Default      |Description                                     |
|-----------------------------------------|-------------|------------------------------------------------|
|`keyboard.led_config['brightness_step']` |`5`          |The number of steps to change the brightness by |
|`keyboard.led_config['brightness_limit']`|`100`        |The maximum brightness level in percent         |

## Built-in Animation Configuration
|Define                                   |Default      |Description                                                                          |
|-----------------------------------------|-------------|-------------------------------------------------------------------------------------|
|`keyboard.led_config['breath_center']`   |`1.5`    |Used to calculate the curve for the breathing animation. Anywhere from 1.0 - 2.7 is valid|

## Functions

If you want to create your own animations, or for example, change the lighting in a macro, or a layer switch, here are some functions that are available.

|Function                                    |Description                                                                                 |
|--------------------------------------------|--------------------------------------------------------------------------------------------|
|`keyboard.pixels.increase_brightness(step)` |Increases hue by a given step                                                               |
|`keyboard.pixels.decrease_brightness(step)` |Decreases hue by a given step                                                               |
|`keyboard.pixels.set_brightness(percent)`   |Increases saturation by a given step                                                        |

## Direct variable access
|Define                             |Default    |Description                                                                                             |
|-----------------------------------|-----------|--------------------------------------------------------------------------------------------------------|
|`keyboard.led.brightness`          |`0`        |Sets the brightness by percent 0-100                                                                       |
|`keyboard.led.brightness_limit`    |`100`      |Sets the limit of brightness                                                                               |
|`keyboard.led.brightness_step`     |`5`        |Sets the step value to change brightness by                                                                |
|`keyboard.led.animation_mode`      |`static`   |This can be changed to any modes included, or to something custom for user animations. Any string is valid |
|`keyboard.led.animation_speed`     |`1`        |Increases animation speed of most animations. Recommended 1-5, Maximum 10.                                 |

## User animations
User animations can be created as well. An example of a light show would look like this
```python
from kmk.keys import make_key

def start_flicker(*args, **kwargs):
    # Setting mode to user will use the user animation
    keyboard.led.animation_mode = 'user'


def flicker(self):
    # This is the code that is run every cycle that can serve as an animation
    # Refer to the kmk/rgb.py for actual examples of what has been done
    if self.brightness == 0:
        self.brightness = 100
    else:
        self.brightness = 0
    keyboard.led.set_brightness(self.brightness)
    return self


# This is what "gives" your function to KMK so it knows what your animation code is
keyboard.led_config['user_animation'] = flicker

# Makes a key that would start your animation
LS = make_key(on_press=start_flicker())

keymap = [...LS,...]
```

# Troubleshooting
Make sure that your board supports LED backlight by checking for a line with "LED_PIN". If it does not, you can add it to your keymap.

|Define               |Description                                  |
|---------------------|---------------------------------------------|
|`keyboard.led_pin`   |The pin connected to the data pin of the LEDs|

