from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.split import Split

keyboard = KMKKeyboard()

keyboard.modules.append(Layers())
keyboard.modules.append(HoldTap())

split = Split(
    data_pin=keyboard.data_pin,
    # data_pin2=,
)
keyboard.modules.append(split)

A_D = KC.HT(KC.D, KC.LALT)
C_F = KC.HT(KC.F, KC.LCTL)
S_SPC = KC.HT(KC.SPC, KC.LSFT)
S_ENT = KC.HT(KC.ENT, KC.RSFT)
C_J = KC.HT(KC.J, KC.RCTL)
A_K = KC.HT(KC.L, KC.LALT)
M_HOME = KC.HT(KC.HOME, KC.MEH)
H_END = KC.HT(KC.END, KC.HYPR)
ALTCTL = KC.LALT(KC.LCTL)

# fmt:off
keyboard.keymap = [
    [   # 0
        KC.GRV,  KC.Q,    KC.W,    KC.E, KC.R,   KC.T,                                         KC.Y, KC.U,    KC.I,    KC.O,    KC.P, KC.BSLS,
        KC.CAPS, KC.A,    KC.S,     A_D,  C_F,   KC.G,                                         KC.H,  C_J,     A_K,    KC.L, KC.SCLN, KC.QUOT,
        KC.LBRC, KC.Z,    KC.X,    KC.C, KC.V,   KC.B,                                         KC.N, KC.M, KC.COMM,  KC.DOT, KC.SLSH, KC.RBRC,
                       KC.LEFT, KC.RGHT,       KC.MO(1), S_SPC,  KC.DEL,       KC.BSPC, S_ENT, KC.MO(2),         KC.UP, KC.DOWN,
                                                KC.ESC,  M_HOME, KC.LGUI,      KC.RGUI, H_END, KC.TAB,
    ],
    [  #1
        KC.TRNS, KC.F1,   KC.F2,   KC.F3,  KC.F4,  KC.INS,                                      KC.NLCK, KC.P7, KC.P8,   KC.P9, KC.PMNS, KC.TRNS,
        KC.TRNS, KC.F5,   KC.F6,   KC.F7,  KC.F8, KC.PSCR,                                      KC.PAST, KC.P4, KC.P5,   KC.P6, KC.PPLS, KC.TRNS,
        KC.TRNS, KC.F9,  KC.F10,  KC.F11, KC.F12, KC.PAUS,                                      KC.PSLS, KC.P1, KC.P2,   KC.P3, KC.PENT, KC.TRNS,
                        KC.TRNS, KC.TRNS,         KC.TRNS, KC.NO, KC.NO,      KC.LALT, KC.RSFT, KC.MO(3),       KC.P0, KC.PDOT,
                                                    KC.NO, KC.NO, KC.NO,      KC.RGUI, KC.RCTL, ALTCTL,
    ],
    [  #2
        KC.TRNS, KC.EXLM,   KC.AT, KC.HASH,  KC.DLR,  KC.PERC,                                      KC.CIRC, KC.AMPR, KC.ASTR, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS,   KC.N1,   KC.N2,   KC.N3,   KC.N4,    KC.N5,                                        KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0, KC.TRNS,
        KC.TRNS, KC.MINS, KC.PLUS, KC.LPRN, KC.LCBR,  KC.TRNS,                                      KC.TRNS, KC.RCBR, KC.RPRN, KC.UNDS,  KC.EQL, KC.TRNS,
                          KC.PGDN, KC.PGUP,          KC.MO(3), KC.LSFT, KC.LALT,      KC.NO, KC.NO, KC.TRNS,          KC.TRNS, KC.SLCK,
                                                       ALTCTL, KC.LCTL, KC.LGUI,      KC.NO, KC.NO,
    ],
    [  #3
        KC.NO, KC.NO,    KC.NO, KC.NO,    KC.NO,   KC.NO,                                  KC.NO,  KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,
        KC.NO, KC.NO,    KC.NO, KC.NO, KC.RESET,   KC.NO,                                  KC.NO, KC.RLD, KC.NO, KC.NO, KC.NO, KC.NO,
        KC.NO, KC.NO,    KC.NO, KC.NO,    KC.NO,   KC.NO,                                  KC.NO,  KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,
                         KC.NO, KC.NO,           KC.TRNS, KC.NO, KC.NO,    KC.NO, KC.NO, KC.TRNS,         KC.NO, KC.NO,
                                                   KC.NO, KC.NO, KC.NO,    KC.NO, KC.NO, KC.NO,
    ],
]
# fmt:on
