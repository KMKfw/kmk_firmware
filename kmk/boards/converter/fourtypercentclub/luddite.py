import board

from kmk.consts import DiodeOrientation
from kmk.mcus.circuitpython_usbhid import KeyboardConfig as _KeyboardConfig


class KeyboardConfig(_KeyboardConfig):
    col_pins = (
        board.A0,
        board.A1,
        board.A2,
        board.A3,
        board.A4,
        board.A5,
        board.SCK,
        board.MOSI,
    )
    row_pins = (
        board.TX,
        board.RX,
        board.SDA,
        board.SCL,
        board.D13,
        board.D12,
        board.D11,
        board.D10,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = board.D9
    rgb_num_pixels = 12
