from storage import getmount

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.modules.split import SplitSide
from kmk.quickpin.pro_micro.liatris import pinout as pins
from kmk.scanners import DiodeOrientation

side = SplitSide.LEFT if str(getmount('/').label)[-1] == 'L' else SplitSide.RIGHT

# With normal col/row mapping, my Left COL1 buttons kept triggering despite it being a working board.
# When swapping cols and rows (and diode_orientation to match) it's working as expected though.
# The coord_mapping corrects the colums for rows change so the other code remains unaffected.


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            (pins[19], pins[17], pins[8], pins[9], pins[10])
            if self.side == SplitSide.LEFT
            else (pins[19], pins[6], pins[14], pins[13], pins[12])
        )
        self.row_pins = (
            (pins[11], pins[16], pins[15], pins[14], pins[13], pins[12])
            if self.side == SplitSide.LEFT
            else (pins[11], pins[10], pins[9], pins[8], pins[7], pins[15])
        )
        self.diode_orientation = DiodeOrientation.COL2ROW
        self.data_pin = pins[1]
        self.rgb_pixel_pin = pins[0]
        self.SCL = pins[5]
        self.SDA = pins[4]

        # fmt:off
        self.coord_mapping = [
             0,  5, 10, 15, 20, 25,           30, 35, 40, 45, 50, 55,
             1,  6, 11, 16, 21, 26,           31, 36, 41, 46, 51, 56,
             2,  7, 12, 17, 22, 27,           32, 37, 42, 47, 52, 57,
             3,  8, 13, 18, 23, 28,  9,   54, 33, 38, 43, 48, 53, 58,
                        14, 19, 24, 29,   34, 39, 44, 49
        ]
        # fmt:on
