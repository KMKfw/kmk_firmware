from kb import KMKKeyboard
from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modulessplit import Split, SplitSide, SplitType

keyboard = KMKKeyboard()

# TODO Comment one of these on each side
split_side = SplitSide.LEFT
split_side = SplitSide.RIGHT
split = Split(split_type=SplitType.BLE, split_side=split_side)

media = MediaKeys()
layers_ext = Layers()
keyboard.modules = [layers_ext, split]
keyboard.extensions = (media)

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(1)
RAISE = KC.MO(2)
ADJUST = KC.MO(3)

CALTDEL = KC.LCTL(KC.LALT(KC.DEL))
TSKMGR = KC.LCTL(KC.LSFT(KC.KC_ESC))

keyboard.keymap = [
    [  #QWERTY
        KC.ESC,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.MINS,          KC.EQL,   KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.BSPC,\
        KC.TAB,  KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.LBRC,          KC.RBRC,  KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,\
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.SPC,           KC.SPC,   KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.ENT,\
        KC.LCTL, KC.LGUI, KC.LALT, ADJUST,           LOWER,   KC.SPC,           KC.SPC,   RAISE,            KC.LEFT, KC.UP,   KC.DOWN, KC.RGHT\
    ],
    [  #LOWER
        KC.TILD, KC.EXLM,  KC.AT,   KC.HASH, KC.DLR,  KC.PERC, KC.HOME,          KC.PGUP, KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.DEL,\
        _______, KC.F1,    KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.END ,          KC.PGDN, KC.F6,   KC.UNDS, KC.PLUS, KC.LCBR, KC.RCBR, KC.BSLS,\
        _______, KC.F7,    KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.BSPC,          KC.BSPC, KC.F12,  _______, _______, KC.MUTE, _______, KC.PIPE,\
        _______, _______,  _______, _______, _______, KC.BSPC,                            KC.BSPC, _______, KC.MNXT, KC.VOLD, KC.VOLU, KC.MPLY\
    ],
    [  #RAISE
        KC.ESC,  KC.N1,   KC.N2, KC.N3,  KC.N4,   KC.N5,    _______,             _______, KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.DEL,  \
        _______, KC.N4,   KC.N5, KC.N6,  KC.PLUS, _______,  _______,             _______, _______, KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC, _______, \
        KC.ENT,  KC.N7,   KC.N8, KC.N9,  KC.MINS, _______,  _______,             _______, _______, KC.NUHS, KC.NUBS, KC.MUTE, _______, KC.BSLS, \
        _______, KC.COMM, KC.N0, KC.DOT, _______, KC.BSPC,                                KC.BSPC, _______, KC.MNXT, KC.VOLD, KC.VOLU, KC.MPLY  \
            ],
    [  #ADJUST
        TSKMGR,  _______,  _______, _______, _______, _______, _______,         _______,  _______, _______, _______, _______, _______, CALTDEL,
        _______, _______,  _______, _______, _______, _______, _______,         _______,  _______, _______, _______, _______, _______, _______,
        _______, _______,  _______, _______, _______, _______, _______,         _______,  _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______,           _______, _______,         _______,  _______,          _______, _______, _______, _______,
    ]
]

if __name__ == '__main__':
    keyboard.go()
