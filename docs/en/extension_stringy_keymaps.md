# Stringy Keymaps

Enables referring to keys by `'NAME'` rather than `KC.NAME`.

For example:

```python
from kmk.extensions.stringy_keymaps import StringyKeymaps

# Normal
# keyboard.keymap = [[ KC.A, KC.B, KC.RESET ]]

# Indexed
# keyboard.keymap = [[ KC['A'], KC['B'], KC['RESET'] ]]

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
