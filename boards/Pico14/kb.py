import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.GP0,
        board.GP1,
        board.GP2,
    )

    row_pins = (
        board.GP18,
        board.GP19,
        board.GP20,
        board.GP21,
        board.GP22,
    )

    diode_orientation = DiodeOrientation.COLUMNS
    led_pin = board.GP27
