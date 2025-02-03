import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            board.GP11,
            board.GP12,
            board.GP13,
            board.GP14,
            board.GP15,
            board.GP19,
            board.GP20,
            board.GP21,
            board.GP22,
            board.GP26,
            board.GP27,
            board.GP28,
        )
        self.row_pins = (board.GP7, board.GP8, board.GP9, board.GP10)
        self.diode_orientation = DiodeOrientation.COL2ROW
        self.rgb_pixel_pin = board.GP6
        self.rgb_num_pixels = 47
