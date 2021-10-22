import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
<<<<<<< HEAD
    col_pins = (
=======
    row_pins = (
>>>>>>> 9e830a1 (adding jpconstantineau's boards)
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
<<<<<<< HEAD
    row_pins = (board.GP22, board.GP21, board.GP14, board.GP15)
=======
    col_pins = (board.GP22, board.GP21, board.GP14, board.GP15)
>>>>>>> 9e830a1 (adding jpconstantineau's boards)
    diode_orientation = DiodeOrientation.COL2ROW
    rgb_pixel_pin = board.GP28
    rgb_num_pixels = 44
