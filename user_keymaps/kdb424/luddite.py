from kb import KMKKeyboard

from kmk.extensions.rgb import RGB
from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()

# ---------------------------------- Config  --------------------------------------------

keyboard.tap_time = 150

keyboard.debug_enabled = False


# ---------------------- Custom Functions --------------------------------------------

BASE = 0
GAMING = 1
FN1 = 2

rgb_ext = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=16)
layers_ext = Layers()
holdtap = HoldTap()

keyboard.modules = [layers_ext, holdtap]
keyboard.extensions = [rgb_ext]

_______ = KC.TRNS
XXXXXXX = KC.NO
HOME = KC.HT(KC.HOME, KC.LSFT)
END = KC.HT(KC.END, KC.RSFT)
LEFT_LAY = KC.LT(FN1, KC.LEFT)
SHFT_INS = KC.LSFT(KC.INS)
SPC = KC.LT(FN1, KC.SPC)


# ---------------------- Keymap ---------------------------------------------------------


keyboard.keymap = [
    # df
    [
        KC.GESC, KC.N1,   KC.N2,   KC.N3,  KC.N4,   KC.N5,   KC.N6,   KC.N7, KC.N8, KC.N9, KC.N0, KC.LBRC, KC.RBRC, KC.BSPC,
        KC.RGB_TOG, KC.QUOT, KC.COMM, KC.DOT, KC.P,    KC.Y,    KC.F,    KC.G,  KC.C,  KC.R,  KC.L,  KC.SLSH, KC.EQL,  KC.BSLS,
        KC.TAB,  KC.A,    KC.O,    KC.E,   KC.U,    KC.I,    KC.D,    KC.H,  KC.T,  KC.N,  KC.S,  KC.MINS, KC.ENT,
        KC.LSFT, KC.SCLN, KC.Q,    KC.J,   KC.K,    KC.X,    KC.B,    KC.M,  KC.W,  KC.V,  KC.Z,  KC.RSFT,
        KC.LCTL, KC.LGUI, KC.LALT,           SPC,              KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT,
    ],

    # df
    [
        KC.GESC, KC.N1,   KC.N2,   KC.N3,  KC.N4,   KC.N5,   KC.N6,   KC.N7, KC.N8, KC.N9, KC.N0, KC.LBRC, KC.RBRC, KC.BSPC,
        KC.RGB_TOG, KC.QUOT, KC.COMM, KC.DOT, KC.P,    KC.Y,    KC.F,    KC.G,  KC.C,  KC.R,  KC.L,  KC.SLSH, KC.EQL,  KC.BSLS,
        KC.TAB,  KC.A,    KC.O,    KC.E,   KC.U,    KC.I,    KC.D,    KC.H,  KC.T,  KC.N,  KC.S,  KC.MINS, KC.ENT,
        KC.LSFT, KC.SCLN, KC.Q,    KC.J,   KC.K,    KC.X,    KC.B,    KC.M,  KC.W,  KC.V,  KC.Z,  KC.RSFT,
        KC.LCTL, KC.LGUI, KC.LALT,        KC.SPC,              LEFT_LAY, KC.DOWN, KC.UP,   KC.RIGHT,
    ],

    # fn
    [
        KC.GESC, KC.F1,      KC.F2,      KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.F7, KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.DEL,
        KC.RESET, KC.RGB_HUD, KC.RGB_HUI, _______, _______, _______, _______, _______, _______, KC.RGB_M_S, _______, _______, KC.VOLU, SHFT_INS,
        KC.RGB_ANI, KC.RGB_SAD, KC.RGB_SAI, _______, _______, _______, _______, _______, KC.RGB_TOG, _______, KC.RGB_M_P, KC.VOLD, _______,
        KC.RGB_AND, KC.RGB_VAD, KC.RGB_VAI, _______, _______, _______, _______, _______,    _______,    _______,    _______, _______,
        _______, _______,    _______,    _______, _______, _______, KC.DF(0),     KC.DF(1),
    ],
]

if __name__ == '__main__':
    keyboard.go()
