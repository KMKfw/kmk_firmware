import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.controller import pinout as pins
from kmk.quickpin.pro_Micro.avr_promicro import translate as avr
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        pins[avr['C6']],
        pins[avr['D7']],
        pins[avr['E6']],
        pins[avr['B4']],
        pins[avr['B5']],
    )
    row_pins = (
        pins[avr['F7']],
        pins[avr['B1']],
        pins[avr['B3']],
        pins[avr['B2']],
        pins[avr['B6']],
    )
    data_pin = pins[avr['D0']]
    #data_pin2 =
    rgb_pixel_pin = pins[avr['D3']]
    diode_orientation = DiodeOrientation.COLUMNS
    
    coord_mapping = [
     0,  1,  2,  3,  4,  29, 28, 27, 26, 25,
     5,  6,  7,  8,  9,  34, 33, 32, 31, 30,
    10, 11, 12, 13, 14,  39, 38, 37, 36, 35,
        16, 17,                  42, 41,
                18, 19,  44, 43,
                23, 24,  49, 48,
                21, 22,  47, 46
    ]
