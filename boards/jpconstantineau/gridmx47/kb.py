import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.GP11,
        board.GP12,
        board.GP13,
        board.GP14,
        board.GP15,
        board.GP19,
        board.GP20,
        board.GP21,
        board.GP22,
        board.GP26,
        board.GP27,
        board.GP28,
    )
    row_pins = (board.GP7, board.GP8, board.GP9, board.GP10)
    diode_orientation = DiodeOrientation.COL2ROW
    rgb_pixel_pin = board.GP6
    rgb_num_pixels = 47
