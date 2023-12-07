# Stringy Keymaps

Enables referring to keys by `'NAME'` rather than `KC.NAME`.\
This extension allows for a seamless integration of both string-based key references and standard keycodes.

For example:

```python
from kmk.extensions.stringy_keymaps import StringyKeymaps

# Normal
# keyboard.keymap = [[ KC.A, KC.B, KC.RESET ]]

# Indexed
# keyboard.keymap = [[ KC['A'], KC['B'], KC['RESET'] ]]

# String names mixed with normal keycodes
# keyboard.keymap = [[ 'A' , KC.B, KC.RESET ]]

# String names
keyboard.keymap = [[ 'A' , 'B', 'RESET' ]]

stringyKeymaps = StringyKeymaps()

# Enabling debug will show each replacement or failure.
# This is recommended during the initial development of a keyboard.
# stringyKeymaps.debug_enable = True

keyboard.extensions.append(stringyKeymaps)
```

It should be noted that these are **not** ASCII. The string is **not** what
will be sent to the computer. The examples above have no functional difference.

When utilizing argumented keys, such as `KC.MO(layer)`, it's not possible to use a string like `'MO(layer)'` instead employ the standard notation of e.g. `KC.MO(1)` in your keymap.