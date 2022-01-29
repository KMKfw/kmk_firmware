# VColMX44 designed by jpconstantineau
# https://github.com/jpconstantineau/VColChoc44
# Board uses a Raspberry Pi Pico
# Requires CircuitPython 7.0.0 to support the RP2040 MCU

from kb import KMKKeyboard

from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()
keyboard.modules.append(Layers())

rgb_ext = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=keyboard.rgb_num_pixels, animation_mode=AnimationModes.STATIC)
keyboard.extensions.append(rgb_ext)

FUN = KC.MO(1)
UPPER = KC.MO(2)
XXXXXXX = KC.TRNS
RGB_BR = KC.RGB_MODE_BREATHE_RAINBOW
RGB_P = KC.RGB_MODE_PLAIN
RGB_B = KC.RGB_MODE_BREATHE
RGB_R = KC.RGB_MODE_RAINBOW
RGB_K = KC.RGB_MODE_KNIGHT

keyboard.keymap = [
    # Colemak Mod-DH See https://colemakmods.github.io/mod-dh/keyboards.html
    [
        KC.Q,       KC.W,       KC.F,       KC.P,       KC.B,           KC.GRAVE,   KC.J,       KC.L,       KC.U,       KC.Y,       KC.SCLN,
        KC.A,       KC.R,       KC.S,       KC.T,       KC.G,           KC.LCTRL,   KC.M,       KC.N,       KC.E,       KC.I,       KC.O,
        KC.Z,       KC.X,       KC.C,       KC.D,       KC.V,           KC.BACKSLASH, KC.K,     KC.H,       KC.COMM,    KC.DOT,     KC.SLSH,
        KC.ESC,     KC.TAB,     KC.LGUI,    KC.LSHIFT,  KC.BACKSPACE,   KC.LALT,    KC.SPC,     FUN,        KC.MINUS,   KC.QUOT,    KC.ENTER,
    ],
    [
        KC.EXLM,    KC.AT,      KC.UP,      KC.DLR,     KC.PERC,        KC.CIRC,    KC.PGUP,    KC.N7,      KC.N8,      KC.N9,      KC.BACKSPACE,
        KC.LPRN,    KC.LEFT,    KC.DOWN,    KC.RIGHT,   KC.RPRN,        XXXXXXX,    KC.PGDN,    KC.N4,      KC.N5,      KC.N6,      KC.SCOLON,
        KC.LBRC,    KC.RBRC,    KC.HASH,    KC.LCBR,    KC.RCBR,        KC.AMPR,    KC.ASTR,    KC.N1,      KC.N2,      KC.N3,      KC.PLUS,
        UPPER,      KC.INSERT,  XXXXXXX,    XXXXXXX,    XXXXXXX,        XXXXXXX,    XXXXXXX,    XXXXXXX,    XXXXXXX,    KC.N0,      KC.EQL,
    ],
    [
        KC.INSERT,  KC.HOME,    KC.UP,      KC.END,     KC.PGUP,        RGB_BR,     KC.UP,      KC.F7,      KC.F8,      KC.F9,      KC.F10,
        KC.DEL,     KC.LEFT,    KC.DOWN,    KC.RIGHT,   KC.PGDN,        XXXXXXX,    KC.DOWN,    KC.F4,      KC.F5,      KC.F6,      KC.F11,
        KC.NO,      KC.VOLU,    RGB_P,      RGB_B,      RGB_R,          RGB_K,      XXXXXXX,    KC.F1,      KC.F2,      KC.F3,      KC.F12,
        UPPER,      KC.VOLD,    XXXXXXX,    XXXXXXX,    XXXXXXX,        XXXXXXX,    XXXXXXX,    XXXXXXX,    KC.PSCR,    KC.SLCK,    KC.PAUS,
    ],
]

if __name__ == '__main__':
    keyboard.go()
