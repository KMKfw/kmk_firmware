from kmk.consts import DiodeOrientation
from kmk.mcus.circuitpython_usbhid import Firmware as _Firmware
from kmk.pins import Pin as P
from kmk.util import intify_coordinate as ic

# Implements what used to be handled by Firmware.swap_indicies for this
# board, by flipping various row3 (bottom physical row) keys so their
# coord_mapping matches what the user pressed (even if the wiring
# underneath is sending different coordinates)
_r3_swap_conversions = {
    3: 9,
    4: 10,
    5: 11,
    9: 3,
    10: 4,
    11: 5,
}


def r3_swap(col):
    try:
        return _r3_swap_conversions[col]
    except KeyError:
        return col


class Firmware(_Firmware):
    # physical, visible cols (SCK, MO, MI, RX, TX, D4)
    # physical, visible rows (10, 11, 12, 13) (9, 6, 5, SCL)
    col_pins = (P.SCK, P.MOSI, P.MISO, P.RX, P.TX, P.D4)
    row_pins = (P.D10, P.D11, P.D12, P.D13, P.D9, P.D6, P.D5, P.SCL)
    rollover_cols_every_rows = 4
    diode_orientation = DiodeOrientation.COLUMNS

    coord_mapping = []
    coord_mapping.extend(ic(0, x) for x in range(12))
    coord_mapping.extend(ic(1, x) for x in range(12))
    coord_mapping.extend(ic(2, x) for x in range(12))
    coord_mapping.extend(ic(3, r3_swap(x)) for x in range(12))
