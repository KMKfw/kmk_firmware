from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.sparkfun_promicro_rp2040 import (
    pinout as pins,  # change this to match your MCU board
)
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (pins[17], pins[16], pins[15], pins[14], pins[13], pins[12])
        self.row_pins = (pins[7], pins[8], pins[9], pins[10], pins[11])
        self.diode_orientation = DiodeOrientation.COL2ROW
        self.encoder_pin_0 = pins[18]
        self.encoder_pin_1 = pins[19]
        # fmt:off
        self.coord_mapping = [
             0,  1,  2,  3,  4,  5,    35, 34, 33, 32, 31, 30,
             6,  7,  8,  9, 10, 11,    41, 40, 39, 38, 37, 36,
            12, 13, 14, 15, 16, 17,    47, 46, 45, 44, 43, 42,
            18, 19, 20, 21, 22, 23,    53, 52, 51, 50, 49, 48,
            24, 25, 26, 27, 28, 29,    59, 58, 57, 56, 55, 54
        ]
        # fmt:on
