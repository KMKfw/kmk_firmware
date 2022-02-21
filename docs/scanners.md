# Scanners

Smaller boards and macro pads sometimes assign a GPIO pin to each key, rather
than using a full matrix. Boards like this aren't compatible with the default
matrix scanner, so you will need to swap it out with an alternative scanner.

Beside the default `Matrix` scanner, KMK includes the following:


## keypad.Keys

The `keypad.Keys` scanner treats individual GPIO pins as discrete keys. To use
this scanner, provide a sequence of pins that describes the layout of your
board then include it in the initialisation sequence of your keyboard class.

```python
import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.native_keypad_scanner import keys_scanner


# GPIO to key mapping - each line is a new row.
_KEY_CFG = [
    [board.SW3,  board.SW7,  board.SW11, board.SW15],
    [board.SW2,  board.SW6,  board.SW10, board.SW14],
    [board.SW1,  board.SW5,  board.SW9,  board.SW13],
    [board.SW0,  board.SW4,  board.SW8,  board.SW12],
]


# Keyboard implementation class
class MyKeyboard(KMKKeyboard):
    def __init__(self):
        # create and register the scanner
        self.matrix = keys_scanner(_KEY_CFG)
```


## keypad.KeyMatrix

The `keypad.KeyMatrix` scanner is an alternative implementation of the default
matrix scanner using CircuitPython's builtin keypad objects. This is currently
experimental and ***not recommended for use***.

Using this scanner is similar to the `keypad.Keys` scanner. Create the scanner
using `keypad_matrix()` instead of `keys_scanner()`.


## `Scanner` base class

If you require a different type of scanner, you can create your own by
providing a subclass of `Scanner`. This is a very simple interface, it only
contains a single method, `scan_for_changes(self)` which returns a key report
if one exists, or `None` otherwise.

