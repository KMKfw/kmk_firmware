from logging import DEBUG

from kmk.common.consts import DiodeOrientation
from kmk.firmware import Firmware


def main():
    cols = ('X10', 'X11', 'X12')
    rows = ('X1', 'X2', 'X3')

    diode_orientation = DiodeOrientation.COLUMNS

    keymap = [
        ['A', 'B', 'C'],
        ['D', 'E', 'F'],
        ['G', 'H', 'I'],
    ]

    firmware = Firmware(
        keymap=keymap,
        row_pins=rows,
        col_pins=cols,
        diode_orientation=diode_orientation,
        log_level=DEBUG,
    )

    firmware.go()
