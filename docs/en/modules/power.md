# Power(save)
This module allows you to save power and is targeted to Bluetooth/battery
based keyboards.

## Keycodes
|Key                    |Description              |
|-----------------------|-------------------------|
|`KC.PS_TOG `           |Toggles powersave on/off |
|`KC.PS_ON `            |Turns powersave on       |
|`KC.PS_OFF `           |Turns powersave off      |

# Enabling the extension
To turn on basic power saving, this is all that is required.
```python
from kmk.modules.power import Power

power = Power()

keyboard.modules.append(power)

```

## Optional extra power saving
On supported boards, such as the nice!nano, power can be cut on VCC saving extra
power if OLEDS or RGBs are installed. These drain power even when off, so this
will prevent them from doing so. 

```python
from kmk.modules.power import Power

# Your kb.py may already have this set. If not, add it like this
# import board
# keyboard.powersave_pin = board.P0_13
power = Power(powersave_pin=keyboard.powersave_pin)

keyboard.modules.append(power)

```

Make sure that the pin is correct for your microcontroller. The example is for 
the nice!nano. Not all microcontrollers have this feature and this can be omitted
if not and there will simply be less power saving.
