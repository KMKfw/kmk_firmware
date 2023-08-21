import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.GP6,
        board.GP7,
        board.GP8,
        board.GP9,
        board.GP10,
        board.GP11,
        board.GP12,
        board.GP13,
        board.GP14,
        board.GP15
    )
    row_pins = (
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5
    )
    diode_orientation = DiodeOrientation.COLUMNS
    # flake8: noqa
    # fmt: off
    coord_mapping = [
        0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
        10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
        30,             34,                 39
    ]
