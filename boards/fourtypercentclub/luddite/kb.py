import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.row_pins = (
            pins[0],
            board.pins[1],
            board.pins[4],
            board.pins[5],
            board.pins[6],
            board.pins[7],
            board.pins[8],
            board.pins[9],
        )
        self.col_pins = (
            board.pins[19],
            board.pins[18],
            board.pins[17],
            board.pins[16],
            board.pins[15],
            board.pins[14],
            board.pins[13],
            board.pins[12],
        )
        self.diode_orientation = DiodeOrientation.COLUMNS
        self.led_pin = board.pins[11]
        self.rgb_pixel_pin = board.pins[10]
        self.rgb_num_pixels = 8
        self.i2c = board.I2C
