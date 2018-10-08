from kmk.common.consts import DiodeOrientation, UnicodeModes
from kmk.common.keycodes import KC
from kmk.common.macros.simple import send_string, simple_key_sequence
from kmk.common.macros.unicode import unicode_sequence
from kmk.common.pins import Pin as P
from kmk.entrypoints.handwire.itsybitsy_m4_express import main
from kmk.firmware import Firmware

cols = (P.A4, P.A5, P.D7)
rows = (P.D12, P.D11, P.D10)

diode_orientation = DiodeOrientation.COLUMNS
unicode_mode = UnicodeModes.LINUX

MACRO_TEST_SIMPLE = simple_key_sequence([
    KC.LSHIFT(KC.H),
    KC.E,
    KC.L,
    KC.L,
    KC.O,

    KC.SPACE,

    KC.MACRO_SLEEP_MS(500),

    KC.LSHIFT(KC.K),
    KC.LSHIFT(KC.M),
    KC.LSHIFT(KC.K),
    KC.EXCLAIM,
])

MACRO_TEST_STRING = send_string("Hello! from, uhhhh, send_string | and some other WEIRD STUFF`  \\ like this' \"\t[]")

ANGRY_TABLE_FLIP = unicode_sequence([
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
        [KC.GESC,              KC.A,     KC.RESET],
        [KC.MO(1),             KC.B,     KC.MUTE],
        [KC.LT(2, KC.EXCLAIM), KC.HASH,  KC.ENTER],
    ],
    [
        [KC.MUTE, KC.B, KC.C],
        [KC.TRNS,   KC.D, KC.E],
        [KC.F,    KC.G, KC.H],
    ],
    [
        [KC.VOLU, KC.MUTE, ANGRY_TABLE_FLIP],
        [KC.NO, KC.PIPE, MACRO_TEST_SIMPLE],
        [KC.TRNS, KC.P,    MACRO_TEST_STRING],
    ],
]
