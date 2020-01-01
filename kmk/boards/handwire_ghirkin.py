import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.SDA, board.A0, board.A1, board.A3, board.A2, board.A4)
    row_pins = (board.MOSI, board.MISO, board.RX, board.TX, board.D2)
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = None
    rgb_num_pixels = 0
