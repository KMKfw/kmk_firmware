'''
KMK keyboard for ANAVI Knobs 3
'''

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner

# fmt: off
_KEY_CFG = [
    board.D0,
    board.D3,
    board.D6
]
# fmt: on


class AnaviKnob(KMKKeyboard):
    '''
    Default keyboard config for the Keybow2040.
    '''

    def __init__(self):
        self.matrix = KeysScanner(_KEY_CFG)
