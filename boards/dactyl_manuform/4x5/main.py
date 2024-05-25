from kb import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.split import Split

keyboard = KMKKeyboard()

keyboard.extensions.append(MediaKeys())
keyboard.modules.append(Layers())
keyboard.modules.append(HoldTap())

split = Split(
    data_pin=keyboard.data_pin,
    # data_pin2=keyboard.data_pin2,
)
keyboard.modules.append(split)

L1_ESC = KC.LT(1, KC.ESC)
L2_TAB = KC.LT(2, KC.TAB)
S_SPC = KC.HT(KC.SPC, KC.LSFT)
S_ENT = KC.HT(KC.ENT, KC.RSFT)
C_HOME = KC.HT(KC.HOME, KC.LCTL)
C_END = KC.HT(KC.END, KC.RCTL)
A_BSPC = KC.HT(KC.BSPC, KC.LALT)
A_DEL = KC.HT(KC.DEL, KC.LALT)
G_LBRC = KC.HT(KC.LBRC, KC.LGUI)
G_RBRC = KC.HT(KC.RBRC, KC.RGUI)

# fmt:off
keyboard.keymap = [
    [   #0
        KC.Q,    KC.W,    KC.E, KC.R,   KC.T,                                        KC.Y, KC.U,    KC.I,    KC.O,    KC.P,
        KC.A,    KC.S,    KC.D, KC.F,   KC.G,                                        KC.H, KC.J,    KC.K,    KC.L, KC.SCLN,
        KC.Z,    KC.X,    KC.C, KC.V,   KC.B,                                        KC.N, KC.M, KC.COMM,  KC.DOT, KC.QUOT,
              KC.LEFT, KC.RGHT,                                                                    KC.UP, KC.DOWN,
                                      L1_ESC, S_SPC,                        S_ENT, L2_TAB,
                                             C_HOME,  A_DEL,      A_BSPC,   C_END,
                                            KC.BSLS, G_LBRC,      G_RBRC, KC.SLSH
    ],
    [  #1
        KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.INS,                                        KC.NLCK,  KC.P7,  KC.P8,   KC.P9,  KC.PMNS,
        KC.F5,   KC.F6,   KC.F7,   KC.F8,  KC.PSCR,                                        KC.PAST,  KC.P4,  KC.P5,   KC.P6,  KC.PPLS,
        KC.F9,  KC.F10,  KC.F11,  KC.F12,  KC.PAUS,                                        KC.PSLS,  KC.P1,  KC.P2,   KC.P3,  KC.PENT,
               KC.BRID, KC.BRIU,                                                                             KC.P0, KC.PDOT,
                                           KC.TRNS, KC.TRNS,                        KC.TRNS, KC.MO(3),
                                                    KC.TRNS, KC.TRNS,      KC.TRNS, KC.TRNS,
                                                    KC.TRNS, KC.TRNS,      KC.TRNS, KC.TRNS
    ],
    [  #2
        KC.EXLM,   KC.AT, KC.HASH,  KC.DLR, KC.PERC,                                           KC.CIRC, KC.AMPR, KC.ASTR,  KC.GRV, KC.TILD,
        KC.N1,     KC.N2,   KC.N3,   KC.N4,   KC.N5,                                             KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,
        KC.TRNS, KC.MINS, KC.PLUS, KC.LPRN, KC.TRNS,                                           KC.TRNS, KC.RPRN, KC.UNDS,  KC.EQL, KC.TRNS,
                 KC.PGDN, KC.PGUP,                                                                               KC.TRNS, KC.SLCK,
                                            KC.MO(3), KC.TRNS,                        KC.TRNS, KC.TRNS,
                                                      KC.TRNS, KC.TRNS,      KC.TRNS, KC.TRNS,
                                                      KC.TRNS, KC.TRNS,      KC.TRNS, KC.TRNS
    ],
    [  #3
        KC.NO,   KC.NO,    KC.NO,   KC.NO, KC.NO,                                    KC.NO,   KC.NO,   KC.NO,   KC.NO, KC.NO,
        KC.NO, KC.BRID,  KC.BRIU, KC.MPLY, KC.NO,                                    KC.NO, KC.MUTE, KC.VOLU, KC.VOLD, KC.NO,
        KC.NO,   KC.NO,    KC.NO,   KC.NO, KC.NO,                                    KC.NO,   KC.NO,   KC.NO,   KC.NO, KC.NO,
                 KC.NO, KC.RESET,                                                                     KC.RLD,   KC.NO,
                                         KC.TRNS, KC.NO,                    KC.NO, KC.TRNS,
                                                  KC.NO, KC.NO,      KC.NO, KC.NO,
                                                  KC.NO, KC.NO,      KC.NO, KC.NO
    ]
]
# fmt:on

if __name__ == '__main__':
    keyboard.go()
