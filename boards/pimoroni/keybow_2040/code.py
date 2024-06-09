from keybow_2040 import Keybow2040
from keybow_2040_rgb import Keybow2040Leds

from kmk.extensions.rgb import RGB, AnimationModes
from kmk.keys import KC

rgb = RGB(
    pixel_pin=0,
    pixels=Keybow2040Leds(16),
    num_pixels=16,
    animation_mode=AnimationModes.BREATHING_RAINBOW,
)

keybow = Keybow2040()
keybow.extensions = [rgb]

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
