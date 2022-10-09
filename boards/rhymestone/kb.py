import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.pins[19], board.pins[18], board.pins[17], board.pins[16])
    col_pins = (
        board.pins[6],
        board.pins[7],
        board.pins[8],
        board.pins[9],
        board.pins[10],
    )
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = pins[0]
    rgb_num_pixels = 40
    data_pin = board.pins[1]
    i2c = board.I2C
