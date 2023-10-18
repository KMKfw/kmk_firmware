import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation
from kmk.scanners import intify_coordinate as ic


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        pins[6],
        pins[7],
        pins[8],
        pins[9],
        pins[10],
        pins[11],
    )
    row_pins = (
        pins[19],
        pins[18],
        pins[17],
        pins[16],
        pins[15],
        pins[14],
        pins[13],
    )
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = pins[0]
    rgb_num_pixels = 11
    i2c = board.I2C

    coord_mapping = []
    coord_mapping.extend(ic(0, x, 12) for x in range(12))
    coord_mapping.extend(ic(1, x, 12) for x in range(12))
    coord_mapping.extend(ic(2, x, 12) for x in range(12))

    # And now, to handle R3, which at this point is down to just five keys
    coord_mapping.extend(ic(3, x, 12) for x in range(5))
