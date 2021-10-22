import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.GP20,
        board.GP19,
        board.GP18,
        board.GP17,
        board.GP16,
        board.GP5,
        board.GP4,
        board.GP3,
        board.GP2,
        board.GP1,
        board.GP0,
    )
    row_pins = (board.GP22, board.GP21, board.GP14, board.GP15)
    diode_orientation = DiodeOrientation.COL2ROW
    rgb_pixel_pin = board.GP28
    rgb_num_pixels = 44
