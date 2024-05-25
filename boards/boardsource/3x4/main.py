from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

layers = Layers()
keyboard.modules = [layers]

RAISE = KC.MO(1)

# fmt:off
keyboard.keymap = [
    [  #Base
        KC.N0,  KC.N1,  KC.N4,  KC.N7,
        KC.ENT, KC.N2,  KC.N5,  KC.N8,
        RAISE,  KC.N3,  KC.N6,  KC.N9
    ],
    [  #RAISE
        _______, _______, _______, _______,
        _______, _______, _______, _______,
        _______, _______, _______, _______
    ]
]
# fmt:on

if __name__ == '__main__':
    keyboard.go()
