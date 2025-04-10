from kb import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()

media = MediaKeys()
layers = Layers()

keyboard.modules = [layers]
keyboard.extensions = [media]

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(1)
RAISE = KC.MO(2)

# fmt:off
keyboard.keymap = [
    [  #QWERTY
        KC.ESC,   KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.PLUS, KC.MINUS, _______, _______, KC.BSPC , KC.F1,
        _______ , KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.AT,  KC.ASTERISK, _______, _______, KC.F3,
        _______ , KC.CAPSLOCK, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.LBRACKET, KC.RBRACKET, KC.EQUAL, _______, KC.ENT, KC.F5,
        KC.MO(1), KC.LSFT, _______, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.RSFT,  _______, _______, KC.F7,
        _______ , _______, _______, _______, _______, _______, _______, KC.SPACE, _______, _______, _______, _______, _______, _______, _______, _______
    ],
    [  #LOWER
        KC.ESC,  KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11 , _______, _______, _______, _______, _______, 
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, KC.UP, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, KC.LEFT, KC.DOWN, KC.RIGHT, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______    ]
]
# fmt:on

if __name__ == '__main__':
    keyboard.go()
ert