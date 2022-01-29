# OffsetMX43 designed by jpconstantineau
# https://github.com/jpconstantineau/OffsetMX43
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
    # Qwerty
    [
        KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.BSPC,
        KC.ESC,  KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.NO,   KC.ENT,
        KC.LSFT, KC.NO,   KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH,
        UPPER,   KC.LCTL, KC.LALT, KC.NO,   FUN,     KC.SPC,  KC.SPC,  KC.NO,   KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT,
    ],
    [
        KC.TILD, KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC, KC.CIRC, KC.AMPR,          KC.ASTR,           KC.LPRN, KC.RPRN, KC.BSPC,
        KC.DEL,  KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.UNDS,          KC.PLUS,           KC.LCBR, KC.NO,   KC.RCBR,
        XXXXXXX, KC.NO,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.LSFT(KC.NUHS), KC.LSFT(KC.NUBS),  KC.HOME, KC.END,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,          KC.MNXT,           KC.VOLD, KC.VOLU, KC.MPLY
    ],
    [
        KC.GRV,  KC.N1,    KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.BSPC,
        KC.DEL,  KC.F1,    KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC, KC.BSLS,
        XXXXXXX, KC.NO,    KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.NUHS, KC.NUBS, KC.PGUP, KC.PGDN,
        XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.RGB_TOG, KC.RGB_MODE_PLAIN, KC.RGB_MODE_BREATHE, KC.RGB_MODE_RAINBOW
    ],
]

if __name__ == '__main__':
    keyboard.go()
