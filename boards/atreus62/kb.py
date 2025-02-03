import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            board.D24,
            board.D25,
            board.D26,
            board.D27,
            board.D28,
            board.D29,
            board.D30,
            board.D31,
            board.D32,
            board.D33,
            board.D34,
            board.D35,
        )

        self.row_pins = (board.D3, board.D4, board.D5, board.D6, board.D7, board.D8)

        self.diode_orientation = DiodeOrientation.ROWS
        # self.diode_orientation = DiodeOrientation.COLUMNS
