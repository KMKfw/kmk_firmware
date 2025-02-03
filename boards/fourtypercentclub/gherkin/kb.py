import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.row_pins = (pins[16], pins[15], pins[14], pins[13], pins[12])
        self.col_pins = (
            board.pins[10],
            board.pins[9],
            board.pins[8],
            board.pins[7],
            board.pins[6],
            board.pins[5],
        )
        self.diode_orientation = DiodeOrientation.COLUMNS
        self.led_pin = board.pins[11]
        self.rgb_num_pixels = 0
        self.i2c = board.I2C
