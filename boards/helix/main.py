from kb import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB
from kmk.keys import KC
from kmk.modules.cg_swap import CgSwap
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide

keyboard = KMKKeyboard()

# RGB backlight support
rgb = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=32, hue_default=80, sat_default=255, val_default=80)
keyboard.extensions.append(rgb)

# Split keyboard support
split_side = SplitSide.LEFT
split_side = SplitSide.RIGHT
split = Split(
    use_pio=True,
    uart_flip=True,
    data_pin=keyboard.data_pin
    )
keyboard.modules.append(split)

# Media key support
keyboard.extensions.append(MediaKeys())

# CG Swap Module
cg_swap = CgSwap()
keyboard.modules.append(cg_swap)

# Layer support
layers_ext = Layers()
keyboard.modules.append(layers_ext)

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

QWERTY = KC.DF(0)
COLEMAK = KC.DF(1)
DVORAK = KC.DF(2)
LOWER = KC.MO(3)
RAISE = KC.MO(4)
ADJUST = KC.MO(5)

RGB_TOG = KC.RGB_TOG
RGB_HUI = KC.RGB_HUI
RGB_HUD = KC.RGB_HUI
RGB_SAI = KC.RGB_SAI
RGB_SAD = KC.RGB_SAD
RGB_VAI = KC.RGB_VAI
RGB_VAD = KC.RGB_VAD

keyboard.keymap = [
    [  # QWERTY
        KC.GRV, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                      KC.N6,  KC.N7,   KC.N8,   KC.N9,   KC.N0,     KC.DEL,
        KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                      KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.BSPC,
        KC.LCTL, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                      KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.LBRC, KC.RBRC, KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.ENT ,
        ADJUST,  KC.ESC,  KC.LALT, KC.LGUI, XXXXXXX,   LOWER,   KC.SPC,  KC.SPC,  RAISE, XXXXXXX,  KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT
    ],
    [  # COLEMAK
        KC.GRV, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                      KC.N6,  KC.N7,   KC.N8,   KC.N9,   KC.N0,     KC.DEL,
        KC.TAB,  KC.Q,    KC.W,    KC.F,    KC.P,    KC.G,                      KC.J,    KC.L,    KC.U,    KC.Y,    KC.SCLN, KC.BSPC,
        KC.LCTL, KC.A,    KC.R,    KC.S,    KC.T,    KC.D,                      KC.H,    KC.N,    KC.E,    KC.I,    KC.O,    KC.QUOT,
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.LBRC, KC.RBRC, KC.K,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.ENT ,
        ADJUST,  KC.ESC,  KC.LALT, KC.LGUI, XXXXXXX,   LOWER,   KC.SPC,  KC.SPC,  RAISE, XXXXXXX,  KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT
    ],
    [  # DVORAK
        KC.GRV, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                      KC.N6,  KC.N7,   KC.N8,   KC.N9,   KC.N0,     KC.DEL,
        KC.TAB,  KC.QUOT, KC.COMM, KC.DOT,  KC.P,    KC.Y,                      KC.F,    KC.G,    KC.C,    KC.R,    KC.L,    KC.DEL,
        KC.LCTL, KC.A,    KC.O,    KC.E,    KC.U,    KC.I,                      KC.D,    KC.H,    KC.T,    KC.N,    KC.S,    KC.SLSH,
        KC.LSFT, KC.SCLN, KC.Q,    KC.J,    KC.K,    KC.X,    KC.LBRC, KC.RBRC, KC.B,    KC.M,    KC.W,    KC.V,    KC.Z,    KC.ENT ,
        ADJUST,  KC.ESC,  KC.LALT, KC.LGUI, XXXXXXX,   LOWER,   KC.SPC,  KC.SPC,  RAISE, XXXXXXX,  KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT
    ],
    [  # LOWER
        KC.TILD, KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC,                   KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, _______,
        KC.TILD, KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC,                   KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, _______,
        _______, KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,                     KC.F6,   KC.UNDS, KC.PLUS, KC.LCBR, KC.RCBR, KC.PIPE,
        KC.CAPS, KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.LPRN, KC.RPRN, KC.F12,  _______, _______, KC.HOME, KC.END,  _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, KC.MNXT, KC.VOLD, KC.VOLU, KC.MPLY
    ],
    [  # RAISE
        KC.GRV, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                     KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,    KC.BSPC,
        KC.GRV, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                     KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,    KC.DEL,
        _______, KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,                     KC.F6,   KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC, KC.BSLS,
        KC.CAPS, KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  _______, _______, KC.F12,  _______, _______, KC.PGDN, KC.PGUP, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, KC.MNXT, KC.VOLD, KC.VOLU, KC.MPLY
    ],
    [  # ADJUSTs
        KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,                     KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,
        _______, KC.RESET, KC.DEBUG, _______, _______, _______,                   _______, _______, _______, _______, _______, KC.DEL,
        _______, _______, _______, _______, _______, KC.CG_NORM,             KC.CG_SWAP, QWERTY,  COLEMAK, DVORAK,  _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, RGB_TOG, RGB_HUI, RGB_SAI, RGB_VAI,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, RGB_HUD, RGB_SAD, RGB_VAD
    ]
]

if __name__ == '__main__':
    keyboard.go()
