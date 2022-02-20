import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.GP12, board.GP13, board.GP14, board.GP15)
    col_pins = (board.GP21, board.GP20, board.GP19, board.GP18, board.GP17, board.GP16)
    diode_orientation = DiodeOrientation.COLUMNS

    # flake8: noqa
    coord_mapping = [
     0,  1,  2,  3,  4,  5,  29, 28, 27, 26, 25, 24,
     6,  7,  8,  9, 10, 11,  35, 34, 33, 32, 31, 30,
    12, 13, 14, 15, 16, 17,  41, 40, 39, 38, 37, 36,
                21, 22, 23,  47, 46, 45,
    ]
