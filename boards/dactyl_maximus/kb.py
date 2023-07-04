import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.avr_promicro import translate as avr
from kmk.quickpin.pro_micro.kb2040 import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        pins[avr['D1']],
        pins[avr['D4']],
        pins[avr['C6']],
        pins[avr['D7']],
        pins[avr['E6']],
        pins[avr['B4']],
        pins[avr['B5']],
    )
    row_pins = (
        pins[avr['F6']],
        pins[avr['F7']],
        pins[avr['B1']],
        pins[avr['B3']],
        pins[avr['B2']],
        pins[avr['B6']],
    )
    diode_orientation = DiodeOrientation.COLUMNS
    data_pin = pins[avr['D3']]
    # data_pin2 = pins[avr['D2']]
    # rgb_pixel_pin = pins[avr['D0']]
    # num_pixels = 12
    
    # flake8: noqa
    # fmt: off
    coord_mapping = [
        0,  1,  2,  3,  4,  5,  6,                    41, 40, 39, 38, 37, 36, 35, 
        7,  8,  9,  10, 11, 12, 13,                   48, 47, 46, 45, 44, 43, 42,
        14, 15, 16, 17, 18, 19, 20,                   55, 54, 53, 52, 51, 50, 49,
        21, 22, 23, 24, 25, 26, 27, 34, 41,   76, 69, 62, 61, 60, 59, 58, 57, 56,
        28, 29, 30, 31, 32, 33, 38, 39, 40,   75, 74, 73, 68, 67, 66, 65, 64, 63, 
                                35, 36, 37,   72, 71, 70                                 
    ]                            
