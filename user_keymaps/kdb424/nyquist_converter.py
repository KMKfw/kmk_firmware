import board
import busio

from kmk.consts import DiodeOrientation, LeaderMode, UnicodeMode
from kmk.keycodes import KC
from kmk.keycodes import generate_leader_dictionary_seq as glds
from kmk.macros.simple import send_string
from kmk.macros.unicode import compile_unicode_string_sequences
from kmk.mcus.circuitpython_samd51 import Firmware
from kmk.pins import Pin as P
from kmk.types import AttrDict

keyboard = Firmware()

keyboard.col_pins = (P.RX, P.A1, P.A2, P.A3, P.A4, P.A5)
keyboard.row_pins = (P.D13, P.D11, P.D10, P.D9, P.D5)
keyboard.diode_orientation = DiodeOrientation.COLUMNS

keyboard.split_type = "UART"
keyboard.split_flip = True
keyboard.split_offsets = [6, 6, 6, 6, 6]
keyboard.uart_flip = True
keyboard.uart = keyboard.init_uart(tx=board.SDA, rx=board.SCL)

# ------------------User level config variables ---------------------------------------
keyboard.leader_mode = LeaderMode.TIMEOUT
keyboard.unicode_mode = UnicodeMode.LINUX
keyboard.tap_time = 150
keyboard.leader_timeout = 2000
keyboard.debug_enabled = True

emoticons = compile_unicode_string_sequences({
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

# ---------------------- Leader Key Macros --------------------------------------------

keyboard.leader_dictionary = {
    glds('flip'): emoticons.ANGRY_TABLE_FLIP,
    glds('cheer'): emoticons.CHEER,
    glds('wat'): emoticons.WAT,
    glds('ff'): emoticons.FF,
    glds('f'): emoticons.F,
    glds('meh'): emoticons.MEH,
    glds('yay'): emoticons.YAY,
}
LT3_SP = KC.LT(3, KC.SPC)
# ---------------------- Keymap ---------------------------------------------------------

keyboard.keymap = [
    [
        # Default
        [KC.GESC,  KC.N1,    KC.N2,    KC.N3,  KC.N4,     KC.N5,  KC.N6,  KC.N7,    KC.N8,   KC.N9,   KC.N0, KC.DEL],
        [KC.GRV,   KC.QUOTE, KC.COMMA, KC.DOT,  KC.P,     KC.Y,   KC.F,   KC.G,     KC.C,    KC.R,    KC.L,  KC.BKSP],
        [KC.TAB,   KC.A,     KC.O,     KC.E,    KC.U,     KC.I,   KC.D,   KC.H,     KC.T,    KC.N,    KC.S,  KC.ENT],
        [KC.LSFT,  KC.SCLN,  KC.Q,     KC.J,    KC.K,     KC.X,   KC.B,   KC.M,     KC.W,    KC.V,    KC.Z,  KC.SLSH],
        [KC.LCTRL, KC.LGUI,  KC.LALT,  KC.LEAD, KC.MO(2), LT3_SP, LT3_SP, KC.MO(4), KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT],
    ],
    [
        # Gaming
        [KC.GESC,  KC.N1,   KC.N2,   KC.N3,  KC.N4, KC.N5,  KC.N6,  KC.N7,    KC.N8,   KC.N9,   KC.N0, KC.DEL],
        [KC.TAB,   KC.QUOT, KC.COMM, KC.DOT, KC.P,  KC.Y,   KC.F,   KC.G,     KC.C,    KC.R,    KC.L,  KC.BKSP],
        [KC.ESC,   KC.A,    KC.O,    KC.E,   KC.U,  KC.I,   KC.D,   KC.H,     KC.T,    KC.N,    KC.S,  KC.ENT],
        [KC.LSFT,  KC.SCLN, KC.Q,    KC.J,   KC.K,  KC.X,   KC.B,   KC.M,     KC.W,    KC.V,    KC.Z,  KC.SLSH],
        [KC.LCTRL, KC.LGUI, KC.LALT, KC.F1,  KC.F2, KC.SPC, KC.SPC, KC.MO(4), KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT],
    ],
    [
        # Raise1
        [KC.GESC,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.DEL],
        [KC.TILD,  KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC, KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.DEL],
        [KC.TRNS,  KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.LBRC, KC.RBRC, KC.BSLS],
        [KC.TRNS,  KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.INS,  KC.PGDN, KC.PGUP, KC.MINS],
        [KC.RESET, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.NO,   KC.NO,   KC.EQL,  KC.HOME, KC.VOLD, KC.VOLU, KC.END],
    ],
    [
        # Raise2
        [KC.GESC, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8, KC.N9, KC.N0,   KC.DEL],
        [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.N7, KC.N8, KC.N9,   KC.BKSP],
        [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.N4, KC.N5, KC.N6,   KC.VOLU],
        [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.N1, KC.N2, KC.N3,   KC.VOLD],
        [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.N0, KC.N0, KC.PDOT, KC.ENT],
    ],
    [
        # Raise3
        [KC.GESC,  KC.N1,    KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,  KC.N9,  KC.N0,  KC.DEL],
        [KC.TRNS,  KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F10, KC.F11, KC.F12, KC.LSHIFT(KC.INS)],
        [KC.TRNS,  KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F7,  KC.F8,  KC.F9,  KC.NO],
        [KC.TRNS,  KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F4,  KC.F5,  KC.F6,  KC.NO],
        [KC.DF(0), KC.DF(1), KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F1,  KC.F2,  KC.F3,  KC.NO],
    ],
]

if __name__ == '__main__':
    keyboard.go()
