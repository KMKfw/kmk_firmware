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
        0,  1,  2,  3,  4,  5,                     36, 37, 38, 39, 40, 41,
        6,  7,  8,  9,  10, 11,                    42, 43, 44, 45, 46, 47,
        12, 13, 14, 15, 16, 17,                    48, 49, 50, 51, 52, 53,
        18, 19, 20, 21, 22, 23,                    54, 55, 56, 57, 58, 59,
                26, 27,     28, 29, 35,    66, 60, 61,     62, 63,
                                33, 34,    67, 68
    ]
