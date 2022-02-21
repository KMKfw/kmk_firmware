from is31fl3731_pixelbuf import Keybow2040Leds
from keybow_2040 import Keybow2040

from kmk.extensions.rgb import RGB, AnimationModes
from kmk.keys import KC

rgb_ext = RGB(
    pixel_pin=0,
    pixels=Keybow2040Leds(16),
    num_pixels=16,
    animation_mode=AnimationModes.BREATHING_RAINBOW,
)

keybow = Keybow2040()
keybow.extensions = [rgb_ext]

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
