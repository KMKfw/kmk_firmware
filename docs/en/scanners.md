# Scanners

The default key scanner in KMK assumes a garden variety switch matrix, with
one diode per switch to prevent ghosting.
This doesn't cover all hardware designs though. With macro pads, for example, it
is very common to not have a matrix topology at all.
Boards like this aren't compatible with the default matrix scanner, so you will
need to swap it out with an alternative scanner.


## Keypad Scanners
The scanners in `kmk.scanners.keypad` wrap the `keypad` module that ships with
CircuitPython and support the same configuration and tuning options as their
upstream.

**Some users may need to tweak debounce parameters**, `interval=0.001,debounce_threshold=5` is a good starting point. `debounce_threshold` is only applicable for CircuitPython >= 9.2.0

You can find out more in the [CircuitPython
documentation](https://docs.circuitpython.org/en/latest/shared-bindings/keypad/index.html).

### keypad MatrixScanner
This is the default scanner used by KMK.
It uses the CircuitPython builtin `keypad.KeyMatrix`.

```python
from kmk.scanners.keypad import MatrixScanner

class MyKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()

        # create and register the scanner
        self.matrix = MatrixScanner(
            # required arguments:
            column_pins=self.col_pins,
            row_pins=self.row_pins,
            # optional arguments with defaults:
            columns_to_anodes=DiodeOrientation.COL2ROW,
            interval=0.02, # Matrix sampling interval in ms
            debounce_threshold=None, # Number of samples needed to change state, values greater than 1 enable debouncing. Only applicable for CircuitPython >= 9.2.0
            max_events=64
        )

```


### keypad KeysScanner

The `keypad.Keys` scanner treats individual GPIO pins as discrete keys. To use
this scanner, provide a sequence of pins that describes the layout of your
board then include it in the initialization sequence of your keyboard class.

```python
import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner


# GPIO to key mapping - each line is a new row.
_KEY_CFG = [
    board.SW3,  board.SW7,  board.SW11, board.SW15,
    board.SW2,  board.SW6,  board.SW10, board.SW14,
    board.SW1,  board.SW5,  board.SW9,  board.SW13,
    board.SW0,  board.SW4,  board.SW8,  board.SW12,
]


# Keyboard implementation class
class MyKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()

        # create and register the scanner
        self.matrix = KeysScanner(
            # require argument:
            pins=_KEY_CFG,
            value_when_pressed=False,
            # optional arguments with defaults:
            pull=True,
            interval=0.02, # Matrix sampling interval in ms
            debounce_threshold=None, # Number of samples needed to change state, values greater than 1 enable debouncing. Only applicable for CircuitPython >= 9.2.0
            max_events=64
        )
```


### keypad ShiftRegisterKeys

This scanner can read keys attached to a parallel-in serial-out shift register
like the 74HC165 or CD4021. Note that you may chain shift registers to load in
as many values as you need.
```python
from kmk.scanners.keypad import ShiftRegisterKeys

class MyKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()

        # create and register the scanner
        self.matrix = ShiftRegisterKeys(
            # require arguments:
            clock=board.GP0,
            data=board.GP1,
            latch=board.GP2,
            key_count=8,
            value_when_pressed=False,
            # optional arguments with defaults:
            value_to_latch=True, # 74HC165: True, CD4021: False
            interval=0.02, # Matrix sampling interval in ms
            debounce_threshold=None, # Number of samples needed to change state, values greater than 1 enable debouncing. Only applicable for CircuitPython >= 9.2.0
            max_events=64
        )
```


## Digitalio Scanners

### digitalio MatrixScanner

The digitalio Matrix can scan over, as the name implies, `digitalio.DigitalInOut`
objects. That is especially useful if a matrix is build with IO-expanders.

```python
from kmk.scanners.digitalio import MatrixScanner

class MyKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()

        # create and register the scanner
        self.matrix = MatrixScanner(
            cols=self.col_pins,
            rows=self.row_pins,
            diode_orientation=self.diode_orientation,
            pull=digitalio.Pull.DOWN,
            rollover_cols_every_rows=None, # optional
        )
```


## Rotary Encoder Scanners

### RotaryioEncoder

Matrix events from a quadrature ("rotary") encoder?

```python
from kmk.scanners.encoder import RotaryioEncoder

class MyKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()

        # create and register the scanner
        self.matrix = RotaryioEncoder(
            pin_a=board.GP0,
            pin_b=board.GP1,
            # optional
            divisor=4,
        )
```


## `Scanner` base class

If you require a different type of scanner, you can create your own by
providing a subclass of `Scanner`. This is a very simple interface, it only
contains a single method, `scan_for_changes(self)` which returns a key report
if one exists, or `None` otherwise.


## Advanced Configuration

### Multiple Scanners

Sometimes a single scanner doesn't cover all hardware configurations. For
example: The bulk of the keyboard may be scanned with a matrix scanner, but a
couple of additional keys are directly connected to GPIOs.
In that case KMK allows you to define multiple scanners. The `KMKKeyboard.matrix` attribute can either be assigned a single scanner, or a list of scanners.
KMK assumes that successive scanner keys are consecutive, and populates
`KMKKeyboard.coord_mapping` accordingly; for convenience you may have to supply a `coord_mapping` that resembles your physical layout more closely (expanded below).

Example:
```python
class MyKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()

        # create and register the scanner
        self.matrix = [
            MatrixScanner(...),
            KeysScanner(...),
            # etc...
        ]
```
#### Multiple Scanners `coord_mapping` and keymap changes
To add more scanners you need to add onto your `coord_mapping`.

Example:

`coord_mapping` with just one `MatrixScanner` on a 58 key split keyboard:
```python
coord_mapping = [
     0,  1,  2,  3,  4,  5,         35, 34, 33, 32, 31, 30,
     6,  7,  8,  9, 10, 11,         41, 40, 39, 38, 37, 36,
    12, 13, 14, 15, 16, 17,         47, 46, 45, 44, 43, 42,
    18, 19, 20, 21, 22, 23, 29, 59, 53, 52, 51, 50, 49, 48,
            25, 26, 27, 28,         58, 57, 56, 55, 
    ]
```

`coord_mapping` using `MatrixScanner` and `RotaryioEncoder` on the same 58 key split keyboard with an encoder on each half:
```python
coord_mapping = [
     0,  1,  2,  3,  4,  5,         37, 36, 35, 34, 33, 32,
     6,  7,  8,  9, 10, 11,         43, 42, 41, 40, 39, 38,
    12, 13, 14, 15, 16, 17,         49, 48, 47, 46, 45, 44,
    18, 19, 20, 21, 22, 23, 29, 61, 55, 54, 53, 52, 51, 50,
            25, 26, 27, 28,         60, 59, 58, 57,
            30, 31,                         62, 63 
    ]
```

On the top left side of a standard split keyboard `coord_mapping`, right below that you see a split keyboard where `RotaryioEncoder` and `MatrixScanner` (the default scanner) are used.
In the single scanner example, we used to count from 0 to 29 while the top right side starts at 30.
With the addition of the encoder scanner, the left side has 2 additional keys making it count up to 31 and the right side would then start at 32 and count to 63.
This means that keys 30, 31, 62, and 63 are for encoders.
Notice that all of the encoders are at the end of the array, because we put the encoder scanner after the matrix scanner in `keyboard.matrix`.
Therefore, we need to add 4 more key codes in the corresponding places of our `keyboard.keymap`, they will be used for the encoders.
