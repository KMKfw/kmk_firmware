import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.matrix import intify_coordinate as ic


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.P0_24, board.P1_00, board.P0_11, board.P1_04)
    col_pins = (
        board.P0_29,
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
    data_pin = board.P0_08
    i2c = board.I2C
    powersave_pin = board.P0_13

    # NOQA
    # flake8: noqa
    coord_mapping = [
     0,  1,  2,  3,  4,  5,  6,  34, 33, 32, 31, 30, 29, 28,
     7,  8,  9, 10, 11, 12, 13,  41, 40, 39, 38, 37, 36, 35,
    14, 15, 16, 17, 18, 19, 20,  48, 47, 46, 45, 44, 43, 42,
    21, 22, 23, 24, 25, 26,          54, 53, 52, 51, 50, 49,
    ]
