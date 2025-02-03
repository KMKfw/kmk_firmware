import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (board.RX, board.A1, board.A2, board.A3, board.A4, board.A5)
        self.row_pins = (board.D13, board.D11, board.D10, board.D9, board.D7)
        self.diode_orientation = DiodeOrientation.COLUMNS

        self.data_pin = board.SCL
        self.rgb_num_pixels = 12
        self.rgb_pixel_pin = board.TX
        self.data_pin2 = board.SDA
