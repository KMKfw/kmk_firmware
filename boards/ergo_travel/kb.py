import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.matrix import intify_coordinate as ic


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.P0_24, board.P1_00, board.P0_11, board.P1_04)
    col_pins = (
        board.P0_29,
        board.P0_02,
        board.P1_15,
        board.P1_13,
        board.P1_11,
        board.P0_10,
        board.P0_09,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    led_pin = board.P1_06
    rgb_pixel_pin = board.P0_06
    rgb_num_pixels = 12
    data_pin = board.P0_08
    i2c = board.I2C
    powersave_pin = board.P0_13

    # NOQA
    coord_mapping = []
    coord_mapping.extend(ic(0, x, 7) for x in range(7))
    coord_mapping.extend(ic(4, x, 7) for x in range(7))
    coord_mapping.extend(ic(1, x, 7) for x in range(7))
    coord_mapping.extend(ic(5, x, 7) for x in range(7))
    coord_mapping.extend(ic(2, x, 7) for x in range(7))
    coord_mapping.extend(ic(6, x, 7) for x in range(7))

    # And now, to handle R3, which at this point is down to just six keys
    coord_mapping.extend(ic(3, x, 7) for x in range(0, 6))
    coord_mapping.extend(ic(7, x, 7) for x in range(1, 7))
