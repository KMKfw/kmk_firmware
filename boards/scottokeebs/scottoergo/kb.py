import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            board.GP0,
            board.GP1,
            board.GP2,
            board.GP3,
            board.GP4,
            board.GP22,
            board.GP21,
            board.GP20,
            board.GP19,
            board.GP18,
        )
        self.row_pins = (
            board.GP12,
            board.GP13,
            board.GP14,
            board.GP15,
        )
        self.diode_orientation = DiodeOrientation.COLUMNS
        # fmt: off
        self.coord_mapping = [
            0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
            10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                    32, 33, 34, 35, 36, 37
        ]
        # fmt: on
