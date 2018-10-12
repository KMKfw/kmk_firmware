# Keymap
The keymap is a very simple set of instruction for your keyboard.
An example keymap for a 4x3 macro pad
```python
keymap = [
    [
        [KC.GESC,  KC.A, KC.B],
        [KC.C,     KC.D, KC.E],
        [KC.F,     KC.G, KC.H],
        [KC.MO(1), KC.I, KC.J],
    ],
    [
        [KC.TRNS, KC.K, KC.RESET],
        [KC.L,    KC.M, KC.N],
        [KC.O,    KC.P, KC.Q],
        [KC.TRNS, KC.R, KC.S],
    ],
]
```

# Handwire
When hand wiring custom keyboards, you will have to set the board up so KMK
knows where things are. This is the basic SETUP.

```python
from kmk.consts import DiodeOrientation
from kmk.keycodes import KC
from kmk.pins import Pin as P
from kmk.entrypoints.circuitpython_samd51 import main
from kmk.firmware import Firmware

cols = (P.D11, P.D10, P.D9)
rows = (P.A2, P.A3, P.A4, P.A5)

diode_orientation = DiodeOrientation.COLUMNS
```

The main things that need set up are:
1. Your microcontroller will need to be set here.
```python
from kmk.entrypoints.circuitpython_samd51 import main
```
2. Set your row and column pins up
```python
cols = (P.D11, P.D10, P.D9)
rows = (P.A2, P.A3, P.A4, P.A5)
```
3. Set your diode orientation
```python
diode_orientation = DiodeOrientation.COLUMNS
```
