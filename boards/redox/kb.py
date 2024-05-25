from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.avr_promicro import translate as avr
from kmk.quickpin.pro_micro.helios import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        pins[avr['F5']],
        pins[avr['F6']],
        pins[avr['F7']],
        pins[avr['B1']],
        pins[avr['B3']],
        pins[avr['B2']],
        pins[avr['B6']],
    )
    row_pins = (
        pins[avr['D4']],
        pins[avr['D7']],
        pins[avr['E6']],
        pins[avr['B4']],
        pins[avr['B5']],
    )

    data_pin = pins[avr['D0']]
    # data_pin2 =
    # rgb_pixel_pin = pins[avr['D3']]
    diode_orientation = DiodeOrientation.COLUMNS
    # fmt: off
    coord_mapping = [
        0,  1,  2,  3,  4,  5,                     40, 39, 38, 37, 36, 35,
        7,  8,  9,  10, 11, 12, 6,             41, 47, 46, 45, 44, 43, 42,
        14, 15, 16, 17, 18, 19, 13,            48, 54, 53, 52, 51, 50, 49,
        21, 22, 23, 24, 25, 26, 20, 27,    62, 55, 61, 60, 59, 58, 57, 56,
        28, 29, 30, 31,   32,   33, 34,    69, 68,    67,  66, 65, 64, 63,
    ]
    # fmt: on
