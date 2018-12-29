import board

from kmk.consts import DiodeOrientation
from kmk.mcus.circuitpython_samd51 import Firmware as _Firmware
from kmk.pins import Pin as P


class Firmware(_Firmware):
    # Pin mappings for converter board found at hardware/README.md
    # QMK: MATRIX_COL_PINS { F6, F7, B1, B3, B2, B6 }
    # QMK: MATRIX_ROW_PINS { D7, E6, B4, D2, D4 }
    col_pins = (P.A2, P.A3, P.A4, P.A5, P.SCK, P.MOSI)
    row_pins = (P.D11, P.D10, P.D9, P.RX, P.D13)
    diode_orientation = DiodeOrientation.COLUMNS

    split_flip = True
    split_offsets = (6, 6, 6, 6, 6)
    split_type = "UART"
    uart_pin = board.SCL
