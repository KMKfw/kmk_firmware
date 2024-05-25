from kb import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.split import Split

keyboard = KMKKeyboard()

keyboard.extensions.append(MediaKeys())
keyboard.modules.append(Layers())

split = Split(
    data_pin=keyboard.data_pin,
    # data_pin2=keyboard.data_pin2,
)
keyboard.modules.append(split)

CTLTAB = KC.LCTL(KC.TAB)
ALTTAB = KC.LALT(KC.TAB)

# fmt:off
keyboard.keymap = [
    [   #0
        KC.ESC,   KC.N1,   KC.N2,   KC.N3, KC.N4, KC.N5,  CTLTAB,                           ALTTAB, KC.N6, KC.N7,   KC.N8,   KC.N9,   KC.N0,  KC.GRV,
        KC.TAB,    KC.Q,    KC.W,    KC.E,  KC.R,  KC.T, KC.LBRC,                          KC.RBRC,  KC.Y,  KC.U,    KC.I,    KC.O,    KC.P, KC.BSLS,
        KC.CAPS,   KC.A,    KC.S,    KC.D,  KC.F,  KC.G, KC.HOME,                           KC.END,  KC.H,  KC.J,    KC.K,    KC.L, KC.SCLN, KC.QUOT,
        KC.MINS,   KC.Z,    KC.X,    KC.C,  KC.V,  KC.B,                                             KC.N,  KC.M, KC.COMM,  KC.DOT, KC.SLSH,  KC.EQL,
        KC.PAUS, KC.DEL, KC.LEFT, KC.RGHT,                                                                          KC.UP, KC.DOWN, KC.BSPC, KC.PSCR,
                                                         KC.MO(1),  KC.SPC,       KC.ENT, KC.MO(2),
                                                          KC.LSFT, KC.LCTL,      KC.RCTL,  KC.RSFT,
                                                          KC.LALT, KC.LGUI,      KC.RGUI,  KC.RALT
    ],
    [  #1
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                       KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.VOLU, KC.PGUP, KC.TRNS,                       KC.TRNS, KC.NLCK,   KC.P7,   KC.P8,   KC.P9, KC.PMNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.MPLY, KC.MUTE, KC.TRNS, KC.SLCK,                        KC.INS, KC.PAST,   KC.P4,   KC.P5,   KC.P6, KC.PPLS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.VOLD, KC.PGDN,                                         KC.PSLS,   KC.P1,   KC.P2,   KC.P3, KC.PENT, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.BRUD, KC.BRIU,                                                                      KC.P0, KC.PDOT, KC.TRNS, KC.TRNS,
                                                              KC.TRNS, KC.TRNS,     KC.TRNS,   KC.NO,
                                                              KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS,
                                                              KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS
    ],
    [  #2
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS,                      KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.F13,   KC.F14,  KC.F15,  KC.F16,   KC.F17,  KC.F18, KC.TRNS,                      KC.TRNS,  KC.F19,  KC.F20,  KC.F21,  KC.F22,  KC.F23,  KC.F24,
        KC.F1,     KC.F2,   KC.F3,   KC.F4,    KC.F5,   KC.F6, KC.TRNS,                      KC.TRNS,   KC.F7,   KC.F8,   KC.F9,  KC.F10,  KC.F11,  KC.F12,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.RESET, KC.TRNS,                                        KC.TRNS,  KC.RLD, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                                                                             KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
                                                                 KC.NO, KC.TRNS,    KC.TRNS, KC.TRNS,
                                                               KC.TRNS, KC.TRNS,    KC.TRNS, KC.TRNS,
                                                               KC.TRNS, KC.TRNS,    KC.TRNS, KC.TRNS
    ]
]
# fmt:on

if __name__ == '__main__':
    keyboard.go()
