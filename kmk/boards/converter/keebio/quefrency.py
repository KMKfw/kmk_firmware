import board

from kmk.keyboard_config import KeyboardConfig as _KeyboardConfig
from kmk.matrix import DiodeOrientation


class KeyboardConfig(_KeyboardConfig):
    # Will need additional work and testing
    col_pins = (
        board.A1,
        board.A2,
        board.A3,
        board.A4,
        board.A5,
        board.SCK,
        board.MOSI,
        board.D12,
    )
    row_pins = (board.A0, board.D13, board.D11, board.D10, board.D9, board.D7)
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = board.TX
    uart_pin = board.SCL
    split_type = 'UART'
    split_flip = False
    split_offsets = [8, 8, 8, 8, 8, 8]
