# Porting to KMK 
Porting a board to KMK is quite simple, and follows this base format.

```python
import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
{EXTENSIONS_IMPORT}

class KMKKeyboard(_KMKKeyboard):
{REQUIRED}
    extensions = []

```

## REQUIRED
This is designed to be replaced with the defining pins of your keyboard. Rows, 
colums and the diode direction (if any), should be defined like this
```python
    row_pins = [board.p0_31, board.p0_29, board.p0_02, board.p1_15]
    col_pins = [board.p0_22, board.p0_24, board.p1_00, board.p0_11, board.p1_04]
    diode_orientation = DiodeOrientation.COL2ROW
```

## Additional pins for extensions
KMK includes built in extensions for RGB and split keyboards, and powersave. If
these are applicible on your keyboard/microcontroller, the pins should be added
here. Refer to the instructions on the respective extensions page on how to add 
them. If not adding any extensions, leave this as an empty list as shown.

# Coord mapping
If your keyboard is not built electrically as a square (though most are), you can
provide a mapping directly. An example of this is the 
[Corne](https://github.com/foostan/crkbd). That has 12 colums for 3 rows, and 6 
colums for the bottom row. Split keyboards count as the total keyboard, not per 
side. That would look like this
```python
from kmk.matrix import intify_coordinate as ic

    coord_mapping = []
    coord_mapping.extend(ic(0, x) for x in range(12))
    coord_mapping.extend(ic(1, x) for x in range(12))
    coord_mapping.extend(ic(2, x) for x in range(12))
    # And now, to handle R3, which at this point is down to just six keys
    coord_mapping.extend(ic(3, x) for x in range(3, 9))
```


## Keymaps
Keymaps are organized as a list of lists. Keycodes are added for every key on 
each layer. See [keycodes](keycodes.md) for more details on what keycodes are 
avaliable. If using layers or other extensions, also refer to the extensions 
page for additional keycodes.
```python
from kb import KMKKeyboard
from kmk.keys import KC

keyboard = KMKKeyboard()

keyboard.keymap = [
    [KC.A, KC.B],
    [KC.C, KC.D],
]

if __name__ == '__main__':
    keyboard.go()
```

## More information
More information on keymaps can be found [here](config_and_keymap.md)
