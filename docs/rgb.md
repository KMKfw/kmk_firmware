# RGB/Underglow/Neopixel
Want your keyboard to shine? Add some lights!
This does require the neopixel library from Adafruit. This can be downloaded [here](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/blob/6e35cd2b40575a20e2904b096508325cef4a71d3/neopixel.py).
It is part of the [Adafruit CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle).

Simply put this in the "root" of your circuitpython device. If unsure, it's the folder with main.py in it, and should be the first folder you see when you open the device.

Currently we support the following addressable LEDs:

 * WS2811, WS2812, WS2812B, WS2812C, etc.
 * SK6812, SK6812MINI, SK6805
 * All neopixels
 
### Color Selection

KMK uses [Hue, Saturation, and Value](https://en.wikipedia.org/wiki/HSL_and_HSV) to select colors rather than RGB. The color wheel below demonstrates how this works.

Changing the **Hue** cycles around the circle.
Changing the **Saturation** moves between the inner and outer sections of the wheel, affecting the intensity of the color.
Changing the **Value** sets the overall brightness.

## [Keycodes]

|Key                          |Aliases            |Description                 |
|-----------------------------|-------------------|----------------------------|
|`KC.RGB_TOG`                 |                   |Toggles RGB                 |
|`KC.RGB_HUI`                 |                   |Increase Hue                |
|`KC.RGB_HUD`                 |                   |Decrease Hue                |
|`KC.RGB_SAI`                 |                   |Increase Saturation         |
|`KC.RGB_SAD`                 |                   |Decrease Saturation         |
|`KC.RGB_VAI`                 |                   |Increase Value              |
|`KC.RGB_VAD`                 |                   |Decrease Value              |
|`KC.RGB_ANI`                 |                   |Increase animation speed    |
|`KC.RGB_AND`                 |                   |Decrease animation speed    |
|`KC.RGB_MODE_PLAIN`          |`RGB_M_P`          |Static RGB                  |
|`KC.RGB_MODE_BREATHE`        |`RGB_M_B`          |Breathing animation         |
|`KC.RGB_MODE_RAINBOW`        |`RGB_M_R`          |Rainbow animation           |
|`KC.RGB_MODE_BREATHE_RAINBOW`|`RGB_M_BR`         |Breathing rainbow animation |
|`KC.RGB_MODE_KNIGHT`         |`RGB_M_K`          |Knightrider animation       |
|`KC.RGB_MODE_SWIRL`          |`RGB_M_S`          |Swirl animation             |

## Configuration
|Define                               |Default      |Description                                                                  |
|-------------------------------------|-------------|-----------------------------------------------------------------------------|
|`keyboard.pixel_pin` | |The pin connected to the data pin of the LEDs|
|`keyboard.num_pixels`| |The number of LEDs connected                 |
|`keyboard.rgb_config['rgb_order']`   |`(1, 0, 2)`  |The order of the pixels R G B, and optionally white. Example(1, 0, 2, 3)     |
|`keyboard.rgb_config['hue_step']`    |`10`         |The number of steps to cycle through the hue by                              |
|`keyboard.rgb_config['sat_step']`    |`17`         |The number of steps to change the saturation by                              |
|`keyboard.rgb_config['val_step']`    |`17`         |The number of steps to change the brightness by                              |
|`keyboard.rgb_config['hue_default']` |`0`          |The default hue when the keyboard boots                                      |
|`keyboard.rgb_config['sat_default']` |`100`        |The default saturation when the keyboard boots                               |
|`keyboard.rgb_config['val_default']` |`100`        |The default value (brightness) when the keyboard boots                       |
|`keyboard.rgb_config['val_limit']`   |`255`        |The maximum brightness level                                                 |

## Built-in Animation Configuration
|Define                                        |Default      |Description                                                                          |
|----------------------------------------------|-------------|-------------------------------------------------------------------------------------|
|`keyboard.rgb_config['breathe_center']`       |`1.5`    |Used to calculate the curve for the breathing animation. Anywhere from 1.0 - 2.7 is valid|
|`keyboard.rgb_config['knight_effect_length']` |`4`      |The number of LEDs to light up for the "Knight" animation                                |

## Functions

If you want to create your own animations, or for example, change the lighting in a macro, or a layer switch, here are some functions that are available.

|Function                                          |Description                                                                                 |
|--------------------------------------------------|--------------------------------------------------------------------------------------------|
|`keyboard.pixels.set_hsv_fill(hue, sat, val)`     |Fills all LED's with HSV values                                                             |
|`keyboard.pixels.set_hsv(hue, sat, val, index)`   |Sets a single LED with HSV value                                                            |
|`keyboard.pixels.set_rgb_fill((r, g, b))`         |Fills all LED's with RGB(W) values                                                          |
|`keyboard.pixels.set_rgb((r, g, b), index)`       |Set's a single LED with RGB(W) values                                                       |
|`keyboard.pixels.disable_auto_write(bool)`        |When True, disables showing changes. Good for setting multiple LED's before a visible update|
|`keyboard.pixels.increase_hue(step)`              |Increases hue by a given step                                                               |
|`keyboard.pixels.decrease_hue(step)`              |Decreases hue by a given step                                                               |
|`keyboard.pixels.increase_sat(step)`              |Increases saturation by a given step                                                        |
|`keyboard.pixels.decrease_sat(step)`              |Decreases saturation by a given step                                                        |
|`keyboard.pixels.increase_val(step)`              |Increases value (brightness) by a given step                                                |
|`keyboard.pixels.decrease_val(step)`              |Decreases value (brightness) by a given step                                                |
|`keyboard.pixels.increase_ani()`                  |Increases animation speed by 1. Maximum 10                                                  |
|`keyboard.pixels.decrease_ani()`                  |Decreases animation speed by 1. Minimum 10                                                  |
|`keyboard.pixels.off()`                           |Turns all LED's off                                                                         |
|`keyboard.pixels.show()`                          |Displays all stored configuration for LED's. Useful with disable_auto_write explained below |
|`keyboard.pixels.time_ms()`                       |Returns a time in ms since the board has booted. Useful for start/stop timers               |

## Direct variable access
|Define                             |Default    |Description                                                                                                |
|-----------------------------------|-----------|-----------------------------------------------------------------------------------------------------------|
|`keyboard.pixels.hue`              |`0`        |Sets the hue from 0-360                                                                                    |
|`keyboard.pixels.sat`              |`100`      |Sets the saturation from 0-100                                                                             |
|`keyboard.pixels.val`              |`80`       |Sets the brightness from 1-255                                                                             |
|`keyboard.pixels.reverse_animation`|`False`    |If true, some animations will run in reverse. Can be safely used in user animations                        |
|`keyboard.pixels.animation_mode`   |`static`   |This can be changed to any modes included, or to something custom for user animations. Any string is valid |
|`keyboard.pixels.animation_speed`  |`1`        |Increases animation speed of most animations. Recommended 1-5, Maximum 10.                                 |


## Hardware Modification

To add RGB LED's to boards that don't support them directly, you will have to add a 3 wires. The power wire will run on 3.3v or 5v (depending on the LED),
ground, and data pins will need added to an unused pin on your microcontroller unless your keyboard has specific solder points for them. With those 3 wires
connected, set the pixel_pin as described above, and you are ready to use your RGB LED's/Neopixels.

## ADVANCED USAGE
If you wish to interact with these as you would normal LED's and do not want help from KMK, you can disable all helper functions from working and access the
neopixel object directly like this.
```python
keyboard.pixels.disable_auto_write = True
keyboard.pixels.neopixel() # <-- This is the neopixel object
```

## User animations
User animations can be created as well. An example of a light show would look like this
```python
from kmk.keys import make_key

def start_light_show(*args, **kwargs):
    # Setting mode to user will use the user animation
    keyboard.pixels.animation_mode = 'user'


def light_show(self):
    # This is the code that is run every cycle that can serve as an animation
    # Refer to the kmk/rgb.py for actual examples of what has been done
    self.hue = (self.hue + 35) % 360
    keyboard.pixels.set_hsv_fill(self.hue, self.sat, self.val)
    return self


# This is what "gives" your function to KMK so it knows what your animation code is
keyboard.rgb_config['user_animation'] = light_show

# Makes a key that would start your animation
LS = make_key(on_press=start_light_show)

keymap = [...LS,...]
```

## Troubleshooting
### Incorrect colors
If your colors are incorrect, check the pixel order of your specific LED's. Here are some common ones.
 * WS2811, WS2812, WS2812B, WS2812C are all GRB (1, 0, 2)
 * SK6812, SK6812MINI, SK6805 are all GRB (1, 0, 2)
 * Neopixels will vary depending on which one you buy. It will be listed on the product page.# Troubleshooting
 
### Lights don't turn on
Make sure that your board supports LED backlight by checking for a line with "PIXEL_PIN". If it does not, you can add it to your keymap.
If you added the LED's yourself, you will also need to set num_pixels to the number of installed LED's in total.
