import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.P1_06,
        board.P1_04,
        board.P0_11,
        board.P1_00,
        board.P0_24,
        board.P0_22,
        board.MOSI,
        board.MISO,
    )
    row_pins = (
        board.P0_08,
        board.P0_31,
        board.P0_29,
        board.P0_02,
        board.P1_15,
        board.SCK,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = board.P0_06
    rgb_num_pixels = 42
    i2c = board.I2C

# flake8: noqa
    coord_mapping = [
       0,   1,  2,  3,  4,  5,      6,  7, 35, 28, 37, 31,
       8,   9, 10, 11, 12, 13, 33, 14, 15, 26, 36, 29, 39,
       16, 17, 18, 19, 20, 21,     22, 23, 34, 27, 30, 38,
       41,         43, 44, 45,     46, 47, 42,         40,
        ]

encoder_pins = ((board.P0_20, board.P0_17, board.P0_09, False))
