import board

from kmk.consts import DiodeOrientation
from kmk.mcus.circuitpython_samd51 import Firmware as _Firmware
from kmk.pins import Pin as P


class Firmware(_Firmware):
    col_pins = (P.RX, P.D13, P.A0, P.D11, P.A4, P.A5, P.D10, P.D9, P.SCK)
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = board.TX
