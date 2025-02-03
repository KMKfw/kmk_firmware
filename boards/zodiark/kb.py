import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.avr_promicro import translate as avr
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation
from kmk.scanners.keypad import MatrixScanner


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            pins[avr['F5']],
            pins[avr['F6']],
            pins[avr['F7']],
            pins[avr['B1']],
            pins[avr['B3']],
            pins[avr['B2']],
            pins[avr['B6']],
        )
        self.row_pins = (
            pins[avr['C6']],
            pins[avr['D7']],
            pins[avr['E6']],
            pins[avr['B4']],
            pins[avr['F4']],
        )
        self.diode_orientation = DiodeOrientation.COLUMNS
        self.rgb_pixel_pin = pins[avr['B5']]
        self.data_pin = pins[avr['D3']]
        self.i2c = board.I2C
        self.SCL = board.SCL
        self.SDA = board.SDA

        # fmt: off
        self.led_key_pos = [
             5,  4,  3,  2,  1, 00,                 34, 35, 36, 37, 38, 39,
             6,  7,  8,  9, 10, 11, 12,         46, 45, 44, 43, 42, 41, 40,
            19, 18, 17, 16, 15, 14, 13,         47, 48, 49, 50, 51, 52, 53,
            20, 21, 22, 23, 24, 25, 26,         60, 59, 58, 57, 56, 55, 54,
            33, 32, 31, 30, 29,     28, 27, 61, 62,     63, 64, 65, 66, 67
        ]
        # fmt:on
        self.brightness_limit = 0.5
        self.num_pixels = 62

        # fmt:off
        self.coord_mapping = [
             0,  1,  2,  3,  4,  5,                 40, 39, 38, 37, 36, 35,
             7,  8,  9, 10, 11, 12,  6,         41, 47, 46, 45, 44, 43, 42,
            14, 15, 16, 17, 18, 19, 13,         48, 54, 53, 52, 51, 50, 49,
            21, 22, 23, 24, 25, 26, 20, 27, 62, 55, 61, 60, 59, 58, 57, 56,
            28, 29, 30, 31, 32,     33, 34, 69, 68,     67, 66, 65, 64, 63
        ]
        # fmt:on

        # create and register the scanner
        self.matrix = [
            MatrixScanner(
                # required arguments:
                column_pins=self.col_pins,
                row_pins=self.row_pins,
                # optional arguments with defaults:
                columns_to_anodes=DiodeOrientation.COL2ROW,
                interval=0.02,
                max_events=64,
            ),
        ]
