from kb import KMKKeyboard
from kmk.extensions.rgb import RGB
from kmk.keys import KC
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

# Adding extensions
rgb = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=keyboard.rgb_num_pixels, val_limit=100, hue_default=190, sat_default=100, val_default=5)

layers_ext = Layers()

keyboard.modules = [layers_ext]
keyboard.extensions = [rgb]

keyboard.keymap = [
    [  #QWERTY
        KC.ESC, KC.Q, KC.W, KC.E, KC.R, KC.T, KC.Y, KC.U, KC.I, KC.O, KC.P, KC.MINS, KC.DEL,\
        KC.TAB, KC.A, KC.S, KC.D, KC.F, KC.G, KC.H, KC.J, KC.K, KC.L, KC.QUOT, KC.ENT,\
        KC.LSFT, KC.Z, KC.X, KC.C, KC.V, KC.B, KC.N, KC.M, KC.COMM, KC.DOT, KC.SLSH, KC.RSFT,\
        KC.LCTL, KC.LGUI, KC.LALT, KC.SPACE, KC.SPACE, KC.RALT, KC.RGUI, KC.RCTL, KC.MO(1)\
    ],
    [  #LOWER
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______
    ],
]

if __name__ == '__main__':
    keyboard.go()
