# VColMX44 designed by jpconstantineau
# https://github.com/jpconstantineau/VColMX44
# Board uses a Raspberry Pi Pico
# Requires CircuitPython 7.0.0 to support the RP2040 MCU

import board

from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.modules.layers import Layers

keyboard = _KMKKeyboard()
keyboard.modules.append(Layers())

rgb_ext = RGB(pixel_pin=board.GP28, num_pixels=61, animation_mode=AnimationModes.STATIC)
keyboard.extensions.append(rgb_ext)

keyboard.col_pins = (
    board.GP20,
    board.GP19,
    board.GP18,
    board.GP17,
    board.GP16,
    board.GP5,
    board.GP4,
    board.GP3,
    board.GP2,
    board.GP1,
    board.GP0,
)
keyboard.row_pins = (board.GP22, board.GP21, board.GP14, board.GP15)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

FUN = KC.MO(1)
UPPER = KC.MO(2)
XXXXXXX = KC.TRNS

keyboard.keymap = [
    # Qwerty
    [
        KC.Q,
        KC.W,
        KC.E,
        KC.R,
        KC.T,
        KC.GRAVE,
        KC.Y,
        KC.U,
        KC.I,
        KC.O,
        KC.P,
        KC.A,
        KC.S,
        KC.D,
        KC.F,
        KC.G,
        KC.LCTRL,
        KC.H,
        KC.J,
        KC.K,
        KC.L,
        KC.SCLN,
        KC.Z,
        KC.X,
        KC.C,
        KC.V,
        KC.B,
        KC.BACKSLASH,
        KC.N,
        KC.M,
        KC.COMM,
        KC.DOT,
        KC.SLSH,
        KC.ESC,
        KC.TAB,
        KC.LGUI,
        KC.LSHIFT,
        KC.BACKSPACE,
        KC.LALT,
        KC.SPC,
        FUN,
        KC.MINUS,
        KC.QUOT,
        KC.ENTER,
    ],
    [
        KC.EXLM,
        KC.AT,
        KC.UP,
        KC.DLR,
        KC.PERC,
        KC.CIRC,
        KC.PGUP,
        KC.N7,
        KC.N8,
        KC.N9,
        KC.BACKSPACE,
        KC.LPRN,
        KC.LEFT,
        KC.DOWN,
        KC.RIGHT,
        KC.RPRN,
        XXXXXXX,
        KC.PGDN,
        KC.N4,
        KC.N5,
        KC.N6,
        KC.SCOLON,
        KC.LBRC,
        KC.RBRC,
        KC.HASH,
        KC.LCBR,
        KC.RCBR,
        KC.AMPR,
        KC.ASTR,
        KC.N1,
        KC.N2,
        KC.N3,
        KC.PLUS,
        UPPER,
        KC.INSERT,
        XXXXXXX,
        XXXXXXX,
        XXXXXXX,
        XXXXXXX,
        XXXXXXX,
        XXXXXXX,
        XXXXXXX,
        KC.N0,
        KC.EQL,
    ],
    [
        KC.INSERT,
        KC.HOME,
        KC.UP,
        KC.END,
        KC.PGUP,
        KC.RGB_MODE_BREATHE_RAINBOW,
        KC.UP,
        KC.F7,
        KC.F8,
        KC.F9,
        KC.F10,
        KC.DEL,
        KC.LEFT,
        KC.DOWN,
        KC.RIGHT,
        KC.PGDN,
        XXXXXXX,
        KC.DOWN,
        KC.F4,
        KC.F5,
        KC.F6,
        KC.F11,
        KC.NO,
        KC.VOLU,
        KC.RGB_MODE_PLAIN,
        KC.RGB_MODE_BREATHE,
        KC.RGB_MODE_RAINBOW,
        KC.RGB_MODE_KNIGHT,
        XXXXXXX,
        KC.F1,
        KC.F2,
        KC.F3,
        KC.F12,
        UPPER,
        KC.VOLD,
        XXXXXXX,
        XXXXXXX,
        XXXXXXX,
        XXXXXXX,
        XXXXXXX,
        XXXXXXX,
        KC.PSCR,
        KC.SLCK,
        KC.PAUS,
    ],
]

if __name__ == '__main__':
    keyboard.go()
