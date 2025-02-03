from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_Micro.avr_promicro import translate as avr
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            pins[avr['B3']],
            pins[avr['B1']],
            pins[avr['F7']],
            pins[avr['F6']],
            pins[avr['F5']],
            pins[avr['D0']],
            pins[avr['D4']],
            pins[avr['C6']],
            pins[avr['D7']],
            pins[avr['E6']],
        )
        self.row_pins = (
            pins[avr['B2']],
            pins[avr['B6']],
            pins[avr['B4']],
            pins[avr['B5']],
        )
        self.diode_orientation = DiodeOrientation.ROWS

        # fmt: off
        self.coord_mapping = [
            0,  1,  2,  3,        4,  5,  6,  7,
            8, 9, 10, 11, 12, 13,       14, 15, 16, 17, 18, 19,
            20, 21, 22, 23, 24,       25, 26, 27, 28, 29,
            30, 31,       32, 33,
            ]
        # fmt:on
