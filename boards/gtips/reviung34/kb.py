import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.row_pins = (pins[19], pins[18], pins[17], pins[16])
        self.col_pins = (
            pins[6],
            pins[7],
            pins[8],
            pins[9],
            pins[10],
            pins[15],
            pins[14],
            pins[13],
            pins[12],
        )
        self.diode_orientation = DiodeOrientation.COLUMNS
        self.i2c = board.I2C
        self.rgb_pixel_pin = pins[0]
        self.rgb_num_pixels = 9
        self.led_key_pos = [0, 1, 2, 3, 8, 4, 5, 6, 7]
        self.brightness_limit = 1.0
        self.num_pixels = 9
        # fmt: off
        self.coord_mapping = [
            0,  1,  2,  3,  4,  5,  6,  7,  8,  32,
            9,  10, 11, 12, 13, 14, 15, 16, 17, 33,
            18, 19, 20, 21, 22, 23, 24, 25, 26, 34,
                        29, 30, 31, 35,
        ]
        # fmt:on
