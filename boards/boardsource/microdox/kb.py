import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            board.pins[19],
            board.pins[18],
            board.pins[17],
            board.pins[16],
            board.pins[15],
        )
        self.row_pins = (board.pins[13], board.pins[12], board.pins[10], board.pins[11])
        self.diode_orientation = DiodeOrientation.COLUMNS
        self.data_pin = board.pins[1]
        self.rgb_pixel_pin = pins[0]
        self.rgb_num_pixels = 12
        self.i2c = board.I2C

        # fmt: off
        self.coord_mapping = [
             0,  1,  2,  3,  4,  20, 21, 22, 23, 24,
             5,  6,  7,  8,  9,  25, 26, 27, 28, 29,
            10, 11, 12, 13, 14,  30, 31, 32, 33, 34,
                    17, 18, 19,  35, 36, 37,
        ]
        # fmt: on
