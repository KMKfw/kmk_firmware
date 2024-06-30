# Sticky Mod
This module allows to hold a modifier while a key is being tapped repeatedly; the modifier will be released when any other key is pressed or released.
This is for example useful if you want to switch between open windows with `ALT+TAB` or `CMD+TAB`, using only a single key.

## Enabling the module
```python
from kmk.modules.sticky_mod import StickyMod
sticky_mod = StickyMod()
keyboard.modules.append(sticky_mod)
keyboard.keymap = [
    [
        KC.SM(key=KC.TAB, mod=KC.LALT),
        KC.SM(KC.TAB, KC.LSFT(KC.LALT)),
    ],
]
```

## Keycodes

|Key                      |Description                                    |
|-------------------------|-----------------------------------------------|
|`KC.SM(KC.key, KC.mod)`  |sticky mod                                     |
