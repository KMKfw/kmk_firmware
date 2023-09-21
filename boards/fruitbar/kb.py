import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
# from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation

# needed to get GP29 when not using the adafruit board
# ph0enix designed by shockdesign & pelrun
# https://github.com/shockdesign/ph0enix-keyboard


class KMKKeyboard(_KMKKeyboard):
    row_pins = (
        board.GP29,
        board.GP18,
        board.GP10,
        board.GP6,
    )
    col_pins = (
        board.GP25,
        board.GP24,
        board.GP23,
        board.GP22,
        board.GP21,
        board.GP20,
        board.GP17,
        board.GP16,
        board.GP15,
        board.GP13,
        board.GP12,
        board.GP11,
        board.GP9,
        board.GP8,
        board.GP7,
        board.GP3,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    #   led_pin = board.pins[11]
    #   rgb_pixel_pin = board.pins[10]
    rgb_num_pixels = 1

    debug_enabled = True


# i2c = board.I2C
SCL = board.GP4
SDA = board.GP5
