from kb import KMKKeyboard

from kmk.extensions.rgb import RGB
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide, SplitType

keyboard = KMKKeyboard()

_______ = KC.TRNS
xxxxxxx = KC.NO

rgb = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=keyboard.rgb_num_pixels)
layers = Layers()

# TODO Comment one of these on each side
split_side = SplitSide.LEFT
split_side = SplitSide.RIGHT
split = Split(split_type=SplitType.BLE, split_side=split_side)

keyboard.extensions = [rgb]
keyboard.modules = [split, layers]


# fmt:off
keyboard.keymap = [
    [
        KC.GESC, KC.N1,   KC.N2,   KC.N3,  KC.N4, KC.N5,                     KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.BSPC,
        KC.TAB,  KC.QUOT, KC.COMM, KC.DOT, KC.P,  KC.Y,                      KC.F,  KC.G,  KC.C,  KC.R,  KC.L,  KC.SLSH,
        KC.LGUI, KC.A,    KC.O,    KC.E,   KC.U,  KC.I,                      KC.D,  KC.H,  KC.T,  KC.N,  KC.S,  KC.ENTER,
        KC.LCTL, KC.SCLN, KC.Q,    KC.J,   KC.K,  KC.X,  KC.MO(2), KC.MO(1), KC.B,  KC.M,  KC.W,  KC.V,  KC.Z,  KC.LALT,
                                    KC.LEFT, KC.RGHT,    KC.LSFT,  KC.SPC,     KC.UP, KC.DOWN,
    ],
    [
        _______, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,                   KC.F10, KC.F11, KC.F12, xxxxxxx, xxxxxxx, _______,
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,                   KC.F7,  KC.F8,  KC.F9,  xxxxxxx, xxxxxxx, KC.EQUAL,
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.INS,                    KC.F4,  KC.F5,  KC.F6,  xxxxxxx, xxxxxxx, xxxxxxx,
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.NO,   _______, KC.F1,  KC.F2,  KC.F3,  xxxxxxx, xxxxxxx, _______,
                                      KC.HOME, KC.END,        _______, xxxxxxx,    KC.PGUP, KC.PGDN,
    ],
    [
        KC.MUTE, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx,                   xxxxxxx, xxxxxxx, xxxxxxx, KC.LBRC,  KC.RBRC, KC.DEL,
        xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx,                   xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, KC.BSLS,
        KC.RGUI, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx,                   xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, KC.MINS,
        xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx, _______, KC.VOLU, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, KC.RALT,
                                      KC.HOME, KC.END,         _______, KC.VOLD,    KC.PGUP, KC.PGDN,
    ],
]
# fmt:off

if __name__ == '__main__':
    keyboard.go()
