import machine

from kmk.common.consts import DiodeOrientation
from kmk.common.keycodes import KC
from kmk.entrypoints.handwire.pyboard import main
from kmk.macros.simple import simple_key_sequence

p = machine.Pin.board
cols = (p.X10, p.X11, p.X12)
rows = (p.X1, p.X2, p.X3)

diode_orientation = DiodeOrientation.COLUMNS

MACRO_TEST_STRING = simple_key_sequence([
    KC.LSHIFT(KC.H),
    KC.E,
    KC.L,
    KC.L,
    KC.O,

    KC.SPACE,

    KC.LSHIFT(KC.K),
    KC.LSHIFT(KC.M),
    KC.LSHIFT(KC.K),
    KC.EXCLAIM,
])

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
        [KC.VOLU, KC.MUTE, KC.Z],
        [KC.TRNS, KC.PIPE, KC.MEDIA_PLAY_PAUSE],
        [KC.VOLD, KC.P, MACRO_TEST_STRING],
    ],
]
