import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.GP18, board.GP1, board.GP4, board.GP5, board.GP6)
    col_pins = (board.GP0, board.GP16, board.GP17)
    diode_orientation = DiodeOrientation.COL2ROW
