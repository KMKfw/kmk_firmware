from kb import KMKKeyboard
from kmk.extensions.layers import Layers
from kmk.keys import KC

keyboard = KMKKeyboard()

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

RAISE = KC.MO(1)
layers_ext = Layers()

keyboard.extensions = [layers_ext]

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

if __name__ == '__main__':
    keyboard.go()
