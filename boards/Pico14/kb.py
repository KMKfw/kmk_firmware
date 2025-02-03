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
        )

        self.row_pins = (
            board.GP18,
            board.GP19,
            board.GP20,
            board.GP21,
            board.GP22,
        )

        self.diode_orientation = DiodeOrientation.COLUMNS
        self.led_pin = board.GP27
