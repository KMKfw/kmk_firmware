import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            board.GP3,
            board.GP2,
            board.GP7,
            board.GP8,
            board.GP13,
            board.GP16,
            board.GP17,
            board.GP18,
            board.GP19,
            board.GP20,
        )
        self.row_pins = (
            board.GP0,
            board.GP4,
            board.GP9,
            board.GP14,
        )
        self.diode_orientation = DiodeOrientation.COLUMNS
        # fmt: off
        self.coord_mapping = [
            0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
            10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                        33, 34, 35, 36
        ]
        # fmt: on
