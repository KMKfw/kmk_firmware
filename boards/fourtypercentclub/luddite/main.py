from kb import KMKKeyboard
from kmk.extensions.led import LED
from kmk.extensions.rgb import RGB
from kmk.keys import KC
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()

_______ = KC.TRNS
XXXXXXX = KC.NO

rgb_ext = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=keyboard.rgb_num_pixels)
led = LED()
layers_ext = Layers()
keyboard.extensions = [rgb_ext, led]
keyboard.modules = [layers_ext]

BASE = 0
FN1 = 1

keyboard.keymap = [
    [
        KC.GESC, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.MINS, KC.EQL,  KC.BSPC,
        KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.LBRC, KC.RBRC, KC.BSLS,
        KC.CAPS, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,           KC.ENT,
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH,                   KC.RSFT,
        KC.LCTL,  KC.LGUI,  KC.LALT,                       KC.SPC,                     KC.RALT, KC.RGUI, KC.MO(FN1), KC.RCTL,
    ],

    [
        KC.GESC,    KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.BSPC,
        KC.RGB_TOG, _______, KC.UP,   _______,   _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, KC.LEFT, KC.DOWN, KC.RGHT, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        KC.LED_INC, KC.LED_DEC, KC.LED_TOG, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        KC.GRV, _______, _______, _______, _______,          _______, _______, _______,
    ],
]

if __name__ == '__main__':
    keyboard.go()
