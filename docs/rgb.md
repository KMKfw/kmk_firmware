# RGB/Underglow/Neopixel
Want your keyboard to shine? Add some lights!
This does require the neopixel library from Adafruit. This can be downloaded here https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/blob/master/neopixel.py

Simply put this in the "root" of your circuitpython device. If unsure, it's the folder with main.py in it, and should be the first folder you see when you open the device.

Currently we support the following addressable LEDs:

 * WS2811, WS2812, WS2812B, WS2812C, etc.
 * SK6812, SK6812MINI, SK6805
 * All neopixels
 
## Usage
At minimum you will need to make sure that these are set in either your keymap ip importing an MCU directly, or it should be included in the predefined boards if they support them.

|Define               |Description                                  |
|---------------------|---------------------------------------------|
|`keyboard.pixel_pin` |The pin connected to the data pin of the LEDs|
|`keyboard.num_pixels`|The number of LEDs connected                 |

Then you should be able to use the keycodes below to change the RGB lighting to your liking.

### Color Selection

KMK uses [Hue, Saturation, and Value](https://en.wikipedia.org/wiki/HSL_and_HSV) to select colors rather than RGB. The color wheel below demonstrates how this works.

<img src="gitbook/images/color-wheel.svg" alt="HSV Color Wheel" width="250"/>

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
|`KC.RGB_MODE_PLAIN`          |`RGB_M_P`          |Static RGB                  |
|`KC.RGB_MODE_BREATHE`        |`RGB_M_B`          |Breathing animation         |
|`KC.RGB_MODE_RAINBOW`        |`RGB_M_R`          |Rainbow animation           |
|`KC.RGB_MODE_BREATHE_RAINBOW`|`RGB_M_BR`         |Breathing rainbow animation |
|`KC.RGB_MODE_KNIGHT`         |`RGB_M_K`          |Knightrider animation       |

## Configuration
|Define               |Default      |Description                                                                  |
|---------------------|-------------|-----------------------------------------------------------------------------|
|`keyboard.hue_step`  |`10`         |The number of steps to cycle through the hue by                              |
|`keyboard.sat_step`  |`17`         |The number of steps to increment the saturation by                           |
|`keyboard.val_step`  |`17`         |The number of steps to increment the brightness by                           |
|`keyboard.val_limit` |`255`        |The maximum brightness level                                                 |

## Functions

If you want to create your own animations, or for example, change the lighting in a macro, or a layer switch, here are some functions that are available.

|Function                                          |Description                                                                                 |
|--------------------------------------------------|--------------------------------------------------------------------------------------------|
|`keyboard.pixels.set_hsv_fill(hue, sat, val)`     |Fills all LED's with HSV values                                                             |
|`keyboard.pixels.set_hsv(hue, sat, val, index)`   |Sets a single LED with HSV value                                                            |
|`keyboard.pixels.set_rgb_fill((r, g, b))`         |Fills all LED's with RGB(W) values                                                          |
|`keyboard.pixels.set_rgb((r, g, b), index)`       |Set's a single LED with RGB(W) values                                                       |
|`keyboard.pixels.increase_hue(step)`              |Increases hue by a given step                                                               |
|`keyboard.pixels.decrease_hue(step)`              |Decreases hue by a given step                                                               |
|`keyboard.pixels.increase_sat(step)`              |Increases saturation by a given step                                                        |
|`keyboard.pixels.decrease_sat(step)`              |Decreases saturation by a given step                                                        |
|`keyboard.pixels.increase_val(step)`              |Increases value (brightness) by a given step                                                |
|`keyboard.pixels.decrease_val(step)`              |Decreases value (brightness) by a given step                                                |
|`keyboard.pixels.off()`                           |Turns all LED's off                                                                         |
|`keyboard.pixels.show()`                          |Displays all stored configuration for LED's. Useful with disable_auto_write explained below |
|`keyboard.pixels.time_ms()`                       |Returns a time in ms since the board has booted. Useful for start/stop timers               |

Other settings that are useful that can be changed.
## Configuration
|Define                        |Default      |Description                                                                                              |
|------------------------------|-------------|---------------------------------------------------------------------------------------------------------|
|`keyboard.hue`                |`0`        |Sets the hue from 0-360                                                                                    |
|`keyboard.sat`                |`100`      |Sets the saturation from 0-100                                                                             |
|`keyboard.val`                |`80`       |Sets the brightness from 1-255                                                                             |
|`keyboard.disable_auto_write` |`False`    |When True, disables showing changes. Good for setting multiple LED's before a visible update               |
|`keyboard.reverse_animation`  |`False`    |If true, some animations will run in reverse. Can be safely used in user animations                        |
|`keyboard.animation_mode`     |`static`   |This can be changed to any modes included, or to something custom for user animations. Any string is valid |
|`keyboard.animation_speed`    |`1`        |Increases animation speed of most animations. Recommended 1-5                                              |

## Built-in Animation Configuration
|Define                         |Default      |Description                                                                          |
|-------------------------------|-------------|-------------------------------------------------------------------------------------|
|`keyboard.breath_center`       |`1.5`    |Used to calculate the curve for the breathing animation. Anywhere from 1.0 - 2.7 is valid|
|`keyboard.knight_effect_length`|`4`      |The number of LEDs to light up for the "Knight" animation                                |

## Hardware Modification

To add LED's to boards that don't support them, you will have to add a 3 wires. The power wire will run on 3.3v or 5v (depending on the LED), ground, and data pins will need added to an unused pin on your microcontroller unless your keyboard has specific solder points for them. With those 3 wires connected, set the pixel_pin as described above, and you are ready to use your LED's/Neopixels.

## ADVANCED USAGE
If you wish to interact with these as you would normal LED's and do not want help from KMK, you can disable all helper functions from working and access the neopixel object directly like this.
```python
keyboard.pixels.disabse_auto_write = True
keyboard.pixels.neopixel() # <-- This is the neopixel object    
```
