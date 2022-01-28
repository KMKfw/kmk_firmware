import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.D5, board.D6, board.D7, board.D8, board.D9)
    col_pins = (
        board.A1,
        board.A0,
        board.SCK,
        board.MISO,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    i2c = board.I2C
