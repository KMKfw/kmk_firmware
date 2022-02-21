from keybow import Keybow

from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.layers import Layers

keybow = Keybow()

# fmt: off
keybow.keymap = [
    [
        KC.A, KC.B, KC.C,
        KC.E, KC.F, KC.G,
        KC.I, KC.J, KC.K,
        KC.M, KC.N, KC.O,
    ]
]

keybow.extensions.extend([MediaKeys()])
keybow.modules.extend([Layers()])
# fmt: on

if __name__ == '__main__':
    keybow.go()
