'''
KMK keyboard for Pimoroni Keybow.

WARNING: This doesn't currently function correctly on the Raspberry Pi Zero,
some of the keys are stuck in the 'pressed' position. There's either a bug in
the keypad implementation on the rpi0, or the pin numbers don't match the pins
in linux.

This is a 4x3 macro pad designed to fit the rpi's GPIO connector. Each key is
attached to a single GPIO and has an APA102 LED mounted underneath it.

The layout of the board is as follows (GPIO connector on the left):

R0 | D20    D6   D22
R1 | D17   D16   D12
R2 | D24   D27   D26
R0 | D13    D5   D23
    ------------------
      C0    C1    C2

This board also functions with an adaptor (see
https://learn.adafruit.com/itsybitsy-keybow-mechanical-keypad/) to work with an
itsybitsy in place of the rpi, which uses an alternate pin mapping:

R0 |  A2    A1    A0
R1 |  A5    A4    A3
R2 | D10    D9    D7
R3 | D11   D12    D2
    ------------------
      C0    C1    C2

This keyboard file should automatically select the correct mapping at runtime.
'''

import board

import adafruit_dotstar
import sys

from kmk.extensions.rgb import RGB, AnimationModes
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.native_keypad_scanner import keys_scanner


# fmt: off
def raspi_pins():
    return [
        [board.D20, board.D16, board.D26],
        [board.D6,  board.D12, board.D13],
        [board.D22, board.D24, board.D5],
        [board.D17, board.D27, board.D23],
    ]


def itsybitsy_pins():
    return [
        [board.D11, board.D12, board.D2],
        [board.D10, board.D9,  board.D7],
        [board.A5,  board.A4,  board.A3],
        [board.A2,  board.A1,  board.A0],
    ]
# fmt: on


def isPi():
    return sys.platform == 'BROADCOM'


if isPi():
    _KEY_CFG = raspi_pins()
    _LED_PINS = (board.SCK, board.MOSI)
else:
    _KEY_CFG = itsybitsy_pins()
    _LED_PINS = (board.SCK, board.MOSI)


led_strip = adafruit_dotstar.DotStar(_LED_PINS[0], _LED_PINS[1], 12)
rgb_ext = RGB(
    pixel_pin=0,
    pixels=led_strip,
    num_pixels=12,
    animation_mode=AnimationModes.BREATHING_RAINBOW,
)


class Keybow(KMKKeyboard):
    '''
    Default keyboard config for the Keybow.
    '''

    extensions = [rgb_ext]

    def __init__(self):
        self.matrix = keys_scanner(_KEY_CFG)
