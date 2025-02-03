import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.row_pins = (board.D5, board.D6, board.D7, board.D8, board.D9)
        self.col_pins = (
            board.A1,
            board.A0,
            board.SCK,
            board.MISO,
        )
        self.diode_orientation = DiodeOrientation.COLUMNS
        self.i2c = board.I2C
