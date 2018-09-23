import machine

from kmk.common.consts import DiodeOrientation
from kmk.common.keycodes import KC
from kmk.micropython.pyb_hid import HIDHelper

p = machine.Pin.board

cols = (p.Y12, p.Y11, p.Y10, p.Y9, p.X8, p.X7, p.X6, p.X5, p.X4, p.X3, p.X2, p.X1)
rows = (p.Y1, p.Y2, p.Y3, p.Y4)

diode_orientation = DiodeOrientation.COLUMNS

keymap = [
    [
        [KC.ESC, KC.QUOTE, KC.COMMA, KC.DOT, KC.P, KC.Y, KC.F, KC.G, KC.C, KC.R, KC.L, KC.BKSP],
        [KC.TAB, KC.A, KC.O, KC.E, KC.U, KC.I, KC.D, KC.H, KC.T, KC.N, KC.S, KC.ENT],
        [KC.LSFT, KC.SCLN, KC.Q, KC.J, KC.K, KC.X, KC.B, KC.M, KC.W, KC.V, KC.Z, KC.SLSH],
        [KC.LCTRL, KC.LGUI, KC.LALT, KC.RESET, KC.MO(1), KC.SPC, KC.SPC, KC.A, KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT],
    ],
    [
        [KC.A, KC.QUOTE, KC.COMMA, KC.DOT, KC.P, KC.Y, KC.F, KC.G, KC.C, KC.R, KC.L, KC.BACKSPACE],
        [KC.TAB, KC.A, KC.O, KC.E, KC.U, KC.I, KC.D, KC.H, KC.T, KC.N, KC.S, KC.ENT],
        [KC.LSFT, KC.SCOLON, KC.Q, KC.J, KC.K, KC.X, KC.B, KC.M, KC.W, KC.V, KC.Z, KC.SLSH],
        [KC.LCTRL, KC.LGUI, KC.LALT, KC.RESET, KC.TRNS, KC.SPC, KC.SPC, KC.A, KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT],
    ],
]
