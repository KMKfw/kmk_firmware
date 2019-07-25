import board

from kmk.matrix import DiodeOrientation
from kmk.keyboard_config import KeyboardConfig as _KeyboardConfig


class KeyboardConfig(_KeyboardConfig):
    col_pins = (board.D9, board.D10, board.D11, board.D12, board.D13, board.SCL)
    row_pins = (board.A3, board.A4, board.A5, board.SCK, board.MOSI)
    diode_orientation = DiodeOrientation.COLUMNS
