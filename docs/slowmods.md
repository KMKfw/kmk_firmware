# Slow Modifiers

This module provides a set of modifier keycodes designed to work around an issue with sending modified keycodes over Remote Desktop or Hyper-V.

It will automatically apply to [US ANSI Shifted Symbols](keycodes.md#us-ansi-shifted-symbols) keycodes, i.e. shifted keycodes between `KC.TILD` and `KC.QUES`. 
## Issue

Sending a key such as `KC.LCTL(C)` via these clients occasionally results in the following behaviour:

```
KEY-DOWN - QMK: KC_LCTL Event key: Control     Code: ControlLeft   KeyCode: 17
KEY-UP   - QMK: KC_LCTL Event key: Control     Code: ControlLeft   KeyCode: 17 in 7.230ms
KEY-DOWN - QMK: KC_C    Event key: c           Code: KeyC          KeyCode: 67
KEY-UP   - QMK: KC_C    Event key: c           Code: KeyC          KeyCode: 67 in 183.920ms
```

Rather than the expected:
```
KEY-DOWN - QMK: KC_LCTL Event key: Control     Code: ControlLeft   KeyCode: 17
KEY-DOWN - QMK: KC_C    Event key: c           Code: KeyC          KeyCode: 67
KEY-UP   - QMK: KC_C    Event key: c           Code: KeyC          KeyCode: 67 in 137.250ms
KEY-UP   - QMK: KC_LCTL Event key: Control     Code: ControlLeft   KeyCode: 17 in 158.335ms
```

This module works around this issue by only sending the `KEY-UP` for the modifier (`KC.LCTL` in this case) during the `on_release` event rather than during the `on_press` event.

## Example
```python
from kmk.modules.slowmods import SlowMods

keyboard.modules.append(SlowMods())

keyboard.keymap = [
	[
        KC.SCTL(KC.A),   # Ctrl+A
    ],
]
```

## Keycodes

|Keycode                   | Description                   |
|--------------------------|-------------------------------|
|SEL_ALL = KC.SCTL(KC.A)   | `LCTL` + `A`                  |
|SLOW_AT = KC.SSFT(KC.N2)  | `LSFT` + `2`                  |
|S_ALT_F = KC.SALT(KC.F)   | `LALT` + `F`                  |
|S_GUI_E = KC.SGUI(KC.E)   | `LGUI` + `E`                  |
|TEST    = KC.SCS(KC.RGHT) | `LCTL` + `LSFT` + right arrow |

## Compatibility Issues

 - ✅ Works with [Combos/Chords](combos.md), both as the trigger and the output.
 - ❌ Doesn't work with [ModTap](modtap.md) (i.e. `KC.MT()`), neither as tap nor as hold.
