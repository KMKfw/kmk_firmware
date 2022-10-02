import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (pins[16], pins[17], pins[18])
    col_pins = (pins[12], pins[13], pins[14], pins[15])
    diode_orientation = DiodeOrientation.COLUMNS
    i2c = board.I2C
