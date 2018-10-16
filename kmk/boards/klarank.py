from kmk.consts import DiodeOrientation
from kmk.mcus.circuitpython_samd51 import Firmware as _Firmware
from kmk.pins import Pin as P


class Firmware(_Firmware):
    # physical, visible cols (SCK, MO, MI, RX, TX, D4)
    # physical, visible rows (10, 11, 12, 13) (9, 6, 5, SCL)
    col_pins = (P.SCK, P.MOSI, P.MISO, P.RX, P.TX, P.D4)
    row_pins = (P.D10, P.D11, P.D12, P.D13, P.D9, P.D6, P.D5, P.SCL)
    rollover_cols_every_rows = 4
    diode_orientation = DiodeOrientation.COLUMNS

    swap_indicies = {
        (3, 3): (3, 9),
        (3, 4): (3, 10),
        (3, 5): (3, 11),
    }
