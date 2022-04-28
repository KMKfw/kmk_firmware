# Sticky Mod
This module allows to immitate the behaviour of ATL+TAB or CMD+TAB, etc. for switching between open windows.
The mod will be on hold and the key will be tapped. The mod will be released when any other key is pressed or the layer key is released.

## Enabling the module
```python
from kmk.module.sticky_mod import StickyMod
sticky_mod = StickyMod()
keyboard.modules.append(sticky_mod)
keyboard.keymap = [
    [
        KC.SM(kc=KC.TAB, mod=KC.LALT),
        KC.SM(KC.TAB, KC.LSFT(KC.LALT)),
    ],
]
```

## Keycodes

|Key                      |Description                                    |
|-------------------------|-----------------------------------------------|
|`KC.SM(KC.key, KC.mod)`  |sticky mod                                     |
