import board

import kb_nn

from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers

encoder_handler = EncoderHandler()
encoder_handler.pins = kb_nn.encoder_pins

keyboard = kb_nn.KMKKeyboard()

keyboard.modules.append(Layers())

_______ = KC.TRNS
xxxxxxx = KC.NO

L1_BSPC = KC.LT(1, KC.BSPC, prefer_hold=True, tap_interrupted=False, tap_time=250)
BTAB = KC.LSFT(KC.TAB)

# keymap
keyboard.keymap = [
    [  # Layer 0: Colemak-DH letters
        KC.ESC , KC.Q   , KC.W   ,    KC.F,    KC.P,    KC.B,          KC.J    , KC.L   , KC.U   , KC.Y   , KC.SCLN, KC.BSPC,
        KC.LGUI, KC.A   , KC.R   ,    KC.S,    KC.T,    KC.G, xxxxxxx, KC.M    , KC.N   , KC.E   , KC.I   , KC.O   , KC.QUOT,
        KC.LALT, KC.Z   , KC.X   ,    KC.C,    KC.D,    KC.V,          KC.K    , KC.H   , KC.COMM, KC.DOT , KC.SLSH, KC.BSLS,
                 xxxxxxx,          KC.LCTL, KC.SPC, KC.MO(1),          KC.MO(1), KC.RSFT , KC.ENT ,         xxxxxxx,
    ],
    [  #Layer 1: Nav & Numbers
         KC.TAB, KC.N1  , KC.N2  , KC.N3  , KC.N4  , KC.N5  ,          KC.N6  , KC.N7  , KC.N8  ,   KC.N9, KC.N0  , KC.DEL ,
        _______, KC.LPRN, KC.LEFT, KC.UP  , KC.RIGHT, KC.RPRN, _______, xxxxxxx, KC.PPLS, KC.PEQL, xxxxxxx, xxxxxxx, xxxxxxx,
        _______, KC.LBRC, KC.LCBR, KC.DOWN, KC.RCBR, KC.RBRC,          KC.EQL , KC.PMNS, KC.UNDS, xxxxxxx, xxxxxxx, xxxxxxx,
                 _______,          _______, _______, _______,          _______, _______, _______, _______,
    ],
    [
        _______, _______, _______, _______, _______, _______,          _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,          _______, _______, _______, _______, _______, _______,
                          _______, _______, _______, _______,          _______, _______, _______, _______,
    ],
    [  #Blank
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,          xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,          xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
                          xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,          xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
    ],
]
# keymap
keyboard.debug_enabled = False

if __name__ == '__main__':
    keyboard.go()
