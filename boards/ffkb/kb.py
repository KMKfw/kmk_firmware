import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.matrix import intify_coordinate as ic


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.D9,
        board.D8,
        board.D7,
        board.D6,
        board.D5,
        board.D4,
        board.MOSI,
        board.MISO,
    )
    row_pins = (
        board.D1,
        board.A3,
        board.A2,
        board.A1,
        board.A0,
        board.SCK,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = board.D0
    rgb_num_pixels = 42
    i2c = board.I2C

    coord_mapping = [
            (0,0), (0,1), (0,2), (0,3), (0,4), (0,5),        (0,6), (0,7), (4,3), (3,4), (4,5), (3,7),
            (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (4,1), (1,6), (1,7), (3,2), (4,4), (3,5), (4,7),
            (2,0), (2,1), (2,2), (2,3), (2,4), (2,5),        (2,6), (2,7), (4,2), (3,3), (3,6), (4,6),
                          (5,1), (5,3), (5,4), (5,5),        (5,6), (5,7), (5,2), (5,0)
    ]
