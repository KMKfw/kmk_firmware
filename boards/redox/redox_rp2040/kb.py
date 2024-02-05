import board
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.GP22,
                board.GP21,
                board.GP20,
                board.GP19,
                board.GP18)
    col_pins = (board.GP6,
                board.GP7,
                board.GP8,
                board.GP9,
                board.GP10,
                board.GP11,
                board.GP12)

    diode_orientation = DiodeOrientation.COL2ROW
    # flake8: noqa
    # fmt: off
    coord_mapping = [
    0,  1,  2,  3,  4,  5,  6,             41, 40, 39, 38, 37, 36, 35,
    7,  8,  9,  10, 11, 12, 13,            48, 47, 46, 45, 44, 43, 42,
    14, 15, 16, 17, 18, 19,                    54, 53, 52, 51, 50, 49,   
    21, 22, 23, 24, 25, 26, 20, 27,    62, 55, 61, 60, 59, 58, 57, 56, 
    28, 29, 30, 31,   32,   33, 34,    69,   68,   67,  66, 65, 64, 63,
    ]