from kb import KMKKeyboard

from kmk.consts import UnicodeMode
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitType

keyboard = KMKKeyboard()
layers = Layers()
split = Split(split_type=SplitType.UART)
keyboard.modules = [layers, split]

keyboard.debug_enabled = False
keyboard.unicode_mode = UnicodeMode.LINUX
keyboard.tap_time = 750

_______ = KC.TRNS
xxxxxxx = KC.NO
# Warning. keymap is missing two keys on it's bottom/5th row.... might be fine if you are using an encoder on those keys... I've no idea,
# but you've been warned.
# fmt:off
keyboard.keymap = [
    [
        KC.GESC, KC.N1,   KC.N2,   KC.N3,  KC.N4, KC.N5,                     KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.BSPC,
        KC.TAB,  KC.QUOT, KC.COMM, KC.DOT, KC.P,  KC.Y,                      KC.F,  KC.G,  KC.C,  KC.R,  KC.L,  KC.SLSH,
        KC.LGUI, KC.A,    KC.O,    KC.E,   KC.U,  KC.I,                      KC.D,  KC.H,  KC.T,  KC.N,  KC.S,  KC.ENTER,
        KC.LCTL, KC.SCLN, KC.Q,    KC.J,   KC.K,  KC.X,                      KC.B,  KC.M,  KC.W,  KC.V,  KC.Z,  KC.LALT,
                    KC.LEFT, KC.RGHT,    KC.LSFT, KC.MO(2),  KC.MO(1), KC.SPC,     KC.UP, KC.DOWN,
    ],
    [
        _______, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,                   KC.F10, KC.F11, KC.F12, xxxxxxx, xxxxxxx, _______,
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,                   KC.F7,  KC.F8,  KC.F9,  xxxxxxx, xxxxxxx, KC.EQUAL,
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.INS,                    KC.F4,  KC.F5,  KC.F6,  xxxxxxx, xxxxxxx, xxxxxxx,
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,                   KC.F1,  KC.F2,  KC.F3,  xxxxxxx, xxxxxxx, _______,
                                      KC.HOME, KC.END, _______, KC.NO, _______,  xxxxxxx,    KC.PGUP, KC.PGDN,
    ],
    [
        KC.MUTE, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx,                   xxxxxxx, xxxxxxx, xxxxxxx, KC.LBRC,  KC.RBRC, KC.DEL,
        xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx,                   xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, KC.BSLS,
        KC.RGUI, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx,                   xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, KC.MINS,
        xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx,                   xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, KC.RALT,
                                      KC.HOME, KC.END, _______, _______, KC.VOLU, KC.VOLD,    KC.PGUP, KC.PGDN,
    ],
]
# fmt:on

if __name__ == '__main__':
    keyboard.go()
