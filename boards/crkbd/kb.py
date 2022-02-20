import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.P0_31,
        board.P0_29,
        board.P0_02,
        board.P1_15,
        board.P1_13,
        board.P1_11,
    )
    row_pins = (board.P0_22, board.P0_24, board.P1_00, board.P0_11)
    diode_orientation = DiodeOrientation.COLUMNS
    data_pin = board.P0_08
    rgb_pixel_pin = board.P0_06
    i2c = board.I2C
    powersave_pin = board.P0_13

    # flake8: noqa
    coord_mapping = [
     0,  1,  2,  3,  4,  5,  29, 28, 27, 26, 25, 24,
     6,  7,  8,  9, 10, 11,  35, 34, 33, 32, 31, 30,
    12, 13, 14, 15, 16, 17,  41, 40, 39, 38, 37, 36,
                21, 22, 23,  47, 46, 45,
    ]

