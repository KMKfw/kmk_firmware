from keybow_2040 import Keybow2040

from kmk.keys import KC

keybow = Keybow2040()

# fmt: off
keybow.keymap = [
    [
        KC.A, KC.B, KC.C, KC.D,
        KC.E, KC.F, KC.G, KC.H,
        KC.I, KC.J, KC.K, KC.L,
        KC.M, KC.N, KC.O, KC.P,
        KC.Q
    ]
]
# fmt: on

if __name__ == '__main__':
    keybow.go()
