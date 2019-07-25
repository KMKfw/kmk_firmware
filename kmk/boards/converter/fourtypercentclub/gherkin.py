import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.D9, board.D10, board.D11, board.D12, board.D13, board.SCL)
    row_pins = (board.A3, board.A4, board.A5, board.SCK, board.MOSI)
    diode_orientation = DiodeOrientation.COLUMNS
