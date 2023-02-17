import board

from kmk.extensions.LED import LED
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.encoder import EncoderHandler
from kmk.scanners import DiodeOrientation

print('ANAVI Macro Pad 10')

keyboard = KMKKeyboard()
led_ext = LED(
    led_pin=[
        board.D0,
    ],
    brightness=100,
    brightness_step=5,
    brightness_limit=100,
    breathe_center=1.5,
    animation_mode=AnimationModes.STATIC,
    animation_speed=1,
    user_animation=None,
    val=100,
)
keyboard.extensions.append(led_ext)

# WS2812B LED strips on the back
underglow = RGB(
    pixel_pin=board.D10,
    num_pixels=4,
    val_limit=100,
    val_default=25,
    animation_mode=AnimationModes.RAINBOW,
)
keyboard.extensions.append(underglow)

# Neopixel on XIAO RP2040
frontglow = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    val_limit=100,
    val_default=25,
    animation_mode=AnimationModes.RAINBOW,
)
keyboard.extensions.append(frontglow)

keyboard.col_pins = (
    board.D4,
    board.D5,
    board.D6,
)
keyboard.row_pins = (
    board.D3,
    board.D2,
    board.D1,
)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

media_keys = MediaKeys()
keyboard.extensions.append(media_keys)

# Matrix 3x3 keymap, 9 keys in total
keyboard.keymap = [
    [
        KC.N1,
        KC.N2,
        KC.N3,
        KC.N4,
        KC.N5,
        KC.N6,
        KC.N7,
        KC.N8,
        KC.N9,
    ]
]

# Rotary encoder that also acts as a key
encoder_handler = EncoderHandler()
encoder_handler.divisor = 2
encoder_handler.pins = ((board.D8, board.D7, board.D9),)
encoder_handler.map = (((KC.VOLD, KC.VOLU, KC.MUTE),),)
keyboard.modules.append(encoder_handler)

if __name__ == '__main__':
    keyboard.go()
