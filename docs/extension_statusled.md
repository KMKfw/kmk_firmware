# Status LEDs

Indicate which layer you are on with ah array of single leds.

During startup the leds light up to indicte that the bootup is finished.

For the time being just a simple consecutive single led
indicator. And when there are more layers than leds it
wraps around to the first led again.
(Also works for a single led, which just lights when any
layer is active)

_Most of the code comes from the Mono color LED backlight extension_.

## Enabling the extension

To enable the extension you need to define a list of `led_pins`. It can be a list of a one, two or three pins.

```python
from kmk.extensions.statusled import statusLED
import board

statusLED = statusLED(led_pins=[board.GP0, board.GP1, board.GP2])
keyboard.extensions.append(statusLED)
```

## [Keycodes]

| Key           | Aliases | Description         |
| ------------- | ------- | ------------------- |
| `KC.SLED_INC` |         | Increase Brightness |
| `KC.SLED_DEC` |         | Decrease Brightness |

## Configuration

All of these values can be set by default for when the keyboard boots.

```python
statusLED = statusLED(
    led_pin=led_pin,
    brightness=30,
    brightness_step=5,
    brightness_limit=100,
    )
```

The brightness values are in percentages.
