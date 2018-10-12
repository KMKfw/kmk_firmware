import machine

from kmk.consts import DiodeOrientation
from kmk.entrypoints.handwire.pyboard import main
from kmk.keycodes import KC

p = machine.Pin.board
cols = (p.X10, p.X11, p.X12)
rows = (p.X1, p.X2, p.X3)

diode_orientation = DiodeOrientation.COLUMNS

keymap = [
    [
        [KC.MO(1), KC.H, KC.RESET],
        [KC.MO(2), KC.I, KC.ENTER],
        [KC.LCTRL, KC.SPACE, KC.LSHIFT],
    ],
    [
        [KC.TRNS, KC.B, KC.C],
        [KC.NO, KC.D, KC.E],
        [KC.F, KC.G, KC.H],
    ],
    [
        [KC.X, KC.Y, KC.Z],
        [KC.TRNS, KC.N, KC.O],
        [KC.R, KC.P, KC.Q],
    ],
]
