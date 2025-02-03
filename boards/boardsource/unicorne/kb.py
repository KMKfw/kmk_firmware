import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            board.GP02,
            board.GP03,
            board.GP04,
            board.GP05,
            board.GP06,
            board.GP07,
        )
        self.row_pins = (board.GP14, board.GP15, board.GP16, board.GP17)
        self.diode_orientation = DiodeOrientation.COLUMNS
        self.rx = board.RX
        self.tx = board.TX
        self.rgb_pixel_pin = board.GP29
        self.i2c = board.I2C
        self.swap_x = False
        self.swap_y = True
        self.SCL = board.SCL
        self.SDA = board.SDA
        # fmt:off
        self.led_key_pos = [
            24, 23, 18, 17, 10, 9, 36, 37, 44, 45, 50, 51,
            25, 22, 19, 16, 11, 8, 35, 38, 43, 46, 49, 52,
            26, 21, 20, 15, 12, 7, 34, 39, 42, 47, 48, 53,
            14, 13, 6, 33, 40, 41,
            2, 1, 0, 27, 28, 29, 3, 4, 5, 32, 31, 30,
        ]
        # fmt:on

        self.brightness_limit = 0.5
        self.num_pixels = 54
        # fmt:off
        self.coord_mapping = [
            0,  1,  2,  3,  4,  5,  29, 28, 27, 26, 25, 24,
            6,  7,  8,  9, 10, 11,  35, 34, 33, 32, 31, 30,
            12, 13, 14, 15, 16, 17,  41, 40, 39, 38, 37, 36,
            21, 22, 23,  47, 46, 45,
        ]
        # fmt:on
