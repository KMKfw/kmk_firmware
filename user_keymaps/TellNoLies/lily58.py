from kb import KMKKeyboard, data_pin

from kmk.extensions.ble_split import BLE_Split
from kmk.extensions.layers import Layers
from kmk.keys import KC
from kmk.modules.split import Split, SplitSide, SplitType

keyboard = KMKKeyboard()

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(1)
RAISE = KC.MO(2)
ADJUST = KC.LT(3, KC.SPC)
BRWSFW = KC.LALT(KC.RIGHT)
BRWSBW = KC.LALT(KC.LEFT)
UNDO = KC.LCTL(KC.Z)
CUT = KC.LCTL(KC.X)
COPY = KC.LCTL(KC.C)
PASTE = KC.LCTL(KC.V)
DEL = KC.LSFT(KC.DEL)

# TODO Comment one of these on each side
# Left is 0, Right is 1
split_side = 0
split_side = 1
# split = BLE_Split(split_side=split_side)
# No trrs connceting the two halves
split = Split(split_type=Split.BLE, split_side=SplitSide.LEFT)
keyboard.modules.append(split)

layers_ext = Layers()

extensions = [layers_ext, split]

keyboard.keymap = [
    [  #COLMAK_DH
        KC.ESC,   KC.N1,  KC.N2,   KC.N3,   KC.N4,   KC.N5,                        KC.N6,   KC.N7,   KC.N8,   KC.N9,  KC.N0,   KC.TILD,\
        KC.TAB,    KC.Q,  KC.W,    KC.F,    KC.P,    KC.B,                         KC.J,    KC.L,    KC.U,    KC.Y,   KC.SCLN, KC.TILD,\
        KC.BSPC,   KC.A,  KC.R,    KC.S,    KC.T,    KC.G,                         KC.M,    KC.N,    KC.E,    KC.I,   KC.O,    KC.QUOT,\
        KC.LCTRL,  KC.Z,  KC.X,    KC.C,    KC.D,    KC.V,  KC.PSCR,      KC.CAPS, KC.K,    KC.H,   KC.COMM,  KC.DOT, KC.SLSH, KC.ENT,\
                                   KC.LALT, KC.LGUI, LOWER, ADJUST,       ADJUST,  RAISE,  KC.VOLD, KC.VOLU,
    ],
    [  #LOWER
        KC.GESC, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                       KC.N6,   KC.N7,   KC.N8,  KC.N9,   KC.N0, KC.BSPC,\
        KC.TAB,  KC.PGUP, KC.END,  KC.UP,   KC.HOME, KC.INS,                      KC.PSLS, KC.P7,   KC.P8,  KC.P9, KC.PMNS, KC.PEQL,\
        KC.DEL,  KC.PGDN, KC.LEFT, KC.DOWN, KC.RGHT, KC.BRK,                      KC.PAST, KC.P4,   KC.P5,  KC.P6, KC.PPLS, KC.PENT,\
        KC.LSFT, KC.VOLD, KC.MUTE, KC.VOLU, BRWSBW, BRWSFW,  KC.F5,      KC.NLCK, KC.P0,   KC.P1,   KC.P2,  KC.P3, KC.PCMM, KC.PDOT,\
                                   KC.LALT, KC.LGUI, LOWER,  KC.MEH,     KC.LCTL,  KC.MPRV,  KC.MPLY, KC.MNXT,
    ],
    [  #RAISE
        KC.DEL,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                       KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT, XXXXXXX, XXXXXXX,\
        KC.ESC,  KC.EXLM, KC.AT, KC.HASH, KC.DLR,  KC.PERC,                         KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.BSPC,\
        KC.LCTL, KC.DQT,  KC.LT,  KC.GT,  KC.ASTR, KC.LPRN,                         KC.RPRN, KC.UNDS, KC.MINS, KC.PLUS, KC.EQL,  KC.GRV,\
        KC.LSFT, XXXXXXX, XXXXXXX, XXXXXXX, KC.RCBR, KC.LBRC, KC.PSCR,     KC.NLCK, KC.RBRC, KC.RCBR, KC.LBRC, _______, KC.BSLS, KC.TILD,\
                                   KC.LALT, KC.LGUI, LOWER,   ADJUST,      ADJUST,  RAISE,  KC.VOLD, KC.VOLU,
    ],
    [  #ADJUST
        KC.F13,  KC.F14, KC.F15, KC.F16, KC.F17, KC.F18,                        KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT, XXXXXXX, XXXXXXX,\
        KC.F1,   KC.F2,  KC.F3,  KC.F4,  KC.F5,  KC.F6,                       XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,\
        KC.F7,   KC.F8,  KC.F9,  KC.F10, KC.F11, KC.F12,                        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,\
        KC.LSFT, UNDO,  CUT,     COPY,   PASTE,  DEL,     KC.SLSH,      KC.NLCK, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,\
                                   KC.LALT, KC.LGUI, KC.LSFT, ADJUST,       ADJUST,  RAISE,  KC.VOLD, KC.VOLU,
    ]
]

if __name__ == '__main__':
    keyboard.go()
