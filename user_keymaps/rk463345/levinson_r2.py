from kb import KMKKeyboard

from kmk.consts import UnicodeMode
from kmk.extensions.rgb import RGB
from kmk.handlers.sequences import compile_unicode_string_sequences
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.media_keys import MediaKeys
from kmk.modules.split import Split, SplitType

keyboard = KMKKeyboard()
layers = Layers()
media_keys = MediaKeys()
split = Split(split_type=SplitType.UART)
rgb_ext = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=16, val_limit=150, hue_default=0, sat_default=100, val_default=20)
keyboard.modules = [layers, media_keys, split]
keyboard.extensions = [rgb_ext]


# ------------------User level config variables ---------------------------------------
keyboard.unicode_mode = UnicodeMode.LINUX
keyboard.tap_time = 150

keyboard.debug_enabled = False

LOWER = KC.TT(3)
UP_HYP = KC.LT(4, KC.MINS)
_______ = KC.TRNS
XXXXXXX = KC.NO

# ---------------------- Keymap ---------------------------------------------------------

keyboard.keymap = [
    [
        # Default
        KC.GESC,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.BSPC,
        KC.TAB,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,
        KC.LSFT,  KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.HT(KC.BSLS, KC.LSFT),
        KC.LCTRL, KC.LGUI, KC.LALT, LOWER,   KC.ENT,  KC.SPC,  KC.SPC,  UP_HYP,  KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT,
    ],
    [
        # Dvorak
        KC.GESC,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.BSPC,
        KC.TAB,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,
        KC.LSFT,  KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.B,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.ENT,
        KC.LCTRL, KC.F9,   KC.LALT, KC.F6,   KC.SPC,  KC.F7,   KC.SPC,  UP_HYP,  KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT,

    ],
    [
        # Gaming
        KC.GESC,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.BSPC,
        KC.TAB,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,
        KC.LSFT,  KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.ENT,
        KC.LCTRL, KC.F9,   KC.LALT, KC.F6,   KC.SPC,  KC.F7,   KC.SPC,  UP_HYP,  KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT,
    ],
    [
        # Lower
        _______, XXXXXXX, XXXXXXX, KC.MUTE, KC.VOLD, KC.VOLU, KC.LPRN, KC.RPRN, KC.N7,    KC.N8,    KC.N9,    KC.MINS,
        _______, XXXXXXX, KC.DEL,  XXXXXXX, KC.PGUP, KC.PGDN, KC.LBRC, KC.RBRC, KC.N4,    KC.N5,    KC.N6,    KC.PLUS,
        _______, KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT, XXXXXXX, KC.EQL,  KC.EXLM, KC.N1,    KC.N2,    KC.N3,    XXXXXXX,
        _______, _______, _______, _______, _______, _______, _______, _______, KC.N0,    KC.N0,    KC.ENT,   KC.ENT,
    ],
    [
        # Raise
        KC.GRV,              KC.N1,    KC.N2,    KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.DEL,
        KC.RGB_MODE_RAINBOW, KC.F1,    KC.F2,    KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC, KC.BSLS,
        KC.RGB_TOG,          KC.F7,    KC.F8,    KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.NUHS, KC.NUBS, _______, _______, _______,
        KC.DF(0),            KC.DF(1), KC.DF(2), _______, _______, _______, _______, _______, KC.HOME, KC.VOLD, KC.VOLU, KC.END,
    ],
]

if __name__ == '__main__':
    keyboard.go()
