import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.pins[1], pins[0], board.pins[4], board.pins[5], board.pins[6])
    col_pins = (
        board.pins[19],
        board.pins[18],
        board.pins[17],
        board.pins[16],
        board.pins[15],
        board.pins[14],
        board.pins[13],
        board.pins[12],
        board.pins[11],
        board.pins[10],
        board.pins[9],
        board.pins[8],
    )
    diode_orientation = DiodeOrientation.COLUMNS
    i2c = board.I2C
