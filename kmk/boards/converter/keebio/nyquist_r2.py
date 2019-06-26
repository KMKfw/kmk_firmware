import board

from kmk.consts import DiodeOrientation
from kmk.mcus.circuitpython_samd51 import Firmware as _Firmware
from kmk.pins import Pin as P


class Firmware(_Firmware):
    col_pins = (P.RX, P.A1, P.A2, P.A3, P.A4, P.A5)
    row_pins = (P.D13, P.D11, P.D10, P.D9, P.D7)
    diode_orientation = DiodeOrientation.COLUMNS

    split_type = 'UART'
    split_flip = True
    split_offsets = [6, 6, 6, 6, 6]
    uart_pin = board.SCL
    rgb_pixel_pin = board.TX
    extra_data_pin = board.SDA
