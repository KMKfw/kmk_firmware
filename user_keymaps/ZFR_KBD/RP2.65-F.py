from kb import KMKKeyboard

from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()
keyboard.modules.append(Layers())

keyboard.keymap = [
    [
        KC.GESC,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,  KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.BSLS, KC.DEL,    KC.MINS, KC.EQUAL,
        KC.TAB,   KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,   KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.BSPC,            KC.LBRC, KC.RBRC,
        KC.LCTRL, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,   KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT, KC.ENTER,  KC.HOME, KC.END,
        KC.LSFT,  KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,   KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.RSFT,            KC.UP,
        KC.LCTRL, KC.LGUI, KC.SPC,           KC.SPC,          KC.SPC,           KC.SPC,  KC.RALT, KC.APP,             KC.LEFT, KC.DOWN, KC.RIGHT,
    ],
]

if __name__ == '__main__':
    keyboard.go()
