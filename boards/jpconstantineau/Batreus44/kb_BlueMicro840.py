import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.P0_15,
        board.P0_17,
        board.P0_20,
        board.P0_13,
        board.P0_24,
        board.P0_09,
        board.P0_03,
        board.P1_13,
        board.P0_02,
        board.P0_29,
        board.P0_26,
        board.P0_30,
    )
    row_pins = (board.P0_28, board.P1_11, board.P0_10, board.P1_06)
    diode_orientation = DiodeOrientation.COL2ROW
