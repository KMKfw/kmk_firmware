import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


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

    # Buckle up friends, the bottom row of this keyboard is wild, and making
    # our layouts match, visually, what the keyboard looks like, requires some
    # surgery on the bottom two rows of coords

    # Row index 3 is actually perfectly sane and we _could_ expose it
    # just like the above three rows, however, visually speaking, the
    # top-right thumb cluster button (when looking at the left-half PCB)
    # is more inline with R3, so we'll jam that key (and its mirror) in here
    # flake8: noqa
    coord_mapping = [
     0,  1,  2,  3,  4,  5,          36, 35, 34, 33, 32, 31,
     6,  7,  8,  9, 10, 11,          42, 41, 40, 39, 38, 37,
    12, 13, 14, 15, 16, 17,          48, 47, 46, 45, 44, 43,
    18, 19, 20, 21, 22, 23, 26,  57, 54, 53, 52, 51, 50, 49,
                28, 29, 30,          60, 59, 58,
    ]
