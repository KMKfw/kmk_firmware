import board

from kmk.consts import DiodeOrientation
from kmk.mcus.circuitpython_usbhid import KeyboardConfig as _KeyboardConfig


class KeyboardConfig(_KeyboardConfig):
    col_pins = (board.A2, board.A3, board.A4, board.A5, board.SCK, board.MOSI)
    row_pins = (board.D13, board.D11, board.D10, board.D9)
    diode_orientation = DiodeOrientation.COLUMNS

    split_type = 'UART'
    split_flip = True
    split_offsets = [6, 6, 6, 6, 6]
    uart_pin = board.SCL
    extra_data_pin = board.SDA
    rgb_pixel_pin = board.TX
    # led_pin = board.D7
