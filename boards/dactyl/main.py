from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide, SplitType

keyboard = KMKKeyboard()

layers_ext = Layers()
keyboard.modules.append(layers_ext)

split = Split(
    data_pin=keyboard.data_pin
    #data_pin2=keyboard.data_pin2
)
keyboard.modules.append(split)

modtap = ModTap()
keyboard.modules.append(modtap)

LT.1SPC = KC.LT(1, KC.SPC)
LT.2ENT = KC.LT(2. KC.ENT)
MT.SBSP = MT.KC(KC.BSPC, KC.LSFT)
MT.CDEL = MT.KC(KC.DEL, KC.LCTL)
MT.MEND = MT.KC(KC.END, KC.MEH)
MT.HPGD = MT.KC(KC.PGDN, KC.HYPER)

keyboard.keymap = [
    [   #0
        KC.ESC,    KC.N1,  KC.N2,   KC.N3,   KC.N4, KC.N5,                                          KC.N6, KC.N7,   KC.N8,   KC.N9,   KC.N0,  KC.GRV,
        KC.TAB,     KC.Q,   KC.W,    KC.E,    KC.R,  KC.T,                                           KC.Y,  KC.U,    KC.I,    KC.O,    KC.P, KC.BSLS,
        KC.CAPS,    KC.A,   KC.S,    KC.D,    KC.F,  KC.G,                                           KC.H,  KC.J,    KC.K,    KC.L, KC.SCLN, KC.QUOT,
        KC.LSFT,    KC.Z,   KC.X,    KC.C,    KC.V,  KC.B,                                           KC.N,  KC.M, KC.COMM,  KC.DOT, KC.SLSH, KC.RSFT,
        KC.LCTL, KC_MINS, KC_EQL, KC_LEFT, KC_RGHT,                                                        KC_UP, KC_DOWN, KC_LBRC, KC_RBRC, KC.RCTL,
                                                           KC.LALT, KC.LGUI,    KC.RGUI, KC.RALT,
                                                                    KC.HOME,    KC.PGUP,  
                                                  LT.1SPC, MT.SBSP, MT.MEND,    MT.HPGD, MT.CDEL, LT.2ENT
    ],
    [   #1
        KC.F1,     KC.F2,  KC.F3,   KC.F4,   KC.F5, KC.F6,                                      KC.F7,   KC.F8, KC.F9,  KC.F10,  KC.F11,  KC.F12,
        KC.NO,     KC.NO,  KC.NO,   KC.NO,   KC.NO, KC.NO,                                      KC.NO,   KC.P7, KC.P8,   KC.P9, KC.PMNS,   KC.NO,
        KC.NLCK, KC.SLCK, KC.INS, KC.PAUS, KC.PSCR, KC.NO,                                    KC.PAST,   KC.P4, KC.P5,   KC.P6, KC.PPLS,   KC.NO,
        KC.TRNS,   KC.NO,  KC.NO,   KC.NO,   KC.NO, KC.NO,                                    KC.PSLS,   KC.P1, KC.P2,   KC.P3, KC.PEQL, KC.TRNS,
        KC.TRNS,   KC.NO,  KC.NO,   KC.NO,   KC.NO,                                                    KC.PCMM, KC.P0, KC.PDOT,   KC.NO, KC.TRNS,
                                                           KC.NO, KC.NO,    KC.TRNS, KC.TRNS,
                                                                  KC.NO,    KC.TRNS,
                                                  KC.TRNS, KC.NO, KC.NO,    KC.TRNS, KC.TRNS, KC.PENT   
    ],
    [   #2
        KC.F13,   KC.14, KC.15, KC.16,   KC.17, KC.18,                                       KC.19,     KC.20,   KC.21, KC.22, KC.23,     KC.24,
        KC.NO,    KC.NO, KC.NO, KC.NO, KC.VOLU, KC.NO,                                       KC.NO,     KC.NO,   KC.NO, KC.NO, KC.NO,     KC.NO,
        KC.RESET, KC.NO, KC.NO, KC.NO, KC.MUTE, KC.NO,                                       KC.NO, KC.BT_NXT, KC.BRIU, KC.NO, KC.NO,  KC.DEBUG,
        KC.NO,    KC.NO, KC.NO, KC.NO, KC.VOLD, KC.NO,                                       KC.NO, KC.BT_PRV, KC.BRID, KC.NO, KC.NO,     KC.NO,
        KC.RLD,   KC.NO, KC.NO, KC.NO,   KC.NO,                                                         KC.NO,   KC.NO, KC.NO, KC.NO, KC.BT_CLR,
                                                        KC.TRNS, KC.TRNS,    KC.NO, KC.NO,
                                                                 KC.TRNS,    KC.NO,
                                               KC.MPLY, KC.TRNS, KC.TRNS,    KC.NO, KC.NO, KC.TRNS
    ]
]

if __name__ == '__main__':
    keyboard.go()
