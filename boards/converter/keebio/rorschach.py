import board

from kmk.extensions.layers import Layers
from kmk.extensions.rgb import RGB
from kmk.extensions.split import Split
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.A2, board.A3, board.A4, board.A5, board.SCK, board.MOSI)
    row_pins = (board.D11, board.D10, board.D9, board.RX, board.D13)
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = board.TX
    uart_pin = board.SCL
    split_type = 'UART'
    split_flip = True
    split_offsets = [6, 6, 6, 6, 6]

    rgb_ext = RGB(pixel_pin=rgb_pixel_pin, num_pixels=12)
    layers_ext = Layers()
    split = Split(uart_pin=uart_pin, split_offsets=split_offsets)
    extensions = [rgb_ext, split, layers_ext]
