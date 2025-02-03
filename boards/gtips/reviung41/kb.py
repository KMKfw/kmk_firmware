import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            pins[6],
            pins[7],
            pins[8],
            pins[9],
            pins[10],
            pins[11],
        )
        self.row_pins = (
            pins[19],
            pins[18],
            pins[17],
            pins[16],
            pins[15],
            pins[14],
            pins[13],
        )
        self.diode_orientation = DiodeOrientation.COLUMNS
        self.rgb_pixel_pin = pins[0]
        self.rgb_num_pixels = 11
        self.i2c = board.I2C

        # fmt: off
        self.coord_mapping = [
                  0,  1,  2,  3,  4,  5,   6,  7,  8,  9, 10, 11,
                12, 13, 14, 15, 16, 17,     18, 19, 20, 21, 22, 23,
               24, 25, 26, 27, 28, 29,       30, 31, 32, 33, 34, 35,
                             36,   37,  38,  39,   40,
        ]
        # fmt: on
