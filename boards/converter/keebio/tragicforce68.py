import board

from kmk.extensions.layers import Layers
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.A0,
        board.A1,
        board.A2,
        board.A3,
        board.A4,
        board.A5,
        board.SCK,
        board.MOSI,
    )
    row_pins = (
        board.TX,
        board.RX,
        board.SDA,
        board.SCL,
        board.D9,
        board.D10,
        board.D12,
        board.D11,
        board.D13,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    layers_ext = Layers()
    extensions = [layers_ext]
