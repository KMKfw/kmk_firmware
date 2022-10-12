import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.pins[6], board.pins[8], board.pins[9], board.pins[10])
    col_pins = (
        board.pins[17],
        board.pins[16],
        board.pins[15],
        board.pins[14],
        board.pins[13],
        board.pins[12],
    )
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = pins[0]
    rgb_num_pixels = 12
    led_pin = board.pins[11]
    data_pin = board.pins[1]
    i2c = board.I2C
    powersave_pin = board.P0_13
