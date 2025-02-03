import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            board.COL1,
            board.COL2,
            board.COL3,
            board.COL4,
            board.COL5,
            board.COL6,
            board.COL7,
            board.COL8,
            board.COL9,
            board.COL10,
            board.COL11,
            board.COL12,
            board.COL13,
            board.COL14,
        )
        self.row_pins = (board.ROW1, board.ROW2, board.ROW3, board.ROW4, board.ROW5)
        self.diode_orientation = DiodeOrientation.COL2ROW
        self.rgb_pixel_pin = board.NEOPIXEL
        self.rgb_num_pixels = 61
