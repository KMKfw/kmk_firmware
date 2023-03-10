# OneShot Keycodes

OneShot keys or sticky keys enable you to have keys that keep staying pressed
for a certain time or until another key is pressed and released.
If the timeout expires or other keys are pressed, and the sticky key wasn't
released, it is handled as a regular key hold.

## Enable OneShot Keys

```python
from kmk.modules.oneshot import OneShot
oneshot = OneShot()
# optional: set a custom tap timeout in ms (default: 1000ms)
# oneshot.tap_time = 1500
keyboard.modules.append(oneshot)
```

## Keycodes

|Keycode          | Aliases      |Description                       |
|-----------------|--------------|----------------------------------|
|`KC.OS(KC.ANY)`  | `KC.ONESHOT` |make a sticky version of `KC.ANY` |

`KC.ONESHOT` accepts any valid key code as argument, including modifiers and KMK
internal keys like momentary layer shifts.

## Custom OneShot Behavior

The full OneShot signature is as follows:

```python
KC.OS(
    KC.TAP, # the sticky keycode
    tap_time=None # length of the tap timeout in milliseconds
    )
```


## OneShot Modifier Combinations

The OneShot keys can be chained. In this example if you press `OS_LCTL` and then `OS_LSFT` followed by `KC.TAB`, the output will be `ctrl+shift+tab`.

```python
from kmk.modules.oneshot import OneShot

oneshot = OneShot()
keyboard.modules.append(oneshot)

OS_LCTL = KC.OS(KC.LCTL, tap_time=None)
OS_LSFT = KC.OS(KC.LSFT, tap_time=None)

keyboard.keymap = [[OS_LSFT, OS_LCTL, KC.TAB]]
```

> </details>
