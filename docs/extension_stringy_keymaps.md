# Stringy Keymaps

Enables referring to keys by `'NAME'` rather than `KC.NAME`.

For example:

```python
from kmk.extensions.stringy_keymaps import Stringy_keymaps

# Normal
# keyboard.keymap = [[ KC.A, KC.B, KC.RESET ]]

# Indexed
# keyboard.keymap = [[ KC['A'], KC['B'], KC['RESET'] ]]

# String names
keyboard.keymap = [[ 'A' , 'B', 'RESET' ]]

stringy_keymaps = Stringy_keymaps()

# Enabling debug will show each replacement or failure.
# This is recommended during the initial development of a keyboard.
# stringy_keymaps.debug_enable = True

keyboard.extensions.append(stringy_keymaps)
```

It should be noted that these are **not** ASCII. The string is **not** what
will be sent to the computer. The examples above have no functional difference.
