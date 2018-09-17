from logging import DEBUG

import machine

from kmk.common.consts import DiodeOrientation
from kmk.common.keycodes import KC
from kmk.firmware import Firmware
from kmk.micropython.pyb_hid import HIDHelper


def main():
    p = machine.Pin.board

    cols = (p.X10, p.X11, p.X12)
    rows = (p.X1, p.X2, p.X3)

    diode_orientation = DiodeOrientation.COLUMNS

    keymap = [
        [KC.ESC, KC.H, KC.BACKSPACE],
        [KC.TAB, KC.I, KC.ENTER],
        [KC.CTRL, KC.SPACE, KC.SHIFT],
    ]

    firmware = Firmware(
        keymap=keymap,
        row_pins=rows,
        col_pins=cols,
        diode_orientation=diode_orientation,
        hid=HIDHelper,
        log_level=DEBUG,
    )

    firmware.go()
