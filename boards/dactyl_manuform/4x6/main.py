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
    [   # BASE
        KC.ESC,    KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                                               KC.Y,    KC.U,    KC.I,    KC.O,    KC.P, KC.BSLS,
        KC.TAB,    KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                                               KC.H,    KC.J,    KC.K,    KC.L, KC.SCLN, KC.QUOT,
        KC.LSFT,   KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,                                               KC.N,    KC.M, KC.COMM,  KC.DOT, KC.SLSH, KC.RSFT,
                         KC.LEFT, KC.RGHT,                                                                                  KC.UP, KC.DOWN,
                                                   KC.MO(1),  KC.SPC,                          KC.ENT, KC.MO(2),
                                                             KC.HOME, KC.BSPC,        KC.DEL,  KC.END,
                                                             KC.LCTL, KC.LGUI,       KC.LALT, KC.RCTL
    ],
    [  #NP_FN
        KC.VOLU,  KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.INS,                                        KC.TRNS,  KC.P7,  KC.P8,   KC.P9,  KC.PMNS,  KC.TRNS,
        KC.MUTE,  KC.F5,   KC.F6,   KC.F7,   KC.F8,  KC.PSCR,                                        KC.PAST,  KC.P4,  KC.P5,   KC.P6,  KC.PPLS,  KC.NLCK,
        KC.VOLD,  KC.F9,  KC.F10,  KC.F11,  KC.F12,  KC.PAUS,                                        KC.PSLS,  KC.P1,  KC.P2,   KC.P3,  KC.PENT,  KC.TRNS,
                         KC.BRID, KC.BRIU,                                                                             KC.P0, KC.PDOT,
                                                     KC.TRNS, KC.NO,                        KC.LGUI, KC.LCTL,
                                                              KC.NO, KC.NO,        KC.TRNS, KC.TRNS,
                                                              KC.NO, KC.NO,       KC.RESET,  KC.RLD
    ],
    [  #NUM_SYM
        KC.TRNS, KC.EXLM,   KC.AT, KC.HASH,  KC.DLR, KC.PERC,                                           KC.CIRC, KC.AMPR, KC.ASTR,  KC.GRV, KC.TILD, KC.TRNS,
        KC.TRNS,   KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                                             KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0, KC.TRNS,
        KC.TRNS, KC.MINS, KC.PLUS, KC.LBRC, KC.LPRN, KC.LCBR,                                           KC.RCBR, KC.RPRN, KC.RBRC, KC.UNDS,  KC.EQL, KC.TRNS,
                          KC.PGDN, KC.PGUP,                                                                               KC.TRNS, KC.SLCK,
                                                      KC.RCTL,   KC.LALT,                        KC.NO, KC.TRNS,
                                                               KC.BT_PRV, KC.BT_NXT,      KC.NO, KC.NO,
                                                               KC.BT_CLR,   KC.TRNS,      KC.NO, KC.NO
    ]
]

if __name__ == '__main__':
    keyboard.go()
    