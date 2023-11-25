import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.pins[17],
        board.pins[16],
        board.pins[15],
        board.pins[14],
        board.pins[13],
        board.pins[12],
    )
    row_pins = (
        board.pins[7],
        board.pins[8],
        board.pins[9],
        board.pins[10],
        board.pins[11],
    )
    diode_orientation = DiodeOrientation.COLUMNS
    uart_pin = board.pins[1]
    rgb_pixel_pin = pins[0]
    data_pin = board.pins[1]
    i2c = board.I2C

    # flake8: noqa
    # fmt: off
   coord_mapping = [
     0,  1,  2,  3,  4,  5,  35, 34, 33, 32, 31, 30,
     6,  7,  8,  9, 10, 11,  41, 40, 39, 38, 37, 36,
    12, 13, 14, 15, 16, 17,  47, 46, 45, 44, 43, 42,
    18, 19, 20, 21, 22, 23,  53, 52, 51, 50, 49, 48,
        25, 26, 27, 28, 29,  59, 58, 57, 56, 55,
    ]

