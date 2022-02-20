import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.P0_31, board.P0_29, board.P0_02, board.P1_15, board.P1_13)
    row_pins = (board.P0_10, board.P0_09, board.P1_04, board.P1_06)
    diode_orientation = DiodeOrientation.COLUMNS
    data_pin = board.P0_08
    rgb_pixel_pin = board.P0_06
    rgb_num_pixels = 12
    i2c = board.I2C
    powersave_pin = board.P0_13

    # NOQA
    # flake8: noqa
    coord_mapping = [
     0,  1,  2,  3,  4,  20, 21, 22, 23, 24,
     5,  6,  7,  8,  9,  25, 26, 27, 28, 29,
    10, 11, 12, 13, 14,  30, 31, 32, 33, 34,
            17, 18, 19,  35, 36, 37,
    ]
