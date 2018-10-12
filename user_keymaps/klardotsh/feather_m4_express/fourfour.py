from kmk.consts import DiodeOrientation, UnicodeModes
from kmk.entrypoints.handwire.feather_m4_express import main
from kmk.firmware import Firmware
from kmk.keycodes import KC
from kmk.macros.simple import send_string, simple_key_sequence
from kmk.macros.unicode import unicode_codepoint_sequence
from kmk.pins import Pin as P

cols = (P.D11, P.D10, P.D9)
rows = (P.A2, P.A3, P.A4, P.A5)

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

ANGRY_TABLE_FLIP = unicode_codepoint_sequence([
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
        [KC.TT(3),             KC.SPACE, ANGRY_TABLE_FLIP],
    ],
    [
        [KC.TRNS, KC.B, KC.C],
        [KC.NO,   KC.D, KC.E],
        [KC.F,    KC.G, KC.H],
        [KC.I,    KC.J, KC.K],
    ],
    [
        [KC.VOLU, KC.MUTE, ANGRY_TABLE_FLIP],
        [KC.TRNS, KC.PIPE, MACRO_TEST_SIMPLE],
        [KC.VOLD, KC.P,    MACRO_TEST_STRING],
        [KC.L,    KC.M,    KC.N],
    ],
    [
        [KC.NO,   KC.UC_MODE_NOOP,  KC.C],
        [KC.NO,   KC.UC_MODE_LINUX, KC.E],
        [KC.TRNS, KC.UC_MODE_MACOS, KC.H],
        [KC.O,    KC.P,             KC.Q],
    ],
]
