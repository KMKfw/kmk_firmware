from kb import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB
from kmk.keys import KC
from kmk.modules.capsword import CapsWord
from kmk.modules.cg_swap import CgSwap
from kmk.modules.layers import Layers
from kmk.modules.split import Split
from kmk.modules.sticky_keys import StickyKeys

keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys())

rgb = RGB(
    pixel_pin=keyboard.rgb_pixel_pin,
    num_pixels=5,
)
keyboard.extensions.append(rgb)
keyboard.modules.append(CapsWord())
keyboard.modules.append(CgSwap())
keyboard.modules.append(Layers())
keyboard.modules.append(StickyKeys())
split = Split(data_pin=keyboard.data_pin)
keyboard.modules.append(split)

SK_LSFT = KC.SK(KC.LSFT)
LYR3 = KC.MO(3)
LYR4 = KC.MO(4)
LYR5 = KC.MO(5)
SK_RALT = KC.SK(KC.RALT)
RGB_M_P = KC.RGB_MODE_PLAIN
RGB_M_B = KC.RGB_MODE_BREATHE
RGB_M_R = KC.RGB_MODE_RAINBOW
RGB_M_BR = KC.RGB_MODE_BREATHE_RAINBOW
RGB_M_K = KC.RGB_MODE_KNIGHT
RGB_M_S = KC.RGB_MODE_SWIRL

# fmt:off
keyboard.keymap = [
    [   #QWERTY
        KC.GRV,  KC.Q,    KC.W,   KC.E,  KC.R,    KC.T,                                    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.BSPC,
        KC.TAB,  KC.A,    KC.S,   KC.D,  KC.F,    KC.G,                                    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.ENT,
        KC.LSFT, KC.Z,    KC.X,   KC.C,  KC.V,    KC.B,    KC.NO,                  KC.NO,  KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.RSFT,
        KC.LCTL,          KC.ESC,        KC.LGUI, KC.LALT, KC.SPC, LYR3,     LYR4, KC.SPC, KC.LALT, KC.RGUI,          KC.UP,            KC.QUOT,
                 KC.CAPS, KC.NO,  KC.NO,                                                                     KC.LEFT, KC.DOWN, KC.RGHT,
    ],
    [   #DVORAK
        KC.TRNS, KC.QUOT, KC.COMM, KC.DOT, KC.P,    KC.Y,                                            KC.F,    KC.G,    KC.C,    KC.R,    KC.L,    KC.TRNS,
        KC.TRNS, KC.TRNS, KC.O,    KC.E,   KC.U,    KC.I,                                            KC.D,    KC.H,    KC.T,    KC.N,    KC.S,    KC.TRNS,
        KC.TRNS, KC.SCLN, KC.Q,    KC.J,   KC.K,    KC.X,    KC.TRNS,                       KC.TRNS, KC.B,    KC.TRNS, KC.W,    KC.V,    KC.Z,    KC.TRNS,
        KC.TRNS,          KC.TRNS,         KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,          KC.TRNS,          KC.SLSH,
                 KC.TRNS, KC.TRNS, KC.TRNS,                                                                            KC.TRNS, KC.TRNS, KC.TRNS,
    ],
    [   #COLEMAK_DH
        KC.TRNS, KC.Q,    KC.W,    KC.F,    KC.P,    KC.B,                                            KC.J,    KC.L,    KC.U,    KC.Y,    KC.SCLN, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.R,    KC.S,    KC.T,    KC.G,                                            KC.M,    KC.N,    KC.E,    KC.I,    KC.O,    KC.TRNS,
        KC.TRNS, KC.Z,    KC.X,    KC.C,    KC.D,    KC.V,    KC.TRNS,                       KC.TRNS, KC.K,    KC.H,    KC.COMM, KC.DOT,  KC.SLSH, KC.TRNS,
        KC.TRNS,          KC.TRNS,          KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,          KC.TRNS,          KC.QUOT,
                 KC.TRNS, KC.TRNS, KC.TRNS,                                                                             KC.TRNS, KC.TRNS, KC.TRNS,
    ],
    [
        KC.INS,  KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC,                                     KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.TRNS,
        KC.TRNS, KC.LGUI, KC.LALT, KC.LCTL, KC.LSFT, KC.NO,                                       KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC, KC.BSLS, KC.TRNS,
        KC.TRNS, KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   SK_RALT,                    KC.APP, KC.UNDS, KC.PLUS, KC.LCBR, KC.RCBR, KC.PIPE, KC.TRNS,
        KC.TRNS,          KC.NO,            KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     LYR5, KC.DEL, KC.TRNS, KC.TRNS,          KC.PGUP,          KC.TRNS,
                 KC.NO,   KC.NO,   KC.NO,                                                                           KC.HOME, KC.PGDN, KC.END,
    ],
    [
        KC.NO,   KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                                        KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.TRNS,
        KC.TRNS, KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,                                        KC.MPLY, KC.LSFT, KC.LCTL, KC.LALT, KC.LGUI, KC.TRNS,
        KC.TRNS, KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,   KC.PSCR,                   KC.MUTE, KC.MRWD, KC.MFFD, KC.COMM, KC.DOT,  KC.MINS, KC.TRNS,
        KC.TRNS,          KC.F12,           KC.TRNS, KC.TRNS, KC.TRNS, LYR5,     KC.TRNS, KC.SPC,  KC.TRNS, KC.TRNS,          KC.NO,            KC.TRNS,
                  KC.F11, KC.NO, KC.NO,                                                                              KC.NO,   KC.VOLD, KC.VOLU,
    ],
    [
        KC.NO,    KC.DF(0), KC.DF(1), KC.DF(2), KC.CG_SWAP, KC.NO,                                               KC.NO,   KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,
        KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.CG_NORM, KC.NO,                                               KC.NO,   KC.RGB_VAI, KC.RGB_HUI, KC.RGB_SAI, KC.RGB_ANI, KC.NO,
        KC.RESET, KC.NO,    KC.BRID,  KC.BRIU,  KC.NO,      RGB_M_P,  KC.NO,                         KC.RGB_TOG, RGB_M_B, KC.RGB_VAD, KC.RGB_HUD, KC.RGB_SAD, KC.RGB_AND, KC.NO,
        KC.NO,              KC.NO,              KC.NO,      RGB_M_BR, RGB_M_R, KC.TRNS,     KC.TRNS, RGB_M_K,    RGB_M_K, KC.NO,                  KC.NO,                  KC.NO,
                  KC.NO,    KC.NO,    KC.NO,                                                                                          KC.NO,      KC.NO,      KC.NO,
    ]
]
# fmt:on

if __name__ == '__main__':
    keyboard.go()
