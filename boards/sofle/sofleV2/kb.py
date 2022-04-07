import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.A1, board.A0, board.SCK, board.MISO, board.MOSI, board.D21)
    row_pins = (board.D5, board.D6, board.D7, board.D8, board.D9)
    diode_orientation = DiodeOrientation.COL2ROW
    encoder_pin_0 = board.A2
    encoder_pin_1 = board.A3
    # NOQA
    # flake8: noqa
    coord_mapping = [
     0,  1,  2,  3,  4,  5,    35, 34, 33, 32, 31, 30,
     6,  7,  8,  9, 10, 11,    41, 40, 39, 38, 37, 36,
    12, 13, 14, 15, 16, 17,    47, 46, 45, 44, 43, 42,
    18, 19, 20, 21, 22, 23,    53, 52, 51, 50, 49, 48,
    24, 25, 26, 27, 28, 29,    59, 58, 57, 56, 55, 54
    ]
