# LED (Mono color backlight)
Want your keyboard to shine? Add some lights!

## Enabling the extention
The only required values that you need to give the LED extention would be the 
pixel pin, and the number of pixels/LED's. If using a split keyboard, this number
is per side, and not the total of both sides.
```python
from kmk.extensions.RGB import RGB
from kb import led_pin  # This can be imported or defined manually

led_ext = LED(led_pin=led_pin)
keyboard.extensions.append(led_ext)
```
 
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
All of these values can be set by default for when the keyboard boots.
```python
from kmk.extentions.led import AnimationModes
led_ext = LED(
    led_pin=led_pin,
    brightness_step=5,
    brightness_limit=100,
    breathe_center=1.5,
    animation_mode=AnimationModes.STATIC,
    animation_speed=1,
    val=100,
    )
```
