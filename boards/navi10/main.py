from kb import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()

media = MediaKeys()
layers_ext = Layers()

keyboard.extensions = [media]
keyboard.modules = [layers_ext]

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

keyboard.keymap = [
    [  #Nav Keys
        KC.INSERT,  KC.HOME,    KC.PGUP,
        KC.DELETE,  KC.END,     KC.PGDOWN,
        XXXXXXX,    KC.UP,      XXXXXXX,
        KC.LEFT,    KC.DOWN,    KC.RIGHT
    ],
    [  #I3
        KC.LGUI(KC.L),                  KC.LGUI(KC.LSHIFT(KC.UP)),     KC.LGUI(KC.LSHIFT(KC.P)),
        KC.LGUI(KC.LSHIFT(KC.LEFT)),    KC.LGUI(KC.LSHIFT(KC.DOWN)),   KC.LGUI(KC.LSHIFT(KC.RIGHT)),
        XXXXXXX,                        KC.LGUI(KC.UP),                XXXXXXX,
        KC.LGUI(KC.LEFT),               KC.LGUI(KC.DOWN),              KC.LGUI(KC.RIGHT)
    ],
    [  #Media keys
        KC.MUTE,    KC.MPLY,   KC.MSTP,
        KC.MRWD,    XXXXXXX,   KC.MFFD,
        XXXXXXX,    KC.VOLU,   XXXXXXX,
        KC.MPRV,    KC.VOLD,   KC.MNXT
    ],
]

if __name__ == '__main__':
    keyboard.go()
