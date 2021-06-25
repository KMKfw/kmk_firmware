from kb import KMKKeyboard
from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()

media = MediaKeys()
layers_ext = Layers()

keyboard.extensions = [media]
keyboard.modules = [layers_ext]

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(1)
RAISE = KC.MO(2)

keyboard.keymap = [
    [  #QWERTY
        KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.BSPC,
        KC.ESC,  KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.ENT ,
        KC.PIPE, KC.LCTL, KC.LALT, KC.LGUI, LOWER,   KC.SPC,  KC.SPC,  RAISE,   KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT
    ],
    [  #LOWER
        KC.GRV,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.BSPC,
        KC.DEL,  KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC, KC.BSLS,
        _______, KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.NUHS, KC.NUBS, KC.PGUP, KC.PGDN, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, KC.MNXT, KC.VOLD, KC.VOLU, KC.MPLY
    ],
    [  #RAISE
        KC.TILD, KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC, KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.BSPC,
        KC.DEL,  KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.UNDS, KC.PLUS, KC.LCBR, KC.RCBR, KC.PIPE,
        _______, KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  _______, _______, KC.HOME, KC.END,  _______,
        _______, _______, _______, _______, _______, _______, _______, _______, KC.MNXT, KC.VOLD, KC.VOLU, KC.MPLY
    ]
]

if __name__ == '__main__':
    keyboard.go()
