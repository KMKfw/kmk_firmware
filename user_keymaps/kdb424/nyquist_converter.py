import board
import busio
import neopixel

from kmk.consts import DiodeOrientation, LeaderMode, UnicodeMode
from kmk.handlers.layers import df_pressed
from kmk.handlers.sequences import (compile_unicode_string_sequences)
from kmk.keys import KC, layer_key_validator, make_argumented_key
from kmk.mcus.circuitpython_samd51 import Firmware
from kmk.pins import Pin as P

keyboard = Firmware()

keyboard.col_pins = (P.RX, P.A1, P.A2, P.A3, P.A4, P.A5)
keyboard.row_pins = (P.D13, P.D11, P.D10, P.D9, P.D7)
keyboard.diode_orientation = DiodeOrientation.COLUMNS

keyboard.split_type = "UART"
keyboard.split_flip = True
keyboard.split_offsets = [6, 6, 6, 6, 6]
keyboard.uart_pin = board.SCL
keyboard.extra_data_pin = board.SDA

# ------------------User level config variables ---------------------------------------
keyboard.leader_mode = LeaderMode.TIMEOUT
keyboard.unicode_mode = UnicodeMode.LINUX
keyboard.tap_time = 150
keyboard.leader_timeout = 2000
keyboard.debug_enabled = True

keyboard.pixel_pin = board.TX
keyboard.num_pixels = 12
OFF = (0, 0, 0)
CYAN = (0, 255, 255)

'''
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

pixels.fill(OFF)
pixels.show()
'''

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
    'flip': emoticons.ANGRY_TABLE_FLIP,
    'cheer': emoticons.CHEER,
    'wat': emoticons.WAT,
    'ff': emoticons.FF,
    'f': emoticons.F,
    'meh': emoticons.MEH,
    'yay': emoticons.YAY,
}

_______ = KC.TRNS
XXXXXXX = KC.NO
LT3_SP = KC.LT(3, KC.SPC)
SHFT_INS = KC.LSHIFT(KC.INS)

df = 0
gw = 1
r1 = 2
r2 = 3
r3 = 4


def base(*args, **kwargs):
    keyboard.pixels.fill(OFF)
    keyboard.pixels.show()
    return df_pressed(*args, **kwargs)


def gaming(*args, **kwargs):
    keyboard.pixels.fill(CYAN)
    keyboard.pixels.show()
    return df_pressed(*args, **kwargs)

make_argumented_key(
    validator=layer_key_validator,
    names=('LAYER_GAMING',),
    on_press=gaming,
)

make_argumented_key(
    validator=layer_key_validator,
    names=('LAYER_BASE',),
    on_press=base,
)
BASE = KC.LAYER_BASE(df)
GAMING = KC.LAYER_GAMING(gw)

# ---------------------- Keymap ---------------------------------------------------------

keyboard.keymap = [
    [
        # df
        [KC.GESC,  KC.N1,    KC.N2,    KC.N3,   KC.N4,     KC.N5,  KC.N6,  KC.N7,     KC.N8,   KC.N9,   KC.N0, KC.DEL],
        [KC.GRV,   KC.QUOTE, KC.COMMA, KC.DOT,  KC.P,      KC.Y,   KC.F,   KC.G,      KC.C,    KC.R,    KC.L,  KC.BKSP],
        [KC.TAB,   KC.A,     KC.O,     KC.E,    KC.U,      KC.I,   KC.D,   KC.H,      KC.T,    KC.N,    KC.S,  KC.ENT],
        [KC.LSFT,  KC.SCLN,  KC.Q,     KC.J,    KC.K,      KC.X,   KC.B,   KC.M,      KC.W,    KC.V,    KC.Z,  KC.SLSH],
        [KC.LCTRL, KC.LGUI,  KC.LALT,  KC.LEAD, KC.MO(r1), LT3_SP, LT3_SP, KC.MO(r3), KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT],
    ],
    [
        # gw
        [KC.GESC,  KC.N1,   KC.N2,   KC.N3,  KC.N4, KC.N5,  KC.N6,  KC.N7,     KC.N8,   KC.N9,   KC.N0, KC.DEL],
        [KC.TAB,   KC.QUOT, KC.COMM, KC.DOT, KC.P,  KC.Y,   KC.F,   KC.G,      KC.C,    KC.R,    KC.L,  KC.BKSP],
        [KC.ESC,   KC.A,    KC.O,    KC.E,   KC.U,  KC.I,   KC.D,   KC.H,      KC.T,    KC.N,    KC.S,  KC.ENT],
        [KC.LSFT,  KC.SCLN, KC.Q,    KC.J,   KC.K,  KC.X,   KC.B,   KC.M,      KC.W,    KC.V,    KC.Z,  KC.SLSH],
        [KC.LCTRL, KC.LGUI, KC.LALT, KC.F1,  KC.F2, KC.SPC, KC.SPC, KC.MO(r3), KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT],
    ],
    [
        # r1
        [KC.GESC,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.DEL],
        [KC.TILD,  KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC, KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.DEL],
        [_______,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.LBRC, KC.RBRC, KC.BSLS],
        [_______,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.INS,  _______, _______, KC.MINS],
        [KC.RESET, _______, _______, _______, _______, XXXXXXX, XXXXXXX, KC.EQL,  KC.HOME, KC.PGDN, KC.PGUP, KC.END],
    ],
    [
        # r2
        [KC.GESC, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8, KC.N9, KC.N0,   KC.DEL],
        [_______, _______, _______, _______, _______, _______, _______, _______, KC.N7, KC.N8, KC.N9,   KC.BKSP],
        [_______, _______, _______, _______, _______, _______, _______, _______, KC.N4, KC.N5, KC.N6,   XXXXXXX],
        [_______, _______, _______, _______, _______, _______, _______, _______, KC.N1, KC.N2, KC.N3,   XXXXXXX],
        [_______, _______, _______, _______, _______, _______, _______, _______, KC.N0, KC.N0, KC.PDOT, KC.ENT],
    ],
    [
        # r3
        [KC.GESC, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.F10,  KC.F11,  KC.F12,  KC.DEL],
        [_______, _______, _______, _______, _______, _______, _______, _______, KC.F7,   KC.F8,   KC.F9,   SHFT_INS],
        [_______, _______, _______, _______, _______, _______, _______, _______, KC.F4,   KC.F5,   KC.F6,   KC.VOLU],
        [_______, _______, _______, _______, _______, _______, _______, _______, KC.F1,   KC.F2,   KC.F4,   KC.VOLD],
        [BASE,    GAMING,  _______, _______, _______, _______, _______, _______, _______, _______, _______, XXXXXXX],
    ],
]

if __name__ == '__main__':
    keyboard.go()
