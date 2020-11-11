import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.P1_15, board.P0_02, board.P0_29)
    col_pins = (board.P0_09, board.P0_10, board.P1_11, board.P1_13)
    diode_orientation = DiodeOrientation.COLUMNS
    i2c = board.I2C
    powersave_pin = board.P0_13
