from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            pins[19],
            pins[18],
            pins[17],
            pins[16],
            pins[15],
            pins[14],
            pins[13],
            pins[12],
        )
        self.row_pins = (pins[10], pins[9], pins[8], pins[6])
        self.diode_orientation = DiodeOrientation.COL2ROW
        self.data_pin = pins[1]
        self.rgb_pixel_pin = pins[0]
        self.encoder_pin_0 = pins[11]
        self.encoder_pin_1 = pins[7]

        # fmt: off
        self.coord_mapping = [
             0,  1,  2,  3,  4,  5,                 37, 36, 35, 34, 33, 32,
             8,  9, 10, 11, 12, 13,                 45, 44, 43, 42, 41, 40,
            16, 17, 18, 19, 20, 21, 22, 23, 55, 54, 53, 52, 51, 50, 49, 48,
                    27, 28, 29, 30, 31,         63, 62, 61, 60, 59,
        ]
        # fmt: on
