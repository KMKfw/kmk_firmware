import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (board.A2, board.A3, board.A4, board.A5, board.SCK, board.MOSI)
        self.row_pins = (board.D13, board.D11, board.D10, board.D9)
        self.diode_orientation = DiodeOrientation.COLUMNS

        self.split_type = 'UART'
        self.split_flip = True
        self.split_offsets = [6, 6, 6, 6, 6]
        self.data_pin = board.SCL
        self.data_pin2 = board.SDA
        self.rgb_pixel_pin = board.TX
        self.led_pin = board.D7
