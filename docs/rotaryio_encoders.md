The module `RotaryIOEncoder` is a wrapper around `rotaryio`  (see [here](https://docs.circuitpython.org/en/latest/shared-bindings/rotaryio/index.html#module-rotaryio)). `rotaryio` has a quirk: encoders must use pins that are consecutive (for example GP16 and GP17 on a Raspberry Pi pico). 

`RotaryIOEncoder` supports using multiple encoders at the same time, each with its own keymap (multiple layers are allowed).

Press buttons are not supported, you should include them in your matrix or wait for the `keypad` module (available in CircuitPython 7.0.0) to be integrated in KMK.

The following is a complete example (you can use it as your `code.py`) of how to use `RotaryIOEncoder`. The example uses `"divisor" = 2` because it was tested using [this](https://www.adafruit.com/product/5001) scrollwheel, but for most cases `"divisor": 4` should work.

```
import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.keys import KC
from kmk.modules.rotaryio_encoder import RotaryIOEncoder
from kmk.modules.mouse_keys import MouseKeys

keyboard = KMKKeyboard()

# We want to use the encoder to scroll so we need mouse keys
keyboard.modules.append(MouseKeys())

# In this example we use only one encoder, connected to the pin 16 and 16
# of a raspberry pi pico.
enc1 = {"pin_a": board.GP17,
            "pin_b": board.GP16,
            "divisor": 2,
            "keymap": [[KC.MW_UP, KC.MW_DN],]
            }

encoders = RotaryIOEncoder((enc1,))

keyboard.modules.append(encoders)

# Matrix
keyboard.diode_orientation = DiodeOrientation.COLUMNS
keyboard.col_pins = (board.GP0,)
keyboard.row_pins = (board.GP20,)

keyboard.keymap = [
    [
        KC.A,
    ],
]

keyboard.debug_enabled = False

if __name__ == "__main__":
    keyboard.go()
```
