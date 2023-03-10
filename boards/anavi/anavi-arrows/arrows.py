'''
KMK keyboard for ANAVI Arrows

This is a macro pad with 4 mechanical switches based on the RP2040. Each key is
attached to a single GPIO, so the KMK matrix scanner needs to be overridden.
'''

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner


class AnaviArrows(KMKKeyboard):
    '''
    Default keyboard config for ANAVI Arrows.
    '''

    def __init__(self):
        self.matrix = KeysScanner([board.D1, board.D2, board.D3, board.D6])
