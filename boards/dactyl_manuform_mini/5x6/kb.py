import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.avr_promicro import translate as avr
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (
        pins[avr['D4']],
        pins[avr['C6']],
        pins[avr['D7']],
        pins[avr['E6']],
        pins[avr['B4']],
        pins[avr['B5']],
    )
    col_pins = (
        pins[avr['F6']],
        pins[avr['F7']],
        pins[avr['B1']],
        pins[avr['B3']],
        pins[avr['B2']],
        pins[avr['B6']],
    )
    diode_orientation = DiodeOrientation.COLUMNS
    data_pin = pins[avr['D0']]
    # data_pin2 =
    # rgb_pixel_pin = pins[avr['D3']]
    # num_pixels = 12

    # flake8: noqa
    # fmt: off
    coord_mapping = [
        0,  1,  2,  3,  4,  5,                     41, 40, 39, 38, 37, 36,
        6,  7,  8,  9,  10, 11,                    47, 46, 45, 44, 43, 42,
        12, 13, 14, 15, 16, 17,                    53, 52, 51, 50, 49, 48,
        18, 19, 20, 21, 22, 23,                    59, 58, 57, 56, 55, 54,
                26, 27,     28, 29, 35,    71, 65, 64,     63, 62,
                                33, 34,    70, 69,
    ]
