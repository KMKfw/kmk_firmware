import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
# change this to match your MCU board
from kmk.quickpin.pro_micro.nice_nano import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (pins[19], pins[17], pins[16], pins[15], pins[13], pins[10], pins[9], pins[8], pins[7], pins[1])
    row_pins = (pins[18], pins[6], pins[14], pins[12], pins[11])
    diode_orientation = DiodeOrientation.COL2ROW
    # NOQA
    # flake8: noqa
    coord_mapping = [
     0,  1,  2,  3,  4, 15, 16, 17, 18, 19,
    20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
    30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
            42, 43, 44, 45, 46, 47
    ]
