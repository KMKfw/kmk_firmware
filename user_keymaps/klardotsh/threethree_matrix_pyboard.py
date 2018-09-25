import machine

from kmk.common.consts import DiodeOrientation
from kmk.common.keycodes import KC
from kmk.entrypoints.handwire.pyboard import main

p = machine.Pin.board
cols = (p.X10, p.X11, p.X12)
rows = (p.X1, p.X2, p.X3)

diode_orientation = DiodeOrientation.COLUMNS

keymap = [
    [
        [KC.MO(1), KC.GESC, KC.RESET],
        [KC.MO(2), KC.HASH, KC.ENTER],
        [KC.LCTRL, KC.SPACE, KC.LSHIFT],
    ],
    [
        [KC.TRNS, KC.B, KC.C],
        [KC.NO, KC.D, KC.E],
        [KC.F, KC.G, KC.H],
    ],
    [
        [KC.X, KC.Y, KC.Z],
        [KC.TRNS, KC.PIPE, KC.O],
        [KC.R, KC.P, KC.Q],
    ],
]
