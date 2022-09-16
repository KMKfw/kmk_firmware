import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.scanners.encoder import RotaryioEncoder
from kmk.scanners.keypad import MatrixScanner


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        # create and register the scanner
        self.matrix = [
            MatrixScanner(
                # required arguments:
                column_pins = self.col_pins,
                row_pins = self.row_pins,
                # optional arguments with defaults:
                columns_to_anodes=DiodeOrientation.COL2ROW,
                interval=0.02,
                max_events=64
            ),
            RotaryioEncoder(
                pin_a=board.GP08,
                pin_b=board.GP09,
                # optional
                divisor=4,
            )
        ]
    col_pins = (
        board.GP02,
        board.GP03,
        board.GP04,
        board.GP05,
        board.GP06,
        board.GP07,
    )
    row_pins = (board.GP14, board.GP15, board.GP16, board.GP17, board.GP18)
    diode_orientation = DiodeOrientation.COLUMNS
    rx = board.RX
    tx = board.TX
    rgb_pixel_pin = board.GP29
    i2c = board.I2C
    data_pin = board.RX
    rgb_pixel_pin = board.GP29
    i2c = board.I2C
    SCL=board.SCL
    SDA=board.SDA
    encoder_a=board.GP08
    encoder_b=board.GP09
    # NOQA
    # flake8: noqa
    led_key_pos =[11,10,9 ,8 ,7 ,6 ,      41,42,43,44,45,46,
                12,13,14,15,16,17,      52,51,50,49,48,47,
                23,22,21,20,19,18,      53,54,55,56,57,58,
                24,25,26,27,28,29,30,65,64,63,62,61,60,59,
                         34,33,32,31,66,67,68,69,
                         3 ,4 ,5 ,      40,39,38,
                         2 ,1 ,0 ,      35,36,37
                         ]
    brightness_limit = 0.5
    num_pixels = 70

    # NOQA
    # flake8: noqa
    coord_mapping = [
     0,  1,  2,  3,  4,  5,         37, 36, 35, 34, 33, 32,
     6,  7,  8,  9, 10, 11,         43, 42, 41, 40, 39, 38,
    12, 13, 14, 15, 16, 17,         49, 48, 47, 46, 45, 44,
    18, 19, 20, 21, 22, 23, 29, 61, 55, 54, 53, 52, 51, 50,
             25,26, 27, 28,         60, 59, 58, 57,
                    30,31,          62,63 
    ]

