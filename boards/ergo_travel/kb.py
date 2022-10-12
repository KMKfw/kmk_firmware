import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (pins[7], pins[8], pins[9], pins[10])
    col_pins = (
        pins[17],
        pins[16],
        pins[15],
        pins[14],
        pins[13],
        pins[12],
        pins[10],
    )
    diode_orientation = DiodeOrientation.COLUMNS
    led_pin = pins[9]
    rgb_pixel_pin = pins[0]
    rgb_num_pixels = 12
    data_pin = pins[1]
    i2c = board.I2C

    # NOQA
    # flake8: noqa
    # fmt: off
    coord_mapping = [
     0,  1,  2,  3,  4,  5,  6,  34, 33, 32, 31, 30, 29, 28,
     7,  8,  9, 10, 11, 12, 13,  41, 40, 39, 38, 37, 36, 35,
    14, 15, 16, 17, 18, 19, 20,  48, 47, 46, 45, 44, 43, 42,
    21, 22, 23, 24, 25, 26,          54, 53, 52, 51, 50, 49,
    ]
