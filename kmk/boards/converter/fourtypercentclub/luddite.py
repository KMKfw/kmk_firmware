import board

from kmk.extensions.layers import Layers
from kmk.extensions.rgb import RGB
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
        board.D13,
        board.D12,
        board.D11,
        board.D10,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = board.D9
    rgb_num_pixels = 12
    rgb_ext = RGB(pixel_pin=board.TX, num_pixels=12)
    layers_ext = Layers()
    extensions = [rgb_ext, layers_ext]
