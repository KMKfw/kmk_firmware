import board

from kb import KMKKeyboard

from kmk.extensions.rgb import RGB
from kmk.handlers.sequences import send_string, simple_key_sequence
from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.split import Split

keyboard = KMKKeyboard()

# ------------------User level config variables ---------------------------------------
keyboard.tap_time = 150

layers = Layers()
holdtap = HoldTap()
rgb_ext = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=27, val_limit=100, hue_default=190, sat_default=100, val_default=5)
split = Split()

keyboard.modules = [holdtap, layers, split]
keyboard.extensions = [rgb_ext]

_______ = KC.TRNS
XXXXXXX = KC.NO
SHFT_INS = KC.LSHIFT(KC.INS)

BASE = KC.DF(0)
GAMING = KC.DF(1)
LT1_SP = KC.MO(2)
LT2_SP = KC.LT(3, KC.SPC)
TAB_SB = KC.LT(5, KC.TAB)
SUPER_L = KC.LM(4, KC.LGUI)

# ---------------------- Keymap ---------------------------------------------------------

keyboard.keymap = [
    [
        # df
        KC.GRV,   KC.N1,    KC.N2,    KC.N3,   KC.N4,   KC.N5,  KC.N6,  KC.N7,   KC.N8,   KC.N9,   KC.N0, KC.DEL,
        KC.GESC,  KC.QUOT,  KC.COMM,  KC.DOT,  KC.P,    KC.Y,   KC.F,   KC.G,    KC.C,    KC.R,    KC.L,   KC.BSPC,
        TAB_SB,   KC.A,     KC.O,     KC.E,    KC.U,    KC.I,   KC.D,   KC.H,    KC.T,    KC.N,    KC.S,   KC.ENT,
        KC.LSFT,  KC.SCLN,  KC.Q,     KC.J,    KC.K,    KC.X,   KC.B,   KC.M,    KC.W,    KC.V,    KC.Z,   KC.SLSH,
        KC.LCTRL, KC.LGUI,  KC.LALT,  KC.LALT, SUPER_L, LT1_SP, LT2_SP, KC.LCTL, KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT,
    ],

    [
        # gw
        KC.GESC,  KC.N1,   KC.N2,   KC.N3,  KC.N4, KC.N5,  KC.N6,  KC.N7,     KC.N8,   KC.N9,   KC.N0, KC.DEL,
        KC.TAB,   KC.QUOT, KC.COMM, KC.DOT, KC.P,  KC.Y,   KC.F,   KC.G,      KC.C,    KC.R,    KC.L,  KC.BKSP,
        KC.ESC,   KC.A,    KC.O,    KC.E,   KC.U,  KC.I,   KC.D,   KC.H,      KC.T,    KC.N,    KC.S,  KC.ENT,
        KC.LSFT,  KC.SCLN, KC.Q,    KC.J,   KC.K,  KC.X,   KC.B,   KC.M,      KC.W,    KC.V,    KC.Z,  KC.SLSH,
        KC.LCTRL, KC.LGUI, KC.LALT, KC.F1,  KC.F2, KC.SPC, LT2_SP, KC.MO(4), KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT,
    ],
    [
        # r1
        KC.GESC,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.DEL,
        _______, _______, _______, _______, _______, _______,  _______, XXXXXXX, KC.N7, KC.N8,   KC.N9,   KC.DEL,
        _______, _______, _______, _______, _______, _______,  XXXXXXX, XXXXXXX, KC.N4,   KC.N5,   KC.N6,   KC.BSLS,
        _______, _______, _______, _______, _______, _______,  XXXXXXX, XXXXXXX, KC.N1,   KC.N2,   KC.N3,   KC.MINS,
        KC.RESET, _______, _______, _______, _______, _______, _______, KC.EQL,  KC.N0,   XXXXXXX, XXXXXXX, XXXXXXX,
    ],
    [
        # r2
        KC.GESC, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,    KC.N9,    KC.N0,   KC.DEL,
        _______, KC.F9,   KC.F10,  KC.F11,  KC.F12,  _______, _______, _______, _______,  KC.LBRC,  KC.RBRC, KC.LSHIFT(KC.INS),
        _______, KC.F5,   KC.F6,   KC.F7,   KC.F8,   _______, KC.HOME, KC.LEFT, KC.DOWN,  KC.UP,    KC.RGHT, KC.END,
        _______, KC.F1,   KC.F2,   KC.F3,   KC.F4,   _______, _______, _______, _______,  _______,  _______, KC.BSLS,
        _______, _______, _______, _______, _______, _______, _______, _______, KC.DF(0), KC.DF(1), _______, _______
    ],
    [
        # GUI
        KC.GESC, KC.RGB_M_P, KC.RGB_M_K, KC.RGB_M_B, KC.RGB_M_BR, KC.RGB_M_S, _______, _______, KC.F10,  KC.F11,  KC.F12,  KC.DEL,
        _______, KC.N1,      KC.N2,      KC.N3,      KC.N4,       KC.N5,      _______, _______, _______, _______, _______, _______,
        _______, KC.N6,      KC.N7,      KC.N8,      KC.N9,       KC.N0,      _______, _______, _______, _______, _______, _______,
        _______, _______,    _______,    _______,    _______,     _______,    _______, _______, _______, _______, _______, _______,
        _______, _______,    _______,    _______,    _______,     _______,    _______, _______, _______, _______, _______, _______
    ],
    [
        # Symbols
        _______, _______,    _______,    _______,    _______,     _______,    _______, _______, _______, _______, _______, _______,
        _______, KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC,                     KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.DEL,
        _______, KC.RGB_HUI, KC.RGB_HUD, KC.RGB_VAI, KC.RGB_VAD, _______,                     _______, _______, _______, KC.LBRC, KC.RBRC, _______,
        _______, KC.RGB_RST, _______, _______, _______, _______,                     _______, _______, _______, _______, _______, _______,
        _______, _______,    _______, KC.RGB_TOG,    _______,     _______,    _______, _______, _______, _______, _______, _______
    ],
]

if __name__ == '__main__':
    keyboard.go()
