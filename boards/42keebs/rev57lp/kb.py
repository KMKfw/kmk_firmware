import board

from kmk.kmk_keyboard import KMKKeyboard as Rev57LP
from kmk.scanners import DiodeOrientation


class KMKKeyboard(Rev57LP):
    def __init__(self):
        super().__init__()

        self.row_pins = (
            board.D0,
            board.D1,
            board.MOSI,
            board.D2,
            board.D21,
        )

        self.col_pins = (
            board.A3,
            board.A2,
            board.A1,
            board.A0,
            board.SCK,
            board.MISO,
            board.D4,
            board.D5,
            board.D6,
            board.D7,
            board.D8,
            board.D9,
        )

        self.diode_orientation = DiodeOrientation.COL2ROW

        self.has_underglow = True
        self.underglow_pin = board.D3
        self.underglow_led_number = 9
        '''
        60mA draws 1 LED at max brightness (255)
        450mA is USB2.0 max current (-50mA for safety)
        so
        450mA / 9 leds = 50mA/led - max current per LED

        60mA → 255 (max value for brightness)
        50mA → x
        x = 50mA/60mA * 255
        x = 212 (roughly 200)
        '''
        self.underglow_max_brightness = 200

        # self.unicode_mode = 1

        # fmt: off
        self.coord_mapping = [
           0,  1,  2,  3,  4,  5,          6,  7,  8,  9, 10, 11,
          12, 13, 14, 15, 16, 17,         18, 19, 20, 21, 22, 23,
          24, 25, 26, 27, 28, 29,   55,   30, 31, 32, 33, 34, 35,
          36, 37, 38, 39, 40, 41,         42, 43, 44, 45, 46, 47,
                      50, 51, 52, 53, 54, 56, 57, 58,
        ]
        # fmt: on
