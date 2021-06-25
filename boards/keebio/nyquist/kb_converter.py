import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.RX, board.A1, board.A2, board.A3, board.A4, board.A5)
    row_pins = (board.D13, board.D11, board.D10, board.D9, board.D7)
    diode_orientation = DiodeOrientation.COLUMNS

    data_pin = board.SCL
    rgb_num_pixels = 12
    rgb_pixel_pin = board.TX
    data_pin2 = board.SDA
