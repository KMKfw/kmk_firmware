# RGB/Underglow/Neopixel
Want your keyboard to shine? Add some lights!

## Circuitpython
If not running KMKpython, this does require the neopixel library from Adafruit. 
This can be downloaded 
[here](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/blob/6e35cd2b40575a20e2904b096508325cef4a71d3/neopixel.py).
It is part of the [Adafruit CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle).
Simply put this in the "root" of your circuitpython device. If unsure, it's the folder with main.py in it, and should be the first folder you see when you open the device.

Currently we support the following addressable LEDs:

 * WS2811, WS2812, WS2812B, WS2812C, etc.
 * SK6812, SK6812MINI, SK6805

### Color Selection

KMK uses [Hue, Saturation, and Value](https://en.wikipedia.org/wiki/HSL_and_HSV) to select colors rather than RGB. The color wheel below demonstrates how this works.

Changing the **Hue** cycles around the circle.
Changing the **Saturation** moves between the inner and outer sections of the wheel, affecting the intensity of the color.
Changing the **Value** sets the overall brightness.

## Enabling the extension
The only required values that you need to give the RGB extension would be the pixel pin, and the number of pixels/LED's. If using a split keyboard, this number is per side, and not the total of both sides.
```python
from kmk.extensions.RGB import RGB
from kb import rgb_pixel_pin  # This can be imported or defined manually

rgb_ext = RGB(pixel_pin=rgb_pixel_pin, num_pixels=27)
keyboard.extensions.append(rgb_ext)
```

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

```python
from kmk.extensions.rgb import AnimationModes
rgb_ext = RGB(pixel_pin=rgb_pixel_pin,
        num_pixels=27
        num_pixels=0,
        val_limit=100,
        hue_default=0,
        sat_default=100,
        rgb_order=(1, 0, 2),  # GRB WS2812
        val_default=100,
        hue_step=5,
        sat_step=5,
        val_step=5,
        animation_speed=1,
        breathe_center=1,  # 1.0-2.7
        knight_effect_length=3,
        animation_mode=AnimationModes.STATIC,
        reverse_animation=False,
        )
```

## Hardware Modification

To add RGB LED's to boards that don't support them directly, you will have to
add a 3 wires. The power wire will run on 3.3v or 5v (depending on the LED),
ground, and data pins will need added to an unused pin on your microcontroller
unless your keyboard has specific solder points for them. With those 3 wires
connected, set the `pixel_pin` as described above, and you are ready to use your
RGB LED's/Neopixels.

## Troubleshooting
### Incorrect colors
If your colors are incorrect, check the pixel order of your specific LED's. Here are some common ones.
 * WS2811, WS2812, WS2812B, WS2812C are all GRB (1, 0, 2)
 * SK6812, SK6812MINI, SK6805 are all GRB (1, 0, 2)
 * Neopixels will vary depending on which one you buy. It will be listed on the product page.

### Lights don't turn on

Make sure that your board supports LED backlight by checking for a line with
`PIXEL_PIN`. If it does not, you can add it to your keymap.  If you added the
LED's yourself, you will also need to set `num_pixels` to the number of
installed LED's in total.
