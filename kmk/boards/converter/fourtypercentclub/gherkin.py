from kmk.consts import DiodeOrientation
from kmk.mcus.circuitpython_usbhid import KeyboardConfig as _KeyboardConfig
from kmk.pins import Pin as P


class KeyboardConfig(_KeyboardConfig):
    col_pins = (P.D9, P.D10, P.D11, P.D12, P.D13, P.SCL)
    row_pins = (P.A3, P.A4, P.A5, P.SCK, P.MOSI)
    diode_orientation = DiodeOrientation.COLUMNS
