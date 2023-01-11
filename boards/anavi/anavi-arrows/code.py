import board

from arrows import AnaviArrows

from kmk.extensions.LED import LED
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.peg_oled_Display import (
    Oled,
    OledData,
    OledDisplayMode,
    OledReactionType,
)
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler

keyboard = AnaviArrows()

# I2C pins for the mini OLED display
keyboard.SCL = board.D5
keyboard.SDA = board.D4

# fmt: off
keyboard.keymap = [
    [
        KC.RIGHT, KC.DOWN, KC.LEFT, KC.UP,
    ]
]
# fmt: on

oled_ext = Oled(
    OledData(
        corner_one={0: OledReactionType.STATIC, 1: ['ANAVI Arrows']},
        corner_two={0: OledReactionType.STATIC, 1: [' ']},
        corner_three={0: OledReactionType.STATIC, 1: ['Open Source']},
        corner_four={0: OledReactionType.STATIC, 1: [' ']},
    ),
    oWidth=128,
    oHeight=64,
    toDisplay=OledDisplayMode.TXT,
    flip=False,
)
keyboard.extensions.append(oled_ext)

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

media_keys = MediaKeys()
keyboard.extensions.append(media_keys)

# Rotary encoder that also acts as a key
encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.D8, board.D7, board.D9),)
encoder_handler.map = (((KC.VOLD, KC.VOLU, KC.MUTE),),)
keyboard.modules.append(encoder_handler)

if __name__ == '__main__':
    keyboard.go()
