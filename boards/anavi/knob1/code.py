import board

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.encoder import EncoderHandler
from kmk.scanners.keypad import KeysScanner

knob = KMKKeyboard()
knob.matrix = KeysScanner([])

media_keys = MediaKeys()
knob.extensions.append(media_keys)

# Rotary encoder that also acts as a key
encoder_handler = EncoderHandler()
encoder_handler.divisor = 2
encoder_handler.pins = ((board.D1, board.D2, board.D0),)
encoder_handler.map = (((KC.VOLD, KC.VOLU, KC.MUTE),),)
knob.modules.append(encoder_handler)

print('ANAVI Knob 1')

rgb_ext = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    val_limit=100,
    val_default=25,
    animation_mode=AnimationModes.RAINBOW,
)
knob.extensions.append(rgb_ext)

knob.keymap = [[KC.MUTE]]

if __name__ == '__main__':
    knob.go()
