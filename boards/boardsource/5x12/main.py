from kb import KMKKeyboard
from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()

media = MediaKeys()
layers_ext = Layers()

keyboard.modules = [layers_ext]
keyboard.extensions = [media]

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(1)
RAISE = KC.MO(2)

keyboard.keymap = [
    [  #QWERTY
        KC.GRV,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.BSPC,
        KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.DEL,
        KC.ESC,  KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.ENT,
        KC.PIPE, KC.LCTL, KC.LALT, KC.LGUI, LOWER,   KC.SPC,  KC.SPC,  RAISE,   KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT
    ],
    [  #LOWER
        KC.ESC,  KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,
        _______, _______, _______, _______, _______, _______, _______, _______, KC.UP,   _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, KC.LEFT, KC.DOWN, KC.RGHT, _______, _______,
        KC.CAPS, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, KC.MNXT, KC.VOLD, KC.VOLU, KC.MPLY
    ],
    [  #RAISE
        KC.GRV,  KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,
        KC.ESC,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.DEL,
        _______, KC.N4,   KC.N5,   KC.N6,   KC.PLUS, KC.F5,   KC.F6,   KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC, _______,
        KC.ENT,  KC.N7,   KC.N8,   KC.N9,   KC.MINS, KC.F11,  KC.F12,  KC.NUHS, KC.NUBS, KC.MUTE, _______, KC.BSLS,
        _______, _______, _______, _______, _______, _______, _______, _______, KC.MNXT, KC.VOLD, KC.VOLU, KC.MPLY
    ]
]

if __name__ == '__main__':
    keyboard.go()
