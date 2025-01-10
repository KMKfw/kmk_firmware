import board

from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.encoder import EncoderHandler
from kmk.scanners.keypad import KeysScanner

knob = KMKKeyboard()

# I2C pins for the mini OLED display
knob.SCL = board.D5
knob.SDA = board.D4

display = Display(
    display=SSD1306(sda=board.D4, scl=board.D5),
    entries=[
        TextEntry(text='ANAVI Knobs 3\n\nKMK Firmware'),
    ],
    height=64,
)
knob.extensions.append(display)

knob.matrix = KeysScanner([], value_when_pressed=False)

media_keys = MediaKeys()
knob.extensions.append(media_keys)

# Rotary encoders that also acts as keys
encoder_handler = EncoderHandler()
encoder_handler.divisor = 2
encoder_handler.pins = (
    (board.D1, board.D2, board.D0),
    (board.D9, board.D10, board.D3),
    (board.D7, board.D8, board.D6),
)
encoder_handler.map = (
    ((KC.VOLD, KC.VOLU, KC.MUTE), (KC.UP, KC.DOWN, KC.A), (KC.RIGHT, KC.LEFT, KC.B)),
)
knob.modules.append(encoder_handler)

rgb = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    val_limit=100,
    val_default=25,
    animation_mode=AnimationModes.RAINBOW,
)
knob.extensions.append(rgb)

knob.keymap = [[KC.MUTE]]

if __name__ == '__main__':
    knob.go()
