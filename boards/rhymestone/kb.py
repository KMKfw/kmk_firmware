import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (pins[19], pins[18], pins[17], pins[16])
    col_pins = (
        pins[6],
        pins[7],
        pins[8],
        pins[9],
        pins[10],
    )
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = pins[0]
    rgb_num_pixels = 40
    data_pin = pins[1]
    SCL = board.SCL
    SDA = board.SDA
    i2c = board.I2C
