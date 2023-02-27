import board
import digitalio

from kb import KMKKeyboard, isRight
from storage import getmount

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide, SplitType

keyboard = KMKKeyboard()
keyboard.tap_time = 100

layers = Layers()

split_side = SplitSide.RIGHT if isRight else SplitSide.LEFT

data_pin = board.GP1 if split_side == SplitSide.LEFT else board.GP0
data_pin2 = board.GP0 if split_side == SplitSide.LEFT else board.GP1

split = Split(
    split_side=split_side,
    split_type=SplitType.UART,
    split_flip=False,
    data_pin=data_pin,
    data_pin2=data_pin2
)
keyboard.modules = [layers, split]

LOWER = KC.MO(1)
RAISE = KC.MO(2)
ADJUST = KC.LT(3, KC.SPC)

# Same as the default Corne/crkbd keymap by foostan and drashna
keyboard.keymap = [
    [  #QWERTY
        KC.TAB,    KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                         KC.Y,    KC.U,    KC.I,    KC.O,   KC.P,  KC.BSPC,\
        KC.LCTL,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                         KC.H,    KC.J,    KC.K,    KC.L, KC.SCLN, KC.QUOT,\
        KC.LSFT,   KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,                         KC.N,    KC.M, KC.COMM,  KC.DOT, KC.SLSH, KC.RSFT,\
                                            KC.LGUI,   LOWER,  ADJUST,     KC.ENT,   RAISE,  KC.RALT,
    ],
    [  #LOWER
        KC.ESC,   KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                         KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0, KC.BSPC,\
        KC.LCTL,  KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,                         KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT, KC.NO,   KC.NO,  \
        KC.LSFT,  KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,                         KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,  \
                                            KC.LGUI,   LOWER,  ADJUST,     KC.ENT,   RAISE,  KC.RALT,
    ],
    [  #RAISE
        KC.ESC, KC.EXLM,   KC.AT, KC.HASH,  KC.DLR, KC.PERC,                         KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.BSPC,\
        KC.LCTL, KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,                          KC.MINS,  KC.EQL, KC.LCBR, KC.RCBR, KC.PIPE,  KC.GRV,\
        KC.LSFT, KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,                          KC.UNDS, KC.PLUS, KC.LBRC, KC.RBRC, KC.BSLS, KC.TILD,\
                                            KC.LGUI,   LOWER,  ADJUST,     KC.ENT,   RAISE,  KC.RALT,
    ],
    [  #ADJUST
        KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,                          KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,  \
        KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,                          KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,  \
        KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,                          KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,  \
                                            KC.LGUI,   LOWER,  ADJUST,     KC.ENT,   RAISE,  KC.RALT,
    ]
]

if __name__ == '__main__':
    keyboard.go()
