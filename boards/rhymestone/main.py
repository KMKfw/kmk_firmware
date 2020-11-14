from kb import KMKKeyboard
from kmk.extensions.layers import Layers
from kmk.extensions.split import Split, SplitSide, SplitType
from kmk.keys import KC

keyboard = KMKKeyboard()

# TODO Comment one of these on each side
split_side = SplitSide.LEFT
split_side = SplitSide.RIGHT
split = Split(split_type=SplitType.BLE, split_side=split_side)

layers_ext = Layers()

keyboard.extensions = [layers_ext, split]

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(2)
RAISE = KC.MO(1)

KC_Z_SF = KC.LSFT(KC.Z)
KC_SLSF = KC.RSFT(KC.SLSH)
KC_11SF = KC.LSFT(KC.F11)
KC_GRSF = KC.RSFT(KC.GRV)

keyboard.keymap = [
    [  #QWERTY
        KC.Q,     KC.W,     KC.E,     KC.R,     KC.T,     KC.Y,     KC.U,     KC.I,     KC.O,     KC.P,
        KC.A,     KC.S,     KC.D,     KC.F,     KC.G,     KC.H,     KC.J,     KC.K,     KC.L,   KC.ENT,
        KC.Z_SF,     KC.X,     KC.C,     KC.V,     KC.B,     KC.N,     KC.M,  KC.COMM,   KC.DOT,  KC.SLSF,
        KC.LCTL,  KC.LALT,  KC.LGUI,    LOWER,  KC.BSPC,   KC.SPC,    RAISE,  KC.RGUI,   KC.APP,  KC.RCTL
    ],
    [  #RAISE
        KC.N1,     KC.N2,     KC.N3,     KC.N4,     KC.N5,     KC.N6,     KC.N7,     KC.N8,     KC.N9,     KC.N0,
        KC.LSFT,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  KC.LEFT,  KC.DOWN,    KC.UP,  KC.RGHT,  KC.RSFT,
        XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  KC.MINS,    KC.RO,  KC.COMM,   KC.DOT,  KC.SLSF,
        _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______
    ],
    [  #LOWER
        KC.F1,    KC.F2,    KC.F3,    KC.F4,    KC.F5,  KC.MINS,   KC.EQL,  KC.LBRC,  KC.RBRC,  KC.BSLS,
        KC.F6,    KC.F7,    KC.F8,    KC.F9,   KC.F10,  XXXXXXX,  XXXXXXX,  XXXXXXX,  KC.SCLN,  KC.QUOT,
        KC.N11SF,   KC.F12,   KC.ESC,   KC.TAB,  _______,   KC.DEL,  XXXXXXX,  XXXXXXX,    KC.RO,  KC.GRSF,
        _______,  _______,  _______,  _______,   KC.DEL,  _______,  _______,  _______,  _______,  _______
    ]
]

if __name__ == '__main__':
    keyboard.go()
