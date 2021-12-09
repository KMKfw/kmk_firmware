# LED (Mono color backlight)
Want your keyboard to shine? Add some lights!

## Enabling the extension
The only required values that you need to give the LED extension would be the
`led_pin`. It can either be a single board pin, or a list of pins for multiple
LED's.
```python
from kmk.extensions.LED import LED
import board

led_ext = LED(led_pin=[board.GP0, board.GP1])
keyboard.extensions.append(led_ext)
```

## [Keycodes]

|Key                          |Aliases            |Description                 |
|-----------------------------|-------------------|----------------------------|
|`KC.LED_TOG()`               |                   |Toggles LED's               |
|`KC.LED_INC()`               |                   |Increase Brightness         |
|`KC.LED_DEC()`               |                   |Decrease Brightness         |
|`KC.LED_SET()`               |                   |Set Brightness              |
|`KC.LED_ANI`                 |                   |Increase animation speed    |
|`KC.LED_AND`                 |                   |Decrease animation speed    |
|`KC.LED_MODE_PLAIN`          |`LED_M_P`          |Static LED's                |
|`KC.LED_MODE_BREATHE`        |`LED_M_B`          |Breathing animation         |

Keycodes with arguments can affect all, or a selection of LED's.
```python
# toggle all LEDs
LED_TOG_ALL = KC.LED_TOG()

# increase brightness of first LED
LED_INC_0   = KC.LED_INC(0)

# decrease brightness of second and third LED
LED_DEC_1_2 = KC.LED_DEC(1,2)

```

## Configuration
All of these values can be set by default for when the keyboard boots.
```python
from kmk.extensions.led import AnimationModes
led_ext = LED(
    led_pin=led_pin,
    brightness_step=5,
    brightness_limit=100,
    breathe_center=1.5,
    animation_mode=AnimationModes.STATIC,
    animation_speed=1,
    user_animation=None,
    val=100,
    )
```
