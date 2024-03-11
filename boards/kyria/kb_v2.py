from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.sparkfun_promicro_rp2040 import pinout as pins
from kmk.scanners import DiodeOrientation
from kmk.scanners import intify_coordinate as ic
from storage import getmount

isLeftSide = False if str(getmount('/').label)[-1] == 'R' else True
leftColPins = (
        pins[6],
        pins[7],
        pins[8],
        pins[9],
        pins[10],
        pins[11],
        pins[12],
        pins[13],
    )
leftRowPins = (pins[17], pins[16], pins[15], pins[14])

rightColPins = (
        pins[10],
        pins[11],
        pins[12],
        pins[13],
        pins[14],
        pins[15],
        pins[16],
        pins[17],
    )
rightRowPins = (pins[6], pins[7], pins[8], pins[9])


colPins = ()
rowPins = ()

if isLeftSide:
    colPins = leftColPins
    rowPins = leftRowPins
else:
    colPins = rightColPins
    rowPins = rightRowPins


class KMKKeyboard(_KMKKeyboard):
    SDA = pins[4]
    SCL = pins[5]
    col_pins = (
        pins[6],
        pins[7],
        pins[8],
        pins[9],
        pins[10],
        pins[11],
        pins[12],
        pins[13],
    )
    row_pins = (pins[17], pins[16], pins[15], pins[14])
    diode_orientation = DiodeOrientation.COL2ROW
    data_pin = pins[1]
    rgb_pixel_pin = pins[0]
 
    coord_mapping = [
        0,   1,  2,  3,  4,  5,                         34, 35, 36, 37, 38, 39, 
        8,   9, 10, 11, 12, 13,                         42, 43, 44, 45, 46, 47, 
        16, 17, 18, 19, 20, 21, 22, 23,         48, 49, 50, 51, 52, 53, 54, 55, 
                    26, 28, 29, 30, 31,         56, 57, 58, 59, 61
    ]
