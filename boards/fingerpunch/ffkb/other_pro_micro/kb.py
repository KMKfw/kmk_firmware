import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation
from kmk.scanners import intify_coordinate as ic


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        pins[11],
        pins[10],
        pins[9],
        pins[8],
        pins[7],
        pins[6],
        pins[10],
        pins[12],
    )
    row_pins = (
        pins[1],
        pins[19],
        pins[18],
        pins[17],
        pins[16],
        pins[15],
    )
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = pins[0]
    rgb_num_pixels = 42
    i2c = board.I2C

    # flake8: noqa
    # fmt: off
    coord_mapping = [
            ic(0, 0), ic(0, 1), ic(0, 2), ic(0, 3), ic(0, 4), ic(0, 5),           ic(0, 6), ic(0, 7), ic(4, 3), ic(3, 4), ic(4, 5), ic(3, 7),
            ic(1, 0), ic(1, 1), ic(1, 2), ic(1, 3), ic(1, 4), ic(1, 5), ic(4, 1), ic(1, 6), ic(1, 7), ic(3, 2), ic(4, 4), ic(3, 5), ic(4, 7),
            ic(2, 0), ic(2, 1), ic(2, 2), ic(2, 3), ic(2, 4), ic(2, 5),           ic(2, 6), ic(2, 7), ic(4, 2), ic(3, 3), ic(3, 6), ic(4, 6),
            ic(5, 1),                     ic(5, 3), ic(5, 4), ic(5, 5),           ic(5, 6), ic(5, 7), ic(5, 2),                     ic(5, 0)
    ]
