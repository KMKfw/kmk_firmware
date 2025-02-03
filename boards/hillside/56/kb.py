from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.avr_promicro import translate as avr
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            pins[avr['C6']],
            pins[avr['D7']],
            pins[avr['E6']],
            pins[avr['B4']],
            pins[avr['B5']],
        )
        self.row_pins = (
            pins[avr['F6']],
            pins[avr['F7']],
            pins[avr['B1']],
            pins[avr['B3']],
            pins[avr['B2']],
            pins[avr['B6']],
        )
        self.diode_orientation = DiodeOrientation.COLUMNS
        self.data_pin = pins[avr['D2']]
        # self.left_encoder_pin_0 = pins[avr['F5']]
        # self.left_encoder_pin_1 = pins[avr['F4']]
        # self.right_encoder_pin_0 = pins[avr['F4']]
        # self.right_encoder_pin_1 = pins[avr['F5']]
        self.rgb_pixel_pin = pins[avr['D3']]

        # fmt: off
        self.coord_mapping = [
            0,  1,  2,  3,  4,  5,                    35, 34, 33, 32, 31, 30,
            6,  7,  8,  9,  10, 11,                   41, 40, 39, 38, 37, 36,
            12, 13, 14, 15, 16, 17, 29,           59, 47, 46, 45, 44, 43, 42,
            18,     20,     25, 26, 27, 28,   58, 57, 56, 55,     50,     48,
                19, 21, 22,                                   52, 51, 49
        ]
        # fmt: on
