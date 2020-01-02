import board
import busio

import adafruit_seesaw.seesaw
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation

i2c = busio.I2C(board.SCL, board.SDA)


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.A0, board.A1, board.A2, board.A3)
    col_pins = (9, 10, 11, 14)
    diode_orientation = DiodeOrientation.COLUMNS
    rgb_pixel_pin = board.NEOPIXEL
    rgb_num_pixels = 1


keyboard = KMKKeyboard()

keyboard.keymap = [[
    KC.N1, KC.N2, KC.N3, KC.N4,
    KC.N5, KC.N6, KC.N7, KC.N8,
    KC.N9, KC.N0, KC.A,  KC.B,
    KC.C,  KC.D,  KC.E,  KC.F]]

if __name__ == '__main__':
    seesaw = adafruit_seesaw.seesaw.Seesaw(i2c)
    keyboard.go(seesaw=seesaw)
