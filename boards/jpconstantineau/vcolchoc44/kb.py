import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.COL1,
        board.COL2,
        board.COL3,
        board.COL4,
        board.COL5,
        board.COL6,
        board.COL7,
        board.COL8,
        board.COL9,
        board.COL10,
        board.COL11,
    )
    row_pins = (board.ROW1, board.ROW2, board.ROW3, board.ROW4)
    diode_orientation = DiodeOrientation.COL2ROW
    rgb_pixel_pin = board.NEOPIXEL
    rgb_num_pixels = 44
