import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            pins[11],
            pins[10],
            pins[9],
            pins[8],
            pins[7],
            pins[6],
            pins[10],
            pins[12],
        )
        self.row_pins = (
            pins[1],
            pins[19],
            pins[18],
            pins[17],
            pins[16],
            pins[15],
        )
        self.diode_orientation = DiodeOrientation.COLUMNS
        self.rgb_pixel_pin = pins[0]
        self.rgb_num_pixels = 42
        self.i2c = board.I2C

        # fmt: off
        self.coord_mapping = [
           0,   1,  2,  3,  4,  5,      6,  7, 35, 28, 37, 31,
           8,   9, 10, 11, 12, 13, 33, 14, 15, 26, 36, 29, 39,
           16, 17, 18, 19, 20, 21,     22, 23, 34, 27, 30, 38,
           41,         43, 44, 45,     46, 47, 42,         40,
        ]
        # fmt: on
