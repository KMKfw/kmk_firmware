import board
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.matrix import intify_coordinate as ic

class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.P1_11, board.AIN0, board.P0_03, board.P1_13)
    col_pins = (
        board.P0_30,
        board.NFC2,
        board.NFC1,
        board.P0_24,
        board.P0_13,
        board.P0_20,
        board.P1_00,
        board.P1_02,
        board.AIN5,
        board.AIN7,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    i2c = board.I2C
    powersave_pin = board.VCC_OFF
    rgb_pixel_pin = board.P0_22

    coord_mapping = []
    coord_mapping.extend(ic(0, x) for x in range(10))
    coord_mapping.extend(ic(1, x) for x in range(10))
    coord_mapping.extend(ic(2, x) for x in range(10))
    # And now, to handle R3, which at this point is down to 8 keys
    coord_mapping.extend(ic(3, x) for x in range(8))