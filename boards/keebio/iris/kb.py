import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.P1_00, board.P0_11, board.P1_04, board.P0_08, board.P0_22)
    col_pins = (
        board.P0_02,
        board.P1_15,
        board.P1_13,
        board.P1_11,
        board.P0_10,
        board.P0_09,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    led_pin = board.P1_06
    rgb_pixel_pin = board.P0_06
    rgb_num_pixels = 12
    i2c = board.I2C
    data_pin = board.P0_20
    powersave_pin = board.P0_13

    # flake8: noqa
    coord_mapping = [
     0,  1,  2,  3,  4,  5,          35, 34, 33, 32, 31, 30,
     6,  7,  8,  9, 10, 11,          41, 40, 39, 38, 37, 36,
    12, 13, 14, 15, 16, 17,          47, 46, 45, 44, 43, 42,
    18, 19, 20, 21, 22, 23, 26,  56, 53, 52, 51, 50, 49, 48,
                27, 28, 29,          59, 58, 57,
    ]
