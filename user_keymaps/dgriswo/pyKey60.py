# PyKey60 designed by jpconstantineau
# https://github.com/jpconstantineau/PyKey60
# Requires CircuitPython 7.0.0 to support the RP2040 MCU

import board

from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.modules.layers import Layers

keyboard = _KMKKeyboard()
keyboard.modules.append(Layers())

rgb_ext = RGB(
    pixel_pin=board.NEOPIXEL, num_pixels=61, animation_mode=AnimationModes.STATIC
)
keyboard.extensions.append(rgb_ext)

keyboard.col_pins = (
    board.COL1, board.COL2, board.COL3, board.COL4, board.COL5, board.COL6, board.COL7,
    board.COL8, board.COL9, board.COL10, board.COL11, board.COL12, board.COL13, board.COL14,
)
keyboard.row_pins = (board.ROW1, board.ROW2, board.ROW3, board.ROW4, board.ROW5)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

FN = KC.MO(1)
XXXXXXX = KC.TRNS

keyboard.keymap = [
    # Qwerty
    # ,-------------------------------------------------------------------------------------------------.
    # | ESC  |   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |   0  |   -  |   =  | Bksp |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Tab  |   Q  |   W  |   E  |   R  |   T  |   Y  |   U  |   I  |   O  |   P  |   [  |   ]  |   \  |
    # |------+------+------+------+------+-------------+------+------+------+------+------+------+------|
    # | Caps |   A  |   S  |   D  |   F  |   G  |   H  |   J  |   K  |   L  |   ;  |   '  |XXXXXX| Enter|
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Shift|   Z  |   X  |   C  |   V  |   B  |   N  |   M  |   ,  |   .  |   /  |XXXXXX|XXXXXX| Shift|
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Ctrl | GUI  |  Alt |XXXXXX|XXXXXX| Space|XXXXXX|XXXXXX|XXXXXX| Alt  | GUI  | Fn   |XXXXXX| Ctrl |
    # `------------------------------------------------------------------------------------------+------'
    [
        KC.GESC,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,  KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.MINS, KC.EQUAL, KC.BSPC,
        KC.TAB,   KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,   KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.LBRC, KC.RBRC,  KC.BSLASH,
        KC.CAPS,  KC.A,    KC.S,    KC.D,    KC.F,    KC.G,   KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT, XXXXXXX,  KC.ENTER,
        KC.LSFT,  KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,   KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, XXXXXXX, XXXXXXX,  KC.RSFT,
        KC.LCTRL, KC.LGUI, KC.LALT, XXXXXXX, XXXXXXX, KC.SPC, XXXXXXX, XXXXXXX, XXXXXXX, KC.RALT, KC.RGUI, FN,      XXXXXXX,  KC.RCTRL
    ],
    # Alt
    # ,-------------------------------------------------------------------------------------------------.
    # |   `  |  F1  |  F2  |  F3  |  F4  |  F5  |  F6  |  F7  |  F8  |  F9  | F10  | F11  | F12  | Del  |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # |      |      |  UP  |      |      |      |      |      | Insrt| Home | PgUp |      |      |      |
    # |------+------+------+------+------+-------------+------+------+------+------+------+------+------|
    # |      | LEFT | DOWN | RIGHT|      |      |      |      | Del  | End  | PgDn |      |      |      |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # |      |      |      |      |      |      |      | MUTE | VOLD | VOLU |      |      |      |      |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # |      |      |      |      |      |      |      |      |      |      | App  | Fn   |      |      |
    # `------------------------------------------------------------------------------------------+------'
    [
        KC.GRV,  KC.F1,   KC.F2,   KC.F3,    KC.F4,   KC.F5,   KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,   KC.F12,  KC.DEL,
        XXXXXXX, XXXXXXX, KC.UP,   XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.INS,  KC.HOME, KC.PGUP, XXXXXXX,  XXXXXXX, XXXXXXX,
        XXXXXXX, KC.LEFT, KC.DOWN, KC.RIGHT, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.DEL,  KC.END,  KC.PGDN, XXXXXXX,  XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, KC.MUTE, KC.VOLD, KC.VOLU, XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.APP,  XXXXXXX,  XXXXXXX, XXXXXXX,
    ],
]

if __name__ == '__main__':
    keyboard.go()
