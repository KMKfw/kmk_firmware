import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.RX,
        board.D13,
        board.A0,
        board.D11,
        board.A4,
        board.A5,
        board.D10,
        board.D9,
        board.SCK,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = board.TX
