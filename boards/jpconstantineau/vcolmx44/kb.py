import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            board.GP20,
            board.GP19,
            board.GP18,
            board.GP17,
            board.GP16,
            board.GP5,
            board.GP4,
            board.GP3,
            board.GP2,
            board.GP1,
            board.GP0,
        )
        self.row_pins = (board.GP22, board.GP21, board.GP14, board.GP15)
        self.diode_orientation = DiodeOrientation.COL2ROW
        self.rgb_pixel_pin = board.GP28
        self.rgb_num_pixels = 44
