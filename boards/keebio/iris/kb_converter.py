import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    # Pin mappings for converter board found at hardware/README.md
    # QMK: MATRIX_COL_PINS { F6, F7, B1, B3, B2, B6 }
    # QMK: MATRIX_ROW_PINS { D7, E6, B4, D2, D4 }
    col_pins = (board.A2, board.A3, board.A4, board.A5, board.SCK, board.MOSI)
    row_pins = (board.D11, board.D10, board.D9, board.RX, board.D13)
    diode_orientation = DiodeOrientation.COLUMNS

    split_flip = True
    split_offset = (6, 6, 6, 6, 6)
    split_type = 'UART'
    data_pin = board.SCL
    data_pin2 = board.SDA
    rgb_num_pixels = 12
    i2c = board.I2C
    rgb_pixel_pin = board.TX
    led_pin = board.D7

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
