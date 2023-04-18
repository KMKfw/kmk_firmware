from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.extensions.media_keys import MediaKeys

keyboard = KMKKeyboard()

layers_ext = Layers()
keyboard.modules.append(layers_ext)

split = Split(
    data_pin=keyboard.data_pin
    #data_pin2=keyboard.data_pin2
)
keyboard.modules.append(split)

keyboard.extensions.append(MediaKeys())


keyboard.keymap = [
    [   #0
        KC.ESC,  KC.N1,   KC.N2,   KC.N3, KC.N4, KC.N5,                             KC.N6, KC.N7,   KC.N8,  KC.N9,   KC.N0,  KC.GRV,
        KC.TAB,   KC.Q,    KC.W,    KC.E,  KC.R,  KC.T,                              KC.Y,  KC.U,    KC.I,   KC.O,    KC.P, KC.BSLS,
        KC.LSFT,  KC.A,    KC.S,    KC.D,  KC.F,  KC.G,                              KC.H,  KC.J,    KC.K,   KC.L, KC.SCLN, KC.RSFT,
        KC.LCTL,  KC.Z,    KC.X,    KC.C,  KC.V,  KC.B,                              KC.N,  KC.M, KC.COMM, KC.DOT, KC.SLSH, KC.RCTL,
                        KC.LEFT, KC.RGHT,                                                           KC.UP, KC.DOWN,
                                              KC.MO(1),  KC.SPC,         KC.ENT, KC.MO(2),
                                               KC.LALT,  KC.DEL,        KC.BSPC,  KC.LALT,
                                               KC.HOME, KC.LGUI,        KC.RGUI,  KC.END  
    ],
    [  #1
        KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5, KC.F6,                           KC.F7, KC.F8, KC.F9,  KC.F10,  KC.F11,  KC.F12,
        KC.TRNS, KC.NO, KC.VOLU, KC.PGUP,   KC.NO, KC.NO,                         KC.NLCK, KC.P7, KC.P8,   KC.P9, KC.PMNS,   KC.NO,
        KC.TRNS, KC.NO, KC.MUTE, KC.SLCK, KC.MPLY, KC.NO,                         KC.PAST, KC.P4, KC.P5,   KC.P6, KC.PPLS, KC.TRNS,
        KC.TRNS, KC.NO, KC.VOLD, KC.PGDN,   KC.NO, KC.NO,                         KC.PSLS, KC.P1,  C.P2,   KC.P3, KC.PENT, KC.TRNS,
                          KC.NO,   KC.NO,                                                         KC.P0, KC.PDOT,
                                                 KC.TRNS, KC.TRNS,       KC.TRNS,   KC.NO,
                                                 KC.TRNS, KC.TRNS,       KC.TRNS, KC.TRNS,
                                                 KC.TRNS, KC.TRNS,       KC.TRNS, KC.TRNS
    ],
    [  #2
        KC.F13,  KC.F14,   KC.F15,  KC.F16,  KC.F17, KC.F18,                         KC.F19,    KC.20, KC.21,   KC.22,   KC.23,   KC.24,
        KC.TRNS, KC.NO,     KC.NO,   KC.NO,   KC.NO,  KC.NO,                          KC.NO,    KC.NO, KC.NO,   KC.NO,   KC.NO,   KC.NO,
        KC.TRNS, KC.MINS, KC.PLUS, KC.LBRC, KC.RBRC,  KC.NO,                          KC.NO, KC.RESET, KC.NO,   KC.NO,  KC.RLD, KC.TRNS,
        KC.TRNS, KC.EQL,  KC.UNDS, KC.LCBR, KC.RCBR,  KC.NO,                          KC.NO,    KC.NO, KC.NO,   KC.NO,   KC.NO, KC.TRNS,
                            KC.NO,   KC.NO,                                                                   KC.BRID, KC.BRIU,
                                                      KC.NO, KC.TRNS,      KC.TRNS, KC.TRNS,
                                                    KC.TRNS, KC.TRNS,      KC.TRNS, KC.TRNS,
                                                    KC.TRNS, KC.TRNS,      KC.TRNS, KC.TRNS
    ]
]

if __name__ == '__main__':
    keyboard.go()
    