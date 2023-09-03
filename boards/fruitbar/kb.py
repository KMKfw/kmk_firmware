import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
# from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
from kmk.scanners import DiodeOrientation

# needed to get GP29 when not using the adafruit board
###from adafruit_blinka.board.raspberrypi.pico import pin

"""

"manufacturer": "Fruitykeeb",
    "keyboard_name": "fruitbar r2",
    "maintainer": "ojthetiny",
    "bootloader": "rp2040",
    "diode_direction": "COL2ROW",
    "processor": "RP2040",
    "features" : {
        "bootmagic": true,
        "command": false,
        "console": false,
        "extrakey": true,
        "mousekey": true,
        "nkro": true,
        "oled": true,
        "encoder": true
    },
    "matrix_pins": {
        "rows": [ "GP29", "GP18", "GP10", "GP6" ],
        "cols": [ "GP25", "GP24", "GP23", "GP22", "GP21", "GP20", "GP17", "GP16", "GP15", "GP13", "GP12", "GP11", "GP9", "GP8", "GP7", "GP3" ]
    },

    ===============================

    # ph0enix designed by shockdesign & pelrun
# https://github.com/shockdesign/ph0enix-keyboard
# Requires CircuitPython 7.0.0 to support the RP2040 MCU
import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC


keyboard = KMKKeyboard()
keyboard.modules.append(Layers())

# keyboard.debug_enabled = True

keyboard.col_pins = (
    board.GP21, board.GP20, board.GP19, board.GP11, board.GP16, board.GP17, board.GP18,
    board.GP12, board.GP15, board.GP14, board.GP13
)
keyboard.row_pins = (board.GP5, board.GP4, board.GP2, board.GP3)

keyboard.diode_orientation = DiodeOrientation.COL2ROW

FN = KC.MO(1)

    "matrix_pins": {
        "rows": [ "GP29", "GP18", "GP10", "GP6" ],
        "cols": [ "GP25", "GP24", "GP23", "GP22", "GP21", "GP20", "GP17", "GP16", "GP15", "GP13", "GP12", "GP11", "GP9", "GP8", "GP7", "GP3" ]
    },
"""


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
