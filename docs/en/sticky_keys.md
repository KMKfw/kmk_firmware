# Sticky Keys

Sticky keys enable you to have keys that stay pressed for a certain time or
until another key is pressed and released.
If the timeout expires or other keys are pressed, and the sticky key wasn't
released, it is handled as a regular key being held.
Sticky keys are sometimes also referred to as "one shot keys".

## Enable Sticky Keys

```python
from kmk.modules.sticky_keys import StickyKeys
sticky_keys = StickyKeys()
# optional: set a custom release timeout in ms (default: 1000ms)
# sticky_keys = StickyKeys(release_after=5000)
keyboard.modules.append(sticky_keys)
```

## Keycodes

|Keycode          | Aliases      |Description                       |
|-----------------|--------------|----------------------------------|
|`KC.SK(KC.ANY)`  | `KC.STICKY`  |make a sticky version of `KC.ANY` |

`KC.STICKY` accepts any valid key code as argument, including modifiers and KMK
internal keys like momentary layer shifts.

## Custom Sticky Behavior

The full sticky key signature is as follows:

```python
KC.SK(
    KC.ANY,              # the key to made sticky
    defer_release=False  # when to release the key
    retap_cancel=True    # repeated tap releases the key
)
```

### `defer_release`

If `False` (default): release sticky key after the first interrupting key
is released, or another is pressed. THis PRevents TYpos LIke THese.
If `True`: stay sticky until all keys are released. Useful when combined with
non-sticky modifiers, layer keys, etc...

### `repeat_cancel`

If `True` (default): Repeated tap releases the key and refreshes timeout.
If `False`: Repeated tap refreshes the timeout.

## Sticky Stacks

Sticky keys can be stacked, i.e. tapping a sticky key within the release timeout
of another will reset the timeout off all previously tapped sticky keys and
"stack" their effects.
In this example if you tap `SK_LCTL` and then `SK_LSFT` followed by `KC.TAB`,
the output will be `ctrl+shift+tab`.

```python
SK_LCTL = KC.SK(KC.LCTL)
SK_LSFT = KC.SK(KC.LSFT)

keyboard.keymap = [[SK_LSFT, SK_LCTL, KC.TAB]]
```
