# PyKey60 designed by jpconstantineau
# https://github.com/jpconstantineau/PyKey60
# Requires CircuitPython 7.0.0 to support the RP2040 MCU

from kb import KMKKeyboard

from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()
keyboard.modules.append(Layers())

rgb_ext = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=keyboard.rgb_num_pixels, animation_mode=AnimationModes.STATIC)
keyboard.extensions.append(rgb_ext)

FN = KC.MO(1)
FN2 = KC.MO(2)
XXXXXXX = KC.TRNS

keyboard.keymap = [
    # Qwerty
    # ,-------------------------------------------------------------------------------------------------.
    # | ESC  |   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |   0  |   -  |   =  | Bksp |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Tab  |   Q  |   W  |   E  |   R  |   T  |   Y  |   U  |   I  |   O  |   P  |   [  |   ]  |   \  |
    # |------+------+------+------+------+-------------+------+------+------+------+------+------+------|
    # | Caps |   A  |   S  |   D  |   F  |   G  |   H  |   J  |   K  |   L  |   ;  |   '  |XXXXXX| Enter|
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Shift|   Z  |   X  |   C  |   V  |   B  |   N  |   M  |   ,  |   .  |   /  |XXXXXX|XXXXXX| Shift|
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Ctrl | GUI  |  Alt |XXXXXX|XXXXXX| Space|XXXXXX|XXXXXX|XXXXXX| Alt  | GUI  | Fn   |XXXXXX| Ctrl |
    # `------------------------------------------------------------------------------------------+------'
    [
        KC.GESC,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,  KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.MINS, KC.EQUAL, KC.BSPC,
        KC.TAB,   KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,   KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.LBRC, KC.RBRC,  KC.BSLASH,
        FN2,      KC.A,    KC.S,    KC.D,    KC.F,    KC.G,   KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT, XXXXXXX,  KC.ENTER,
        KC.LSFT,  KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,   KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, XXXXXXX, XXXXXXX,  KC.RSFT,
        KC.LCTRL, KC.LGUI, KC.LALT, XXXXXXX, XXXXXXX, KC.SPC, XXXXXXX, XXXXXXX, XXXXXXX, KC.RALT, KC.RGUI, FN,      XXXXXXX,  KC.RCTRL
    ],
    # Alt
    # ,-------------------------------------------------------------------------------------------------.
    # |   `  |  F1  |  F2  |  F3  |  F4  |  F5  |  F6  |  F7  |  F8  |  F9  | F10  | F11  | F12  | Del  |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # |      |      |  UP  |      |      |      |      |      | Insrt| Home | PgUp |      |      |      |
    # |------+------+------+------+------+-------------+------+------+------+------+------+------+------|
    # |      | LEFT | DOWN | RIGHT|      |      |      |      | Del  | End  | PgDn |      |      |      |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # |      |      |      |      |      |      |      | MUTE | VOLD | VOLU |      |      |      |      |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # |      |      |      |      |      |      |      |      |      |      | App  | Fn   |      |      |
    # `------------------------------------------------------------------------------------------+------'
    [
        KC.GRV,  KC.F1,   KC.F2,   KC.F3,    KC.F4,   KC.F5,   KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,   KC.F12,  KC.DEL,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.INS,  KC.HOME, KC.PGUP, XXXXXXX,  XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.DEL,  KC.END,  KC.PGDN, XXXXXXX,  XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, KC.MUTE, KC.VOLD, KC.VOLU, XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.APP,  XXXXXXX,  XXXXXXX, XXXXXXX,
    ],
    # Arrows
    # ,-------------------------------------------------------------------------------------------------.
    # |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
    # |------+------+------+------+------+-------------+------+------+------+------+------+------+------|
    # |      | RGB T| RGB R|      |      |      |      |      |      |      |      |      |      |      |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # |      |      |      |      |      |      |      |      |      |      |      |      |      |  UP  |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # |      |      |      |      |      |      |      |      |      |      | LEFT | DOWN |      | RGHT |
    # `------------------------------------------------------------------------------------------+------'
    [
        XXXXXXX, XXXXXXX,    XXXXXXX,               XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX,    XXXXXXX,               XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX,
        XXXXXXX, KC.RGB_TOG, KC.RGB_MODE_RAINBOW,   XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX,    XXXXXXX,               XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,  XXXXXXX, KC.UP,
        XXXXXXX, XXXXXXX,    XXXXXXX,               XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.LEFT, KC.DOWN,  XXXXXXX, KC.RIGHT
    ],
]

if __name__ == '__main__':
    keyboard.go()
