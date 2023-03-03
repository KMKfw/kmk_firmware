# Ferris Sweep pinout translated from QMK repo
# CreditT: 2018-2020 ENDO Katsuhiro, David Philip Barr, Pierre Chevalier

import board

from storage import getmount

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.kb2040 import pinout as pins
from kmk.scanners.keypad import KeysScanner

# GPIO to key mapping - each line is a new row.
# fmt: off
_KEY_CFG_LEFT = [
     pins[9], pins[16], pins[17], pins[18], pins[19],
    pins[15], pins[14], pins[13], pins[12],  pins[0],
     pins[4],  pins[5],  pins[6],  pins[7],  pins[8],
                                  pins[10], pins[11],
]


# fmt: on

class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        # create and register the scanner
        self.matrix = KeysScanner(_KEY_CFG_LEFT)

    # flake8: noqa
    # fmt: off
    coord_mapping = [
     0,  1,  2,  3,  4,   21, 20, 19, 18, 17,
     5,  6,  7,  8,  9,   26, 25, 24, 23, 22,
    10, 11, 12, 13, 14,   31, 30, 29, 28, 27,
                15, 16,   33, 32
    ]
