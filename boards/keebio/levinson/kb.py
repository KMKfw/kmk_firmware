import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.P0_22, board.P1_00, board.P0_11, board.P1_04)
    col_pins = (
        board.P0_02,
        board.P1_15,
        board.P1_13,
        board.P1_11,
        board.P0_10,
        board.P0_09,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = board.P0_06
    rgb_num_pixels = 12
    led_pin = board.P1_06
    data_pin = board.P0_08
    i2c = board.I2C
    powersave_pin = board.P0_13
