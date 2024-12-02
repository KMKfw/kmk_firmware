from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.sparkfun_promicro_rp2040 import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        pins[19],
        pins[18],
        pins[17],
        pins[16],
        pins[15],
        pins[14],
        pins[13],
    )
    row_pins = (
        pins[6],
        pins[7],
        pins[8],
        pins[9],
        pins[10],
    )
    diode_orientation = DiodeOrientation.COL2ROW
    data_pin = pins[1]
    rgb_pixel_pin = pins[0]
    SDA = pins[4]
    SCL = pins[5]

    # flake8: noqa
    # fmt: off
    coord_mapping = [
        0,   1,  2,  3,  4,  5,         40, 39, 38, 37, 36, 35,
        7,   8,  9, 10, 11, 12,         47, 46, 45, 44, 43, 42,
        14, 15, 16, 17, 18, 19,         54, 53, 52, 51, 50, 49,
        21, 22, 23, 24, 25, 26, 27, 62, 61, 60, 59, 58, 57, 56,
        28, 29, 30, 31, 32, 33, 34, 69, 68, 67, 66, 65, 64, 63
    ]
