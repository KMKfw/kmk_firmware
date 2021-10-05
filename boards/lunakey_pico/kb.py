import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.matrix import intify_coordinate as ic


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.GP12, board.GP13, board.GP14, board.GP15)
    col_pins = (board.GP21, board.GP20, board.GP19, board.GP18, board.GP17, board.GP16)
    diode_orientation = DiodeOrientation.COLUMNS

    coord_mapping = []
    coord_mapping.extend(ic(0, x) for x in range(12))
    coord_mapping.extend(ic(1, x) for x in range(12))
    coord_mapping.extend(ic(2, x) for x in range(12))
    coord_mapping.extend(ic(3, x) for x in range(2, 10))
