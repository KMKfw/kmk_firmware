from kmk.consts import DiodeOrientation, UnicodeModes
from kmk.entrypoints.handwire.circuitpython_samd51 import main
from kmk.keycodes import KC
from kmk.macros.simple import send_string
from kmk.macros.unicode import unicode_string_sequence
from kmk.pins import Pin as P
from kmk.types import AttrDict

cols = (P.A0, P.A1, P.A2, P.A3, P.A4, P.A5, P.SCK, P.MOSI, P.MISO, P.RX, P.TX, P.D4)
rows = (P.D10, P.D11, P.D12, P.D13)

diode_orientation = DiodeOrientation.COLUMNS


# ------------------User level config variables ---------------------------------------
unicode_mode = UnicodeModes.LINUX
tap_time = 200
leader_timeout = 2000
DEBUG_ENABLE = True

emoticons = AttrDict({
    # Emoticons, but fancier
    'ANGRY_TABLE_FLIP': r'(ノಠ痊ಠ)ノ彡┻━┻',
    'CHEER': r'+｡:.ﾟヽ(´∀｡)ﾉﾟ.:｡+ﾟﾟ+｡:.ﾟヽ(*´∀)ﾉﾟ.:｡+ﾟ',
    'TABLE_FLIP': r'(╯°□°）╯︵ ┻━┻',
    'WAT': r'⊙.☉',
    'FF': r'凸(ﾟДﾟ#)',
    'F': r'（￣^￣）凸',
    'MEH': r'╮(￣_￣)╭',
    'YAY': r'o(^▽^)o',
})

for k, v in emoticons.items():
    emoticons[k] = unicode_string_sequence(v)

# ---------------------- Leader Key Macros --------------------------------------------

LEADER_DICTIONARY = {
    (KC.F, KC.L, KC.I, KC.P): emoticons.ANGRY_TABLE_FLIP,
    (KC.C, KC.H, KC.E, KC.E, KC.R): emoticons.CHEER,
    (KC.W, KC.A, KC.T): emoticons.WAT,
    (KC.F, KC.F): emoticons.FF,
    (KC.F,): emoticons.F,
    (KC.M, KC.E, KC.H): emoticons.MEH,
    (KC.Y, KC.A, KC.Y): emoticons.YAY,
}

WPM = send_string("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Bibendum arcu vitae elementum curabitur vitae nunc sed. Facilisis sed odio morbi quis.")

# ---------------------- Keymap ---------------------------------------------------------

keymap = [
    [
        # Default
        [KC.GESC, KC.QUOTE, KC.COMMA, KC.DOT, KC.P, KC.Y, KC.F, KC.G, KC.C, KC.R, KC.L, KC.BKSP],
        [KC.TAB, KC.A, KC.O, KC.E, KC.U, KC.I, KC.D, KC.H, KC.T, KC.N, KC.S, KC.ENT],
        [KC.LSFT, KC.SCLN, KC.Q, KC.J, KC.K, KC.X, KC.B, KC.M, KC.W, KC.V, KC.Z, KC.SLSH],
        [KC.LCTRL, KC.LGUI, KC.LALT, KC.LEAD, KC.MO(2), KC.LT(3, KC.SPC), KC.LT(3, KC.SPC), KC.MO(4), KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT],
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
        [WPM, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F10, KC.F11, KC.F12, KC.LSHIFT(KC.INS)],
        [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F7, KC.F8, KC.F9, KC.NO],
        [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F4, KC.F5, KC.F6, KC.NO],
        [KC.DF(0), KC.DF(1), KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F1, KC.F2, KC.F3, KC.NO],
    ],
]
