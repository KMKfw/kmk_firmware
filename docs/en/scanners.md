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

column_pins = [board.GP0, board.GP1, board.GP2]
row_pins = [board.GP3, board.GP4, board.GP5]

class MyKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()

        # create and register the scanner
        self.matrix = MatrixScanner(
            # required arguments:
            column_pins=column_pins,
            row_pins=row_pins,
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
pins = [
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
            pins=pins,
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

mcp = MCP23017(busio.I2C(board.SCL, board.SDA))

cols = [mcp.get_pin(0), mcp.get_pin(1), mcp.get_pin(2)]
rows = [mcp.get_pin(3), mcp.get_pin(4), mcp.get_pin(5)]

class MyKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()

        # create and register the scanner
        self.matrix = MatrixScanner(
            cols=cols,
            rows=rows,
            diode_orientation=self.diode_orientation,
            pull=digitalio.Pull.DOWN,
            rollover_cols_every_rows=None, # optional
        )
```


## Rotary Encoder Scanners

### RotaryioEncoder

Matrix events from a quadrature ("rotary") encoder.

For any rotary encoders that you may include in your keyboard configuration, you can add this scanner to handle the input of the encoder actions (usually: left turn, right turn, and click) and to be able to configure them via the `keyboard.keymap` as if they were regular keys.

Often, rotary encoders are attached as accessories, i.e. alongside a key/button matrix. The below example shows how this can be configured.

```python
from kmk.scanners.encoder import RotaryioEncoder
from kmk.scanners import DiodeOrientation

class MyKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()
        row_pins = (board.GP2, board.GP3, board.GP4, board.GP5, board.GP6)
        col_pins = (board.GP29, board.GP28, board.GP27,  board.GP26,  board.GP22, board.GP20)

        # create and register the scanner
        rotary = RotaryioEncoder(
            pin_a=board.GP0,
            pin_b=board.GP1,
            # optional
            divisor=4,
        )
        matrix = MatrixScanner(
            row_pins=self.row_pins,
            column_pins=self.col_pins,
            columns_to_anodes=DiodeOrientation.ROW2COL
        )
        self.matrix = [
            matrix,
            rotary
        ]
```

If your design requires symmetrical encoders (e.g. one on each half of a split keyboard), see Multiple Scanners section below for more details.


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


#### Adding Single-Pin Buttons or Rotary Encoders to Keymap Using Scanners and Split

In many cases, split keyboards are symmetrical in form and function. Some split keyboards also have additional hardware like one or more rotary encoders, or non-matrix-connected media or macro buttons. In this case, you will want to configure multiple scanners.

The `Split` class that you're probably already using creates the `coord_mapping` indexes automatically. However, the `add_buttons` argument will cause it to append any additional "buttons" (or encoder actions) to the `coord_mapping` for _each half_ of the keyboard.

By default, `Split` will also configure `MatrixScanner` and assign it to `KMKKeyboard.matrix` as a single/default scanner, but with the additional actions/keys from `RotaryioEncoder`, it will need to be configured in your custom class so that `RotaryioEncoder` can be configured and appended to `KNKKeyboard.matrix`. This enables the rotary actions to map from the `coord_mapping` to the `keybaord.keymap` correctly, making it easy to assign keycodes to the actions or buttons.

Example:
```python
from kmk.scanners import DiodeOrientation
from kmk.scanners.keypad import MatrixScanner
from kmk.scanners.encoder import RotaryioEncoder
from kmk.modules.split import Split


class MyKeyboard(KMKKeyboard):
    def __init__(self) -> None:
        super().__init__()
        self.diode_orientation = DiodeOrientation.ROW2COL
        split_args = {
            'split_side': None, # EE Hands
            'data_pin': board.GP1,
            'data_pin2': board.GP0,
            'split_flip': True,
            'use_pio': True,
            'uart_flip': True,
            'add_buttons': 2 # add left- and right-turn actions for one encoder on each side; see `split_keyboards.md`
        }
        self.row_pins = (board.GP2, board.GP3, board.GP4, board.GP5, board.GP6)
        self.col_pins = (board.GP29, board.GP28, board.GP27,  board.GP26,  board.GP22, board.GP20)
        self.split = Split(**split_args)
        self.modules.append(self.split)

        matrix = MatrixScanner(row_pins=self.row_pins, column_pins=self.col_pins, columns_to_anodes=DiodeOrientation.ROW2COL)
        rotary = RotaryioEncoder(pin_a=board.D7, pin_b=board.D8)
        self.matrix = [
            matrix,
            rotary
        ]


if __name__ == '__main__':
    keyboard = MyKeyboard()
    keyboard.go()
```


#### Multiple Scanners `coord_mapping` and keymap changes
For a more manually-controlled configuration, you can add any other scanners that you need and create your `coord_mapping` in your own code (leaving off the `add_buttons` argument when initializing `Split`)
Creating and assigning a custom `coord_mapping` should be done before initializing `Split` or any scanners.

The below examples illustrate how the additional encoder actions are assigned to the `coord_mapping`. Your configuration should follow this pattern.


`coord_mapping` with just one `MatrixScanner` on a 58 key split keyboard:
```python
keyboard.coord_mapping = [
     0,  1,  2,  3,  4,  5,         35, 34, 33, 32, 31, 30,
     6,  7,  8,  9, 10, 11,         41, 40, 39, 38, 37, 36,
    12, 13, 14, 15, 16, 17,         47, 46, 45, 44, 43, 42,
    18, 19, 20, 21, 22, 23, 29, 59, 53, 52, 51, 50, 49, 48,
            25, 26, 27, 28,         58, 57, 56, 55, 
    ]
```

`coord_mapping` using `MatrixScanner` and `RotaryioEncoder` on the same 58 key split keyboard, adding an encoder to each half:
```python
keyboard.coord_mapping = [
     0,  1,  2,  3,  4,  5,         37, 36, 35, 34, 33, 32,
     6,  7,  8,  9, 10, 11,         43, 42, 41, 40, 39, 38,
    12, 13, 14, 15, 16, 17,         49, 48, 47, 46, 45, 44,
    18, 19, 20, 21, 22, 23, 29, 61, 55, 54, 53, 52, 51, 50,
            25, 26, 27, 28,         60, 59, 58, 57,
            30, 31,                         62, 63 
    ]
```

Note that in both examples, the left-side indexes count from 0 to 29 for the first five rows. But the right side of the first (single scanner) example starts at 30 (in the top right corner) and ends at 59 in the center.

With the addition of the `RotaryioEncoder` scanner, the left side has 2 additional keys (30 and 31) causing the right side to start at 32 and count to 61 in the center, with two more keys at the bottom (62 and 63).
**This means that keys 30, 31, 62, and 63 are for the encoders.**

Notice that, despite the visual layout, all of the encoder keys are at the **_end_** of the array. This is because `RotaryioEncoder` was **_after_** `MatrixScanner` **_in the list_** when the `keyboard.matrix` was assigned. (see example in the previous section above)

Therefore, 4 more key codes can be added in the corresponding places in the `keyboard.keymap`, and they will be assigned to the encoders' actions.


Also note, it may be necessary to configure `Split().split_offset` when configuring your own `coord_mapping` to make sure that the encoders are assigned properly. The value will usually be the first/lowest index value of the right side. In the case of the second example above, the offset value would be 32, but this also depends on your `coord_mapping` layout.
