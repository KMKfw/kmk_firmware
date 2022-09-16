import board

from kmk.extensions.LED import LED
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.GP0,
        board.GP1,
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
        board.GP6,
        board.GP7,
        board.GP8,
        board.GP9,
        board.GP10,
        board.GP11,
        board.GP12,
        board.GP13,
        board.GP14,
        board.GP15,
        board.GP16,
        board.GP17,
    )

    row_pins = (
        board.GP18,
        board.GP19,
        board.GP20,
        board.GP21,
        board.GP22,
        board.GP26,
    )

    diode_orientation = DiodeOrientation.COLUMNS

    leds = LED(led_pin=[board.GP27, board.GP28])
    _KMKKeyboard.extensions.append(leds)
