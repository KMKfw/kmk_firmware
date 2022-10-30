# Ferris Sweep pinout translated from QMK repo
# CreditT: 2018-2020 ENDO Katsuhiro, David Philip Barr, Pierre Chevalier

import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.kb2040 import pinout as pins

from kmk.scanners.keypad import KeysScanner

from storage import getmount

# GPIO to key mapping - each line is a new row.
# fmt: off
_KEY_CFG_LEFT = [
     pins[9], pins[16], pins[17], pins[18], pins[19],
    pins[15], pins[14], pins[13], pins[12],  pins[0],
     pins[4],  pins[5],  pins[6],  pins[7],  pins[8],
                                  pins[10], pins[11],
]

_KEY_CFG_RIGHT = [
    pins[19], pins[18], pins[17], pins[16],  pins[9],
     pins[0], pins[12], pins[13], pins[14], pins[15],
     pins[8],  pins[7],  pins[6],  pins[5],  pins[4],
    pins[11], pins[10],                        
]
# fmt: on


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        # create and register the scanner
        self.matrix = KeysScanner(
            # Swap the pins for the left and right half
            pins=_KEY_CFG_RIGHT
            if str(getmount('/').label)[-1] == 'R'
            else _KEY_CFG_LEFT,
        )

    # flake8: noqa
    # fmt: off
    coord_mapping = [
     0,  1,  2,  3,  4,   17, 18, 19, 20, 21,
     5,  6,  7,  8,  9,   22, 23, 24, 25, 26,
    10, 11, 12, 13, 14,   27, 28, 29, 30, 31,
                15, 16,   32, 33
    ]
