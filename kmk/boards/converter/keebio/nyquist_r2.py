import board

from kmk.extensions.rgb import RGB
from kmk.extensions.split import Split
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.RX, board.A1, board.A2, board.A3, board.A4, board.A5)
    row_pins = (board.D13, board.D11, board.D10, board.D9, board.D7)
    diode_orientation = DiodeOrientation.COLUMNS

    split_type = 'UART'
    split_flip = True
    split_offsets = [6, 6, 6, 6, 6]
    uart_pin = board.SCL
    rgb_pixel_pin = board.TX
    extra_data_pin = board.SDA
    rgb_ext = RGB(
        pixel_pin=board.TX,
        num_pixels=12,
        val_limit=150,
        hue_step=10,
        sat_step=5,
        val_step=5,
        hue_default=260,
        sat_default=100,
        val_default=40,
        animation_speed=1,
    )
    split = Split(uart_pin=board.SCL, split_offsets=[6, 6, 6, 6, 6])
    extensions = [rgb_ext, split]
