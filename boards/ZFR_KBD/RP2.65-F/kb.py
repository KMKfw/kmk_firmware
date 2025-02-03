import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            board.COL0,
            board.COL1,
            board.COL2,
            board.COL3,
            board.COL4,
            board.COL5,
            board.COL6,
            board.COL7,
        )
        self.row_pins = (
            board.ROW0,
            board.ROW1,
            board.ROW2,
            board.ROW3,
            board.ROW4,
            board.ROW5,
            board.ROW6,
            board.ROW7,
            board.ROW8,
            board.ROW9,
        )
        self.diode_orientation = DiodeOrientation.COL2ROW
        self.rgb_pixel_pin = board.LED
        self.rgb_num_pixels = 70

        # fmt:off
        self.coord_mapping = [
             0,  8,  1,  9,  2, 10,  3, 11,
             4, 12,  5, 13,  6, 14,  7, 15,
            24, 17, 25, 18, 26, 19, 27, 20,
            28, 21, 29, 22, 23, 31, 40, 33,
            41, 34, 42, 35, 43, 36, 44, 37,
            45, 38, 46, 39, 47, 56, 49, 57,
            50, 58, 51, 59, 52, 60, 53, 61,
            54, 55, 63, 72, 65, 73, 74, 75,
            76, 69, 77, 78, 71, 79,
        ]
        # fmt:on
