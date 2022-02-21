'''
KMK keyboard for Pimoroni Keybow 2040.

This is a 4x4 macro pad based on the RP2040. Each key is attached to a single
GPIO, so the KMK matrix scanner needs to be overridden. Additionally, each
key has an RGB LED controlled by an IS31FL3731 controller which is incompatible
with the default RGB module.

The layout of the board is as follows:

        [RESET] [USB-C] [BOOT]
R0 | SW3     SW7     SW11    SW15
R1 | SW2     SW6     SW10    SW14
R2 | SW1     SW5     SW9     SW13
R3 | SW0     SW4     SW8     SW12
    -----------------------------
     C0      C1      C2      C3

The binding defined in the _KEY_CFG array binds the switches to keys such that
the keymap can be written in a way that lines up with the natural order of the
key switches, then adds [BOOT] in (4,0). [RESET] can't be mapped as a key.
'''

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.native_keypad_scanner import keys_scanner

# fmt: off
_KEY_CFG = [
    [board.SW3,  board.SW7,  board.SW11, board.SW15],
    [board.SW2,  board.SW6,  board.SW10, board.SW14],
    [board.SW1,  board.SW5,  board.SW9,  board.SW13],
    [board.SW0,  board.SW4,  board.SW8,  board.SW12],
    [board.USER_SW],
]
# fmt: on


class Keybow2040(KMKKeyboard):
    '''
    Default keyboard config for the Keybow2040.
    '''

    def __init__(self):
        self.matrix = keys_scanner(_KEY_CFG)
