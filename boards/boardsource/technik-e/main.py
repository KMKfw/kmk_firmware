from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.hid import HIDModes

keyboard = KMKKeyboard()


modtap = ModTap()
layers_ext = Layers()

keyboard.modules = [layers_ext, modtap]
# keymap
keyboard.keymap = [[
        KC.L,    KC.W,    KC.E,    KC.R,    KC.T,                         KC.Y,    KC.U,    KC.I,    KC.O,   KC.L,
        KC.L,    KC.S,    KC.D,    KC.F,    KC.G,                         KC.H,    KC.J,    KC.K,    KC.L,  KC.L,
        KC.L,    KC.X,    KC.C,    KC.V,    KC.B,                         KC.N,    KC.M,    KC.COMM, KC.DOT,KC.L,
        KC.LALT,            KC.L,       KC.LCTRL,     KC.L,        KC.L,    KC.L,      KC.TAB,            KC.MO(3),
    ],
    [
        KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                        KC.N6,   KC.N7,  KC.N8,   KC.N9,   KC.N0,
        KC.ESC, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                       KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT, KC.QUOTE,
        KC.TRNS, KC.GRV, KC.TRNS, KC.TRNS, KC.TRNS,                       KC.MINS, KC.EQL, KC.LCBR, KC.RCBR, KC.BSLS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,    KC.TRNS, KC.TRNS, KC.TRNS,KC.TRNS
    ],
    [  
         KC.EXLM,   KC.AT, KC.HASH,  KC.DLR, KC.PERC,                      KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN,
         KC.ESC, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                      KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT, KC.DQT,
         KC.ESC, KC.TILD, KC.TRNS, KC.TRNS, KC.TRNS,                     KC.UNDS, KC.PLUS, KC.LBRC, KC.RBRC, KC.PIPE,
         KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,    KC.TRNS, KC.TRNS, KC.TRNS,KC.TRNS
    ],
    [  
         KC.F1,    KC.F2,    KC.F3,    KC.F4,    KC.F5,                     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
         KC.F6,    KC.F7,    KC.F8,    KC.F9,   KC.F10,                     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
         KC.F11 ,  KC.F12,   KC.DEL,   KC.TRNS, KC.TRNS,                    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
         KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,    KC.TRNS, KC.TRNS, KC.TRNS,KC.TRNS
    ],
     
]
# keymap

if __name__ == '__main__':
    keyboard.go()
    # keyboard.go(hid_type=HIDModes.BLE)
    # keyboard.go(hid_type=HIDModes.BLE, ble_name='KMKeyboard')