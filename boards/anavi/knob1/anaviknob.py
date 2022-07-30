'''
KMK keyboard for ANAVI Knob 1
'''

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner

# fmt: off
_KEY_CFG = [
    board.D0
]
# fmt: on


class AnaviKnob(KMKKeyboard):
    '''
    Default keyboard config for the ANAVI Knob 1
    '''

    def __init__(self):
        self.matrix = KeysScanner(_KEY_CFG)
