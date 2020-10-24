import board

from kmk.extensions.layers import Layers
from kmk.extensions.rgb import RGB
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

    rgb_ext = RGB(pixel_pin=rgb_pixel_pin, num_pixels=9)
    layers_ext = Layers()
    extensions = [rgb_ext, layers_ext]
