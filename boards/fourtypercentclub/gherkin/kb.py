import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (pins[16], pins[15], pins[14], pins[13], pins[12])
    col_pins = (
        board.pins[10],
        board.pins[9],
        board.pins[8],
        board.pins[7],
        board.pins[6],
        board.pins[5],
    )
    diode_orientation = DiodeOrientation.COLUMNS
    led_pin = board.pins[11]
    rgb_num_pixels = 0
    i2c = board.I2C
