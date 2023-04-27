import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.D6,
        board.D8,
        board.D9,
    )
    row_pins = (
        board.D1,
        board.D2,
        board.D3,
        board.D7,
    )
    diode_orientation = DiodeOrientation.COL2ROW
