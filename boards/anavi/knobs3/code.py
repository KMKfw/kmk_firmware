import board

from anaviknob import AnaviKnob

from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler

encoder_handler = EncoderHandler()
encoder_handler.pins = (
    (board.D1, board.D2, None, False),
    (board.D9, board.D10, None, False),
    (board.D7, board.D8, None, False),
)
encoder_handler.map = (
    ((KC.VOLD, KC.VOLU), (KC.UP, KC.DOWN), (KC.RIGHT, KC.LEFT)),  # base layer
)

knob = AnaviKnob()
knob.modules.append(encoder_handler)

rgb_ext = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    val_limit=100,
    val_default=25,
    animation_mode=AnimationModes.RAINBOW,
)
knob.extensions.append(rgb_ext)

knob.keymap = [[KC.MUTE, KC.A, KC.B]]

if __name__ == '__main__':
    knob.go()
