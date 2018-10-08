from kmk.common.consts import DiodeOrientation, UnicodeModes
from kmk.common.keycodes import KC
from kmk.common.macros.unicode import unicode_sequence
from kmk.common.pins import Pin as P
from kmk.entrypoints.handwire.pyboard import main

cols = (P.Y12, P.Y11, P.Y10, P.Y9, P.X8, P.X7, P.X6, P.X5, P.X4, P.X3, P.X2, P.X1)
rows = (P.Y1, P.Y2, P.Y3, P.Y4)

diode_orientation = DiodeOrientation.COLUMNS

unicode_mode = UnicodeModes.LINUX
tap_time = 180

FLIP = unicode_sequence([
    "28",
    "30ce",
    "ca0",
    "75ca",
    "ca0",
    "29",
    "30ce",
    "5f61",
    "253b",
    "2501",
    "253b",
])

keymap = [
    [
        # Default
        [KC.GESC, KC.QUOTE, KC.COMMA, KC.DOT, KC.P, KC.Y, KC.F, KC.G, KC.C, KC.R, KC.L, KC.BKSP],
        [KC.TAB, KC.A, KC.O, KC.E, KC.U, KC.I, KC.D, KC.H, KC.T, KC.N, KC.S, KC.ENT],
        [KC.LSFT, KC.SCLN, KC.Q, KC.J, KC.K, KC.X, KC.B, KC.M, KC.W, KC.V, KC.Z, KC.SLSH],
        [KC.LCTRL, KC.LGUI, KC.LALT, KC.NO, KC.MO(2), KC.LT(3, KC.SPC), KC.LT(3, KC.SPC), KC.MO(4), KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT],
    ],
    [
        # Gaming
        [KC.TAB, KC.QUOT, KC.COMM, KC.DOT, KC.P, KC.Y, KC.F, KC.G, KC.C, KC.R, KC.L, KC.BKSP],
        [KC.ESC, KC.A, KC.O, KC.E, KC.U, KC.I, KC.D, KC.H, KC.T, KC.N, KC.S, KC.ENT],
        [KC.LSFT, KC.SCLN, KC.Q, KC.J, KC.K, KC.X, KC.B, KC.M, KC.W, KC.V, KC.Z, KC.SLSH],
        [KC.LCTRL, KC.LGUI, KC.LALT, KC.F1, KC.F2, KC.SPC, KC.SPC, KC.MO(4), KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT],
    ],
    [
        # Raise1
        [KC.TILD, KC.EXLM, KC.AT, KC.HASH, KC.DLR, KC.PERC, KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.DEL],
        [KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.LBRC, KC.RBRC, KC.BSLS],
        [KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.INS, KC.PGDN, KC.PGUP, KC.MINS],
        [KC.RESET, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.NO, KC.NO, KC.EQL, KC.HOME, KC.VOLD, KC.VOLU, KC.END],
    ],
    [
        # Raise2
        [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.N7, KC.N8, KC.N9, KC.BKSP],
        [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.N4, KC.N5, KC.N6, KC.NO],
        [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.N1, KC.N2, KC.N3, KC.NO],
        [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.N0, KC.N0, KC.PDOT, KC.ENT],
    ],
    [
        # Raise3
        [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, FLIP, KC.TRNS, KC.F10, KC.F11, KC.F12, KC.LSHIFT(KC.INS)],
        [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F7, KC.F8, KC.F9, KC.NO],
        [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F4, KC.F5, KC.F6, KC.NO],
        [KC.DF(0), KC.DF(1), KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F1, KC.F2, KC.F3, KC.NO],
    ],
]
