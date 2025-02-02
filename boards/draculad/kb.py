import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.avr_promicro import translate as avr
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation
from kmk.scanners.keypad import MatrixScanner

# from kmk.scanners.encoder import RotaryioEncoder


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            pins[avr['F4']],
            pins[avr['F5']],
            pins[avr['F6']],
            pins[avr['F7']],
            pins[avr['B1']],
        )
        self.row_pins = (
            pins[avr['D4']],
            pins[avr['C6']],
            pins[avr['D7']],
            pins[avr['E6']],
        )
        self.data_pin = pins[avr['D2']]
        self.rgb_pixel_pin = pins[avr['D3']]
        self.rgb_num_pixels = 20
        self.i2c = board.I2C
        self.SCL = pins[5]
        self.SDA = pins[4]
        self.pin_a1 = pins[avr['B2']]
        self.pin_a2 = pins[avr['B4']]
        self.pin_b1 = pins[avr['B6']]
        self.pin_b2 = pins[avr['B5']]
        # fmt: off
        self.led_key_pos = [
             5,  6,  7,  8,  9, 19, 18, 17, 16, 15,
            14, 13, 12, 11, 10,  0,  1,  2,  3,  4
        ]
        # fmt: on
        self.brightness_limit = 1.0
        self.num_pixels = 20

        # fmt: off
        self.coord_mapping = [
            0,  1,  2,  3,  4,  24, 23, 22, 21, 20,
            5,  6,  7,  8,  9,  29, 28, 27, 26, 25,
            10, 11, 12, 13, 14,  34, 33, 32, 31, 30,
                    17, 18, 19,  39, 38, 37
        ]
        # fmt: on

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
            # RotaryioEncoder(
            #     pin_a=self.pin_a1,
            #     pin_b=self.pin_b1,
            #     # optional
            #     divisor=4,
            # ),
            #  RotaryioEncoder(
            #     pin_a=self.pin_a2,
            #     pin_b=self.pin_b2,
            #     # optional
            #     divisor=4,
            # )
        ]
