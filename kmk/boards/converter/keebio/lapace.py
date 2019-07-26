import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.SDA,
        board.A2,
        board.A3,
        board.A4,
        board.A5,
        board.SCK,
        board.MOSI,
    )
    row_pins = (
        board.TX,
        board.A0,
        board.RX,
        board.A1,
        board.D11,
        board.D9,
        board.D12,
        board.D10,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = board.D13
