from kb import KMKKeyboard
from kmk.extensions.rgb import RGB
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap

keyboard = KMKKeyboard()

# Adding extensions
rgb = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=keyboard.rgb_num_pixels, val_limit=100, hue_default=190, sat_default=100, val_default=5)

modtap = ModTap()
layers_ext = Layers()

keyboard.modules = [layers_ext, modtap]
keyboard.extensions = [rgb]

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(1)
RAISE = KC.MO(2)
ADJUST = KC.LT(3, KC.SPC)
RSFT_ENT = KC.MT(KC.ENT, KC.RSFT)
RSFT_SPC = KC.MT(KC.SPC, KC.RSFT)

RGB_TOG = KC.RGB_TOG
RGB_HUI = KC.RGB_HUI
RGB_HUD = KC.RGB_HUI
RGB_SAI = KC.RGB_SAI
RGB_SAD = KC.RGB_SAD
RGB_VAI = KC.RGB_VAI
RGB_VAD = KC.RGB_VAD

keyboard.keymap = [
    [  #QWERTY
        KC.TAB,    KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                         KC.Y,    KC.U,    KC.I,    KC.O,   KC.P,  KC.BSPC,
        KC.LCTL,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                         KC.H,    KC.J,    KC.K,    KC.L, KC.SCLN, KC.QUOT,
        KC.LSFT,   KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,                         KC.N,    KC.M, KC.COMM,  KC.DOT, KC.SLSH, RSFT_ENT,
                                            KC.LALT,   LOWER,       KC.SPC,          RAISE,   KC.RGUI,
    ],
    [  #LOWER
        KC.ESC,   KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                        KC.N6,   KC.N7,  KC.N8,   KC.N9,   KC.N0, KC.BSPC,
        KC.LCTL, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                       KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT, XXXXXXX, XXXXXXX,
        KC.LSFT, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                       XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, RSFT_SPC,
                                            KC.LALT,   LOWER,       KC.SPC,         RAISE,   KC.RGUI,
    ],
    [  #RAISE
        KC.ESC, KC.EXLM,   KC.AT, KC.HASH,  KC.DLR, KC.PERC,                      KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.BSPC,
        KC.LCTL, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                     KC.MINS, KC.EQL, KC.LCBR, KC.RCBR, KC.PIPE,  KC.GRV,
        KC.LSFT, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                     KC.UNDS, KC.PLUS, KC.LBRC, KC.RBRC, KC.BSLS, KC.TILD,
                                            KC.LALT,   LOWER,       KC.SPC,       RAISE,   KC.RGUI,
    ],
    [  #ADJUST
        RGB_TOG, RGB_HUI, RGB_SAI, RGB_VAI, XXXXXXX, XXXXXXX,                      XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        XXXXXXX, RGB_HUD, RGB_SAD, RGB_VAD, XXXXXXX, XXXXXXX,                      XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                      XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
                                            KC.LALT,   LOWER,       KC.SPC,        RAISE,   KC.RGUI,
    ]
]

if __name__ == '__main__':
    keyboard.go()
