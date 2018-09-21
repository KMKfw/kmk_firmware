from logging import DEBUG

import machine

from kmk.common.consts import DiodeOrientation
from kmk.common.keycodes import KC
from kmk.firmware import Firmware
from kmk.micropython.pyb_hid import HIDHelper


def main():
    p = machine.Pin.board

    cols = (p.Y12, p.Y11, p.Y10, p.Y9, p.X8, p.X7, p.X6, p.X5, p.X4, p.X3, p.X2, p.X1)
    rows = (p.Y1, p.Y2, p.Y3, p.Y4)

    diode_orientation = DiodeOrientation.COLUMNS

    keymap = [
        [KC.ESC, KC.QUOTE, KC.COMMA, KC.PERIOD, KC.P, KC.Y, KC.F, KC.G, KC.C, KC.R, KC.L,
            KC.BACKSPACE],
        [KC.TAB, KC.A, KC.O, KC.E, KC.U, KC.I, KC.D, KC.H, KC.T, KC.N, KC.S, KC.ENTER],
        [KC.SHIFT, KC.SEMICOLON, KC.Q, KC.J, KC.K, KC.X, KC.B, KC.M, KC.W, KC.V, KC.Z, KC.SLASH],
        [KC.CTRL, KC.GUI, KC.ALT, KC.RESET, KC.A, KC.SPACE, KC.SPACE, KC.A, KC.LEFT, KC.DOWN,
            KC.UP, KC.RIGHT],
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
