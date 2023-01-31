import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (
        pins[11],
        pins[10],
        pins[9],
        pins[8],
        pins[7],
        pins[6],
        pins[5],
        pins[4],
    )
    col_pins = [
        pins[0],
        pins[14],
        pins[15],
        pins[16],
        pins[17],
        pins[18],
        pins[19],
    ]
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = pins[1]
    rgb_num_pixels = 7
    i2c = board.I2C
    ## large keys
    coord_mapping = [
     0 ,1 ,2 ,3 ,4 ,5 ,6 ,28,29,30,31,33,
     7 ,8 ,9 ,10,11,12,13,35,36,37,38,39,
     14,15,16,17,18,19,20,42,43,44,46,
     21,22,23,25,26,50,51,52,53
         ]
    #all keys
    #          coord_mapping = [
    #  0 ,1 ,2 ,3 ,4 ,5 ,6 ,28,29,30,31,32,33,
    #  7 ,8 ,9 ,10,11,12,13,35,36,37,38,39,
    #  14,15,16,17,18,19,20,42,43,44,45,46,
    #  21,22,23,25,26,50,51,52,53
    #      ]
