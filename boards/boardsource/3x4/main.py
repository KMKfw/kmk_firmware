from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

layers_ext = Layers()
keyboard.modules = [layers_ext]

RAISE = KC.MO(1)

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
