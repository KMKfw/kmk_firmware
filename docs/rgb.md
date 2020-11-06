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

## Enabling the extention
The only required values that you need to give the RGB extention would be the pixel pin, and the number of pixels/LED's. If using a split keyboard, this number is per side, and not the total of both sides.
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
All of these values can be set by default for when the keyboard boots.
```python
from kmk.extentions.rgb import AnimationModes
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

To add RGB LED's to boards that don't support them directly, you will have to add a 3 wires. The power wire will run on 3.3v or 5v (depending on the LED),
ground, and data pins will need added to an unused pin on your microcontroller unless your keyboard has specific solder points for them. With those 3 wires
connected, set the pixel_pin as described above, and you are ready to use your RGB LED's/Neopixels.

## Troubleshooting
### Incorrect colors
If your colors are incorrect, check the pixel order of your specific LED's. Here are some common ones.
 * WS2811, WS2812, WS2812B, WS2812C are all GRB (1, 0, 2)
 * SK6812, SK6812MINI, SK6805 are all GRB (1, 0, 2)
 * Neopixels will vary depending on which one you buy. It will be listed on the product page.
 
