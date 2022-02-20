import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.matrix import intify_coordinate as ic


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.A3,
        board.A2,
        board.A1,
        board.A0,
        board.SCK,
        board.MISO,
        board.MOSI,
        board.D10,
    )
    row_pins = (board.D8, board.D7, board.D6, board.D4)
    diode_orientation = DiodeOrientation.COL2ROW
    data_pin = board.D1
    rgb_pixel_pin = board.D0
    encoder_pin_0 = board.D9
    encoder_pin_1 = board.D5

    coord_mapping = []
    coord_mapping.extend(ic(0, x, 8) for x in range(6))
    coord_mapping.extend(ic(4, x, 8) for x in range(5, -1, -1))
    coord_mapping.extend(ic(1, x, 8) for x in range(6))
    coord_mapping.extend(ic(5, x, 8) for x in range(5, -1, -1))
    coord_mapping.extend(ic(2, x, 8) for x in range(8))
    coord_mapping.extend(ic(6, x, 8) for x in range(7, -1, -1))
    coord_mapping.extend(ic(3, x, 8) for x in range(3, 8))
    coord_mapping.extend(ic(7, x, 8) for x in range(7, 2, -1))
