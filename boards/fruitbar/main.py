from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.scanners import DiodeOrientation

keyboard = KMKKeyboard()

_______ = KC.TRNS
XXXXXXX = KC.NO

layers = Layers()
# keyboard.extensions = [rgb_ext, led]
keyboard.modules = [layers]

BASE = 0
FN1 = KC.MO(1)
FN2 = KC.MO(2)

keyboard.keymap = [
    # Qwerty
    # ,---------------------------------------------------------------------------------------------------------------.
    # | ESC  |   Q  |   W  |   E  |   R  |   T  |   Y  |   U  |   I  |   O  |   P  |   (  |   )  |   \  |  Next|      |
    # |------+------+------+------+------+------+------+------+------+------+------|------+------+------+------+------|
    # | Tab  |   A  |   S  |   D  |   F  |   G  |   H  |   J  |   K  |   L  |   ;  |   '  | Enter|
    # |------+------+------+------+------+-------------+------+------+------+------|------+------+------+------+------|
    # | Shift|   Z  |   X  |   C  |   V  |   B  |   N  |   M  |   ,  |   .  |   /  |   -  |   =  |   Up |
    # |------+------+------+------+------+------+------+------+------+------+------|------+------+------+------+------|
    # | Ctrl |  GUI |  Alt | Bksp | Space|  FN1 | FN2  |      |      | Left | Down | Right| Bksp |
    # `---------------------------------------------------------------------------------------------------------------'
    [
        KC.ESC,   KC.Q,    KC.W,    KC.E,    KC.R,   KC.T,   KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.LBRC,  KC.RBRC, KC.BSLS, KC.MEDIA_NEXT_TRACK,  KC.TRNS,
        KC.TAB,   KC.A,    KC.S,    KC.D,    KC.F,   KC.G,   KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,  KC.ENT,  KC.BSLS, KC.TRNS,  KC.TRNS,
        KC.LSFT,  KC.Z,    KC.X,    KC.C,    KC.V,   KC.B,   KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.MINS,  KC.EQL,  KC.UP,   KC.TRNS,  KC.TRNS,
        KC.LCTRL, KC.LGUI, KC.LALT, KC.SPC,  KC.SPC, FN1,    FN2,     KC.TRNS, KC.TRNS, KC.TRNS, KC.LEFT, KC.DOWN,  KC.RGHT, KC.BSPC, KC.TRNS,  KC.TRNS,
    ],
    # Alt
    # ,----------------------------------------------------------------------------.
    # | Grave|   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |   0  |
    # |------+------+------+------+------+------+------+------+------+------+------|
    # | Trans|   F1 |   F3 |   F5 |   F7 |   F9 |  F11 |   -  |   ;  |   '  | Trans|
    # |------+------+------+------+------+-------------+------+------+------+------|
    # | Trans|   F2 |   F4 |   F6 |   F8 |  F10 |  F12 |   =  |   (  | Pg Up|   )  |
    # |------+------+------+------+------+------+------+------+------+------+------|
    # | Trans| Trans| Trans| Trans| Trans| Trans|   \  | Home | Pg Dn|  End |  Del |
    # `----------------------------------------------------------------------------'
    [
        KC.GRV,  KC.N1,   KC.N2,   KC.N3,    KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.F1,   KC.F3,   KC.F5,    KC.F7,   KC.F9,   KC.F11,  KC.MINS, KC.SCLN, KC.QUOT, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.F2,   KC.F4,   KC.F6,    KC.F8,   KC.F10,  KC.F12,  KC.EQL,  KC.LBRC, KC.PGUP, KC.RBRC, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,  KC.TRNS, KC.TRNS, KC.BSLS, KC.HOME, KC.PGDN, KC.END,  KC.DEL,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
    ],
    # Alt 2
    # ,----------------------------------------------------------------------------.
    # | Trans|  F1 |   F2 |   F3 |   F4 |   F5 |  F6 |   F7  |   F8  |  F9   | F10 |
    # |------+------+------+------+------+------+------+------+------+------+------|
    # | Trans|   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |   0  |
    # |------+------+------+------+------+-------------+------+------+------+------|
    # | Trans|   F2 |   F4 |   F6 |   F8 |  F10 |  F12 |   =  |   (  | Pg Up|   )  |
    # |------+------+------+------+------+------+------+------+------+------+------|
    # | Trans| Trans| Trans| Trans| Trans| Trans|   \  | Home | Pg Dn|  End |  Del |
    # `----------------------------------------------------------------------------'
    [
        KC.TRNS, KC.F1,   KC.F2,   KC.F3,    KC.F4,   KC.F5,   KC.F6,  KC.F7, KC.F8, KC.F9, KC.F10, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.GRV,  KC.N1,   KC.N2,   KC.N3,    KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.F2,   KC.F4,   KC.F6,    KC.N8,   KC.F10,  KC.F12,  KC.EQL,  KC.LBRC, KC.PGUP, KC.RBRC, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,  KC.TRNS, KC.TRNS, KC.BSLS, KC.HOME, KC.PGDN, KC.END,  KC.DEL, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
    ],
]

if __name__ == '__main__':
    keyboard.go()
