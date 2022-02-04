import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.matrix import intify_coordinate as ic


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.GP12, board.GP13, board.GP14, board.GP15)
    col_pins = (board.GP21, board.GP20, board.GP19, board.GP18, board.GP17, board.GP16)
    diode_orientation = DiodeOrientation.COLUMNS

    coord_mapping = []
    coord_mapping.extend(ic(0, x, 6) for x in range(6))
    coord_mapping.extend(ic(4, x, 6) for x in range(6))
    coord_mapping.extend(ic(1, x, 6) for x in range(6))
    coord_mapping.extend(ic(5, x, 6) for x in range(6))
    coord_mapping.extend(ic(2, x, 6) for x in range(6))
    coord_mapping.extend(ic(6, x, 6) for x in range(6))

    # And now, to handle R3, which at this point is down to just six keys
    coord_mapping.extend(ic(3, x, 6) for x in range(2, 6))
    coord_mapping.extend(ic(7, x, 6) for x in range(0, 4))
