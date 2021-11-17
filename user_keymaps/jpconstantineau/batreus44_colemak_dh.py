# Batreus44 designed by jpconstantineau
# https://github.com/jpconstantineau/Batreus44
# Board can use different controllers.
# Edit last 2 lines if you have a nRF52840 and want BLE

from kb import KMKKeyboard
from kmk.hid import HIDModes
from kmk.keys import KC
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()
keyboard.modules.append(Layers())

FUN = KC.MO(1)
UPPER = KC.MO(2)
XXXXXXX = KC.TRNS

keyboard.keymap = [
    # Colemak Mod-DH See https://colemakmods.github.io/mod-dh/keyboards.html
    [
        KC.Q,       KC.W,       KC.F,       KC.P,       KC.B,           KC.NO,      KC.NO,      KC.J,       KC.L,       KC.U,       KC.Y,       KC.SCLN,
        KC.A,       KC.R,       KC.S,       KC.T,       KC.G,           KC.NO,      KC.NO,      KC.M,       KC.N,       KC.E,       KC.I,       KC.O,
        KC.Z,       KC.X,       KC.C,       KC.D,       KC.V,           KC.GRAVE,  KC.BACKSLASH, KC.K,     KC.H,       KC.COMM,    KC.DOT,     KC.SLSH,
        KC.ESC,     KC.TAB,     KC.LGUI,    KC.LSHIFT,  KC.BACKSPACE,   KC.LCTRL,   KC.LALT,    KC.SPC,     FUN,        KC.MINUS,   KC.QUOT,    KC.ENTER,
    ],
    [
        KC.EXLM,    KC.AT,      KC.UP,      KC.DLR,     KC.PERC,        KC.NO,      KC.NO,      KC.PGUP,    KC.N7,      KC.N8,      KC.N9,      KC.BACKSPACE,
        KC.LPRN,    KC.LEFT,    KC.DOWN,    KC.RIGHT,   KC.RPRN,        KC.NO,      KC.NO,      KC.PGDN,    KC.N4,      KC.N5,      KC.N6,      KC.SCOLON,
        KC.LBRC,    KC.RBRC,    KC.HASH,    KC.LCBR,    KC.RCBR,        KC.CIRC,    KC.AMPR,    KC.ASTR,    KC.N1,      KC.N2,      KC.N3,      KC.PLUS,
        UPPER,      KC.INSERT,  XXXXXXX,    XXXXXXX,    XXXXXXX,        XXXXXXX,    XXXXXXX,    XXXXXXX,    XXXXXXX,    XXXXXXX,    KC.N0,      KC.EQL,
    ],
    [
        KC.INSERT,  KC.HOME,    KC.UP,      KC.END,     KC.PGUP,    KC.NO,      KC.NO,          KC.UP,      KC.F7,      KC.F8,      KC.F9,      KC.F10,
        KC.DEL,     KC.LEFT,    KC.DOWN,    KC.RIGHT,   KC.PGDN,    KC.NO,      KC.NO,          KC.DOWN,    KC.F4,      KC.F5,      KC.F6,      KC.F11,
        KC.NO,      KC.VOLU,    XXXXXXX,    XXXXXXX,    XXXXXXX,    XXXXXXX,    XXXXXXX,        XXXXXXX,    KC.F1,      KC.F2,      KC.F3,      KC.F12,
        UPPER,      KC.VOLD,    XXXXXXX,    XXXXXXX,    XXXXXXX,    XXXXXXX,    XXXXXXX,        XXXXXXX,    XXXXXXX,    KC.PSCR,    KC.SLCK,    KC.PAUS,
    ],
]

if __name__ == '__main__':
    #  keyboard.go(hid_type=HIDModes.BLE, ble_name='Batreus44')
    keyboard.go(hid_type=HIDModes.USB)
