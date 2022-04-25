# ModHoldAndTap
This module allows to immitate the behaviour of ATL+TAB or CMD+TAB, etc.  
Basically, it will hold the mod and tap a key. The mod will be released when any other key is pressed or the layer key is released.

## Enabling the module
```python
from kmk.module.modholdandtap import ModHoldAndTap
modholdandtap = ModHoldAndTap()
keyboard.modules.append(modholdandtap)
keyboard.keymap = [
    [
        KC.MHAT(kc=KC.TAB, mod=KC.LALT),
        KC.MHAT(KC.TAB, KC.LSFT(KC.LALT)),
    ],
]
```

## Keycodes

|Key                      |Description                                    |
|-------------------------|-----------------------------------------------|
|`KC.MHAT(KC.key, KC.mod)`|holds the mod and taps the key                 |
