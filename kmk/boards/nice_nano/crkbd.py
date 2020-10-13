import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.matrix import intify_coordinate as ic


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.P0_31,
        board.P0_29,
        board.P0_02,
        board.P1_15,
        board.P1_13,
        board.P1_11,
    )
    row_pins = (board.P0_22, board.P0_24, board.P1_00, board.P0_11)
    diode_orientation = DiodeOrientation.COLUMNS

    split_type = 'UART'  # TODO add bluetooth support as well
    split_flip = True
    split_offsets = [6, 6, 6, 6, 6]
    uart_pin = board.P0_08
    rgb_pixel_pin = board.P0_06
    extra_data_pin = board.SDA  # TODO This is incorrect. Find better solution

    coord_mapping = []
    coord_mapping.extend(ic(0, x) for x in range(12))
    coord_mapping.extend(ic(1, x) for x in range(12))
    coord_mapping.extend(ic(2, x) for x in range(12))

    # And now, to handle R3, which at this point is down to just six keys
    coord_mapping.extend(ic(3, x) for x in range(3, 9))
