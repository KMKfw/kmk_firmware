import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.matrix import intify_coordinate as ic


class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.P0_31, board.P0_29, board.P0_02, board.P1_15, board.P1_13)
    row_pins = (board.P0_10, board.P0_09, board.P1_04, board.P1_06)
    diode_orientation = DiodeOrientation.COLUMNS
    data_pin = board.P0_08
    rgb_pixel_pin = board.P0_06
    rgb_num_pixels = 12
    i2c = board.I2C
    powersave_pin = board.P0_13

    coord_mapping = []
    coord_mapping.extend(ic(0, x) for x in range(10))
    coord_mapping.extend(ic(1, x) for x in range(10))
    coord_mapping.extend(ic(2, x) for x in range(10))

    # And now, to handle R3, which at this point is down to just six keys
    coord_mapping.extend(ic(3, x) for x in range(3, 9))
