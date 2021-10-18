import board
from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()
encodermap = [
    [
        (KC.VOLD, KC.VOLU, 1),
        (KC.MINUS, KC.PLUS, 1),
        (KC.DOWN, KC.UP, 1)
    ]
]
encoderctrl = EncoderHandler([board.GP19, board.GP21, board.GP26], [board.GP20, board.GP22, board.GP27], encodermap)

layersctrl = Layers()

keyboard.modules = [encoderctrl, layersctrl]

keyboard.keymap = [
    [
        KC.N1, KC.N2, KC.N3,
        KC.A, KC.E, KC.I,
        KC.B, KC.F, KC.J,
        KC.C, KC.G, KC.K,
        KC.D, KC.H, KC.L
    ]
]

if __name__ == '__main__':
    keyboard.go()
