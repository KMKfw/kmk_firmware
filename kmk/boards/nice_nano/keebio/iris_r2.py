import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.matrix import intify_coordinate as ic


class KMKKeyboard(_KMKKeyboard):
    # Pin mappings for converter board found at hardware/README.md
    # QMK: MATRIX_COL_PINS { F6, F7, B1, B3, B2, B6 }
    # QMK: MATRIX_ROW_PINS { D7, E6, B4, D2, D4 }
    row_pins = (board.P1_00, board.P0_11, board.P1_04, board.P0_08, board.P0_22)
    col_pins = (board.P0_02, board.P1_15, board.P1_13, board.P1_11, board.P0_10, board.P0_09)
    diode_orientation = DiodeOrientation.COLUMNS

    split_flip = True
    split_offsets = (6, 6, 6, 6, 6)
    split_type = 'UART'
    uart_pin = board.P0_20
    extra_data_pin = None
    rgb_pixel_pin = board.P0_06
    led_pin = board.P1_06

    coord_mapping = []
    coord_mapping.extend(ic(0, x) for x in range(12))
    coord_mapping.extend(ic(1, x) for x in range(12))
    coord_mapping.extend(ic(2, x) for x in range(12))

    # Buckle up friends, the bottom row of this keyboard is wild, and making
    # our layouts match, visually, what the keyboard looks like, requires some
    # surgery on the bottom two rows of coords

    # Row index 3 is actually perfectly sane and we _could_ expose it
    # just like the above three rows, however, visually speaking, the
    # top-right thumb cluster button (when looking at the left-half PCB)
    # is more inline with R3, so we'll jam that key (and its mirror) in here
    coord_mapping.extend(ic(3, x) for x in range(6))
    coord_mapping.append(ic(4, 2))
    coord_mapping.append(ic(4, 9))
    coord_mapping.extend(ic(3, x) for x in range(6, 12))  # Now, the rest of R3

    # And now, to handle R4, which at this point is down to just six keys
    coord_mapping.extend(ic(4, x) for x in range(3, 9))
