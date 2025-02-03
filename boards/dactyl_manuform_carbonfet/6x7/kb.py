from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.avr_promicro import translate as avr
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.row_pins = (
            pins[avr['D4']],
            pins[avr['C6']],
            pins[avr['D7']],
            pins[avr['E6']],
            pins[avr['B4']],
            pins[avr['B5']],
            pins[avr['B7']],
        )
        self.col_pins = (
            pins[avr['F5']],
            pins[avr['F6']],
            pins[avr['F7']],
            pins[avr['B1']],
            pins[avr['B3']],
            pins[avr['B2']],
            pins[avr['B6']],
        )
        self.diode_orientation = DiodeOrientation.COLUMNS
        self.data_pin = pins[avr['D0']]
        # self.data_pin2 =
        # self.rgb_pixel_pin = pins[avr['D3']]
        # self.num_pixels = 12

        # fmt: off
        self.coord_mapping = [
            0,  1,  2,  3,  4,  5,  6,                      49, 50, 51, 52, 53, 54, 55,
            7,  8,  9,  10, 11, 12, 13,                     56, 57, 58, 59, 60, 61, 62,
            14, 15, 16, 17, 18, 19, 20,                     63, 64, 65, 66, 67, 68, 69,
            21, 22, 23, 24, 25, 26, 27,                     70, 71, 72, 73, 74, 75, 76,
            28, 29, 30, 31, 32, 33, 34,                     77, 78, 79, 80, 81, 82, 83,
                        38, 39,     46, 40, 41,     84, 85, 93,     86, 87,
                                    45, 47, 48,     91, 92, 94
        ]
        # fmt:on
