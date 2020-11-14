import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.A2, board.A3, board.A4, board.A5, board.SCK, board.MOSI)
    row_pins = (board.D13, board.D11, board.D10, board.D9)
    diode_orientation = DiodeOrientation.COLUMNS

    split_type = 'UART'
    split_flip = True
    split_offsets = [6, 6, 6, 6, 6]
    data_pin = board.SCL
    data_pin2 = board.SDA
    rgb_pixel_pin = board.TX
    led_pin = board.D7
