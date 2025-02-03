import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.row_pins = (pins[7], pins[8], pins[9], pins[10])
        self.col_pins = (
            pins[17],
            pins[16],
            pins[15],
            pins[14],
            pins[13],
            pins[12],
            pins[10],
        )
        self.diode_orientation = DiodeOrientation.COLUMNS
        self.led_pin = pins[9]
        self.rgb_pixel_pin = pins[0]
        self.rgb_num_pixels = 12
        self.data_pin = pins[1]
        self.i2c = board.I2C

        # fmt: off
        self.coord_mapping = [
             0,  1,  2,  3,  4,  5,  6,  34, 33, 32, 31, 30, 29, 28,
             7,  8,  9, 10, 11, 12, 13,  41, 40, 39, 38, 37, 36, 35,
            14, 15, 16, 17, 18, 19, 20,  48, 47, 46, 45, 44, 43, 42,
            21, 22, 23, 24, 25, 26,          54, 53, 52, 51, 50, 49,
        ]
        # fmt:on
