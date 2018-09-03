from logging import DEBUG

import board

from kmk.common.consts import DiodeOrientation
from kmk.firmware import Firmware


def main():
    cols = (board.A4, board.A5)
    rows = (board.D27, board.A6)

    diode_orientation = DiodeOrientation.COLUMNS

    keymap = [
        ['A', 'B'],
        ['C', 'D'],
    ]

    firmware = Firmware(
        keymap=keymap,
        row_pins=rows,
        col_pins=cols,
        diode_orientation=diode_orientation,
        log_level=DEBUG,
    )

    firmware.go()
