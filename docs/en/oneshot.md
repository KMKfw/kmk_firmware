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

The OneShot module by default cannot apply two OneShot modifiers to another key. To get around this you can use the [Combos](combos.md) module. Below is a minimal example that allows for multiple OneShot modifiers to apply to the next key pressed. In this example you can tap either of the OneShot keys then tap the other and finally tap `p` and that will send `ctrl+shift+p`.

```python
from kmk.modules.combos import Chord, Combos
from kmk.modules.oneshot import OneShot

oneshot = OneShot()
keyboard.modules.append(oneshot)

OS_LCTL = KC.OS(KC.LCTL, tap_time=None)
OS_LSFT = KC.OS(KC.LSFT, tap_time=None)
OS_LCTL_LSFT = KC.OS(KC.LCTL(OS_LSFT), tap_time=None)

combos = Combos()
keyboard.modules.append(combos)

combos.combos = [
    Chord((OS_LCTL, OS_LSFT), OS_LCTL_LSFT, timeout=1000),
]

keyboard.keymap = [[OS_LSFT, OS_LCTL, KC.P]]
```

Below is the complete list of OneShot and Chords you need to allow any combination of modifiers (left modifiers only).

> <details>
>     <summary>Long code chunk (click to load)</summary>
> 
>     ```python
>     OS_LCTL = KC.OS(KC.LCTL, tap_time=None)
>     OS_LSFT = KC.OS(KC.LSFT, tap_time=None)
>     OS_LGUI = KC.OS(KC.LGUI, tap_time=None)
>     OS_LALT = KC.OS(KC.LALT, tap_time=None)
> 
>     OS_LCTL_LSFT = KC.OS(KC.LCTL(OS_LSFT), tap_time=None)
>     OS_LCTL_LALT = KC.OS(KC.LCTL(OS_LALT), tap_time=None)
>     OS_LCTL_LGUI = KC.OS(KC.LCTL(OS_LGUI), tap_time=None)
>     OS_LSFT_LALT = KC.OS(KC.LSFT(OS_LALT), tap_time=None)
>     OS_LSFT_LGUI = KC.OS(KC.LSFT(OS_LGUI), tap_time=None)
>     OS_LALT_LGUI = KC.OS(KC.LALT(OS_LGUI), tap_time=None)
> 
>     OS_LCTL_LSFT_LGUI = KC.OS(KC.LCTL(KC.LSFT(OS_LGUI)), tap_time=None)
>     OS_LCTL_LSFT_LALT = KC.OS(KC.LCTL(KC.LSFT(OS_LALT)), tap_time=None)
>     OS_LCTL_LALT_LGUI = KC.OS(KC.LCTL(KC.LALT(OS_LGUI)), tap_time=None)
>     OS_LSFT_LALT_LGUI = KC.OS(KC.LSFT(KC.LALT(OS_LGUI)), tap_time=None)
> 
>     OS_LCTL_LSFT_LALT_LGUI = KC.OS(KC.LCTL(KC.LSFT(KC.LALT(OS_LGUI))), tap_time=None)
> 
>     combos.combos = [
>         Chord((OS_LCTL, OS_LSFT), OS_LCTL_LSFT, timeout=1000),
>         Chord((OS_LCTL, OS_LALT), OS_LCTL_LALT, timeout=1000),
>         Chord((OS_LCTL, OS_LGUI), OS_LCTL_LGUI, timeout=1000),
>         Chord((OS_LSFT, OS_LALT), OS_LSFT_LALT, timeout=1000),
>         Chord((OS_LSFT, OS_LGUI), OS_LSFT_LGUI, timeout=1000),
>         Chord((OS_LALT, OS_LGUI), OS_LALT_LGUI, timeout=1000),
> 
>         Chord((OS_LCTL, OS_LSFT, OS_LGUI), OS_LCTL_LSFT_LGUI, timeout=1000),
>         Chord((OS_LCTL, OS_LSFT, OS_LALT), OS_LCTL_LSFT_LALT, timeout=1000),
>         Chord((OS_LCTL, OS_LALT, OS_LGUI), OS_LCTL_LALT_LGUI, timeout=1000),
>         Chord((OS_LSFT, OS_LALT, OS_LGUI), OS_LSFT_LALT_LGUI, timeout=1000),
> 
>         Chord((OS_LCTL, OS_LSFT, OS_LALT, OS_LGUI), OS_LCTL_LSFT_LALT_LGUI, timeout=1000),
>     ]
>     ```
> 
> </details>
