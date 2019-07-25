import board

from kmk.matrix import DiodeOrientation
from kmk.keyboard_config import KeyboardConfig as _KeyboardConfig


class KeyboardConfig(_KeyboardConfig):
    col_pins = (
        board.RX,
        board.D13,
        board.A0,
        board.D11,
        board.A4,
        board.A5,
        board.D10,
        board.D9,
        board.SCK,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = board.TX
