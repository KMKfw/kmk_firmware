import board

import kb
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler


encoder_handler = EncoderHandler()
encoder_handler.pins = kb.encoder_pins

keyboard = kb.KMKKeyboard()

keyboard.modules.append(Layers())

_______ = KC.TRNS
xxxxxxx = KC.NO

keyboard.keymap = [
    [  #COLEMAK-DH
        KC.TAB,   KC.Q,  KC.W,    KC.F,    KC.P,    KC.B,            KC.J,     KC.L,   KC.U,    KC.Y,    KC.SCLN, KC.BSPC,
        KC.LCTL,  KC.A,  KC.R,    KC.S,    KC.T,    KC.G,   KC.NO,   KC.H,     KC.N,   KC.E,    KC.I,    KC.O,    KC.QUOT,
        KC.LALT,  KC.Z,  KC.X,    KC.C,    KC.D,    KC.V,            KC.K,     KC.H,   KC.COMM, KC.DOT,  KC.SLSH, KC.BSLS,
                        KC.NO, KC.LGUI, KC.LSFT, KC.BSPC,            KC.MO(1), KC.SPC, KC.ENT,  KC.NO,
    ],
    [  #NAVIGATION
        _______, KC.ESC,  KC.PGUP, KC.UP,   KC.PGDN, _______,              KC.ASTR,     KC.N7,     KC.N8,       KC.N9,     KC.PLUS,     _______,
        _______, KC.HOME, KC.LEFT, KC.DOWN, KC.RIGHT, KC.END,   _______,   KC.SLSH,     KC.N4,     KC.N5,       KC.N6,     KC.MINS,     _______,
        _______, _______, _______, _______, _______, _______,              KC.EQL,      KC.N1,     KC.N2,       KC.N3,     KC.N0,       _______,
                          _______, _______, _______, _______,              KC.BKSP,     KC.SPC,    KC.DOT,      _______,
    ],
]

if __name__ == '__main__':
    keyboard.go()
