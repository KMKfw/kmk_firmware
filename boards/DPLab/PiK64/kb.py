import board

from kmk.extensions.LED import LED
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            board.GP0,
            board.GP1,
            board.GP16,
            board.GP2,
            board.GP3,
            board.GP4,
            board.GP5,
            board.GP6,
            board.GP7,
            board.GP8,
            board.GP9,
            board.GP10,
            board.GP11,
            board.GP12,
            board.GP13,
            board.GP14,
            board.GP15
        )

        self.row_pins = (
            board.GP18,
            board.GP19,
            board.GP20,
            board.GP21,
            board.GP22
        )

        self.diode_orientation = DiodeOrientation.COLUMNS
