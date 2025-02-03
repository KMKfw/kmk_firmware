import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            board.GP6,
            board.GP7,
            board.GP8,
            board.GP9,
            board.GP10,
            board.GP18,
            board.GP19,
            board.GP20,
            board.GP21,
            board.GP22,
        )
        self.row_pins = (
            board.GP14,
            board.GP15,
            board.GP16,
            board.GP17,
        )
        self.diode_orientation = DiodeOrientation.COL2ROW
