from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide, SplitType

keyboard = KMKKeyboard()

# TODO Comment one of these on each side
split_side = SplitSide.LEFT
split_side = SplitSide.RIGHT
split = Split(split_type=SplitType.BLE, split_side=split_side)

layers_ext = Layers()

keyboard.modules = [layers_ext, split]

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(2)
RAISE = KC.MO(1)

RGB_TOG = KC.RGB_TOG
RGB_HUI = KC.RGB_HUI
RGB_HUD = KC.RGB_HUI
RGB_SAI = KC.RGB_SAI
RGB_SAD = KC.RGB_SAD
RGB_VAI = KC.RGB_VAI
RGB_VAD = KC.RGB_VAD

keyboard.keymap = [
    [  #QWERTY
        KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                         KC.Y,    KC.U,    KC.I,    KC.O,   KC.P,\
        KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                         KC.H,    KC.J,    KC.K,    KC.L, KC.SCLN,\
        KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,                         KC.N,    KC.M, KC.COMM,  KC.DOT, KC.SLSH,\
                                    KC.LCTL,   LOWER,  KC.SPC,     KC.BSPC,    RAISE,  KC.ENT,
    ],
    [  #RAISE
        KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                        KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,\
        KC.TAB,  KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT,                      XXXXXXX, KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC,\
        KC.LCTL, KC.GRV,  KC.LGUI, KC.LALT, XXXXXXX,                      XXXXXXX, XXXXXXX, XXXXXXX, KC.BSLS, KC.QUOT,\
                                    XXXXXXX, XXXXXXX, XXXXXXX,      XXXXXXX, XXXXXXX, XXXXXXX,
    ],
    [  #LOWER
        KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC,      KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN,\
        KC.ESC,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,      XXXXXXX, KC.UNDS, KC.PLUS, KC.LCBR, KC.RCBR,\
        KC.CAPS, KC.TILD, XXXXXXX, XXXXXXX, XXXXXXX,      XXXXXXX, XXXXXXX, XXXXXXX, KC.PIPE,  KC.DQT,\
                            XXXXXXX, XXXXXXX, XXXXXXX,      KC.ENT,  XXXXXXX, KC.DEL
    ]
]

if __name__ == '__main__':
    keyboard.go()
