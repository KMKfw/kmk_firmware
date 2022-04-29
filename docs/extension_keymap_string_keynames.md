# Keymap String KeyNames

Enables referring to keys by 'NAME' rather than KC.NAME.

For example:

```python
from kmk.extensions.keymap_string_keynames import keymap_string_keynames

# Normal
# keyboard.keymap = [[ KC.A, KC.B, KC.RESET ]]

# Indexed
# keyboard.keymap = [[ KC['A'], KC['B'], KC['RESET'] ]]

# String names
keyboard.keymap = [[ 'A' , 'B', 'RESET' ]]

keymap_string_keynames = keymap_string_keynames()

# Enabling debug will show each replacement or failure.
# This is recommended during the initial development of a keyboard.
# keymap_string_keynames.debug_enable = True

keyboard.extensions.append(keymap_string_keynames)
```

It should be noted that these are **not** ASCII. The string is **not** what
will be sent to the computer. The examples above have no functional difference.
