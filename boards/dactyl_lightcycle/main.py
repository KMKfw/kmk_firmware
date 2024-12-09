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
    # data_pin2=keyboard.data_pin2,
)
keyboard.modules.append(split)

# keymap aliases
H_D = KC.HT(KC.D, KC.HYPR)
M_F = KC.HT(KC.F, KC.MEH)
M_J = KC.HT(KC.J, KC.MEH)
H_K = KC.HT(KC.K, KC.HYPR)
LA_CAPS = KC.HT(KC.CAPS, KC.LALT)
L1_HOME = KC.LT(1, KC.HOME)
L2_END = KC.LT(2, KC.END)
DKT_N = KC.LGUI(KC.TAB)
DKT_P = KC.LSFT(KC.LGUI(KC.TAB))
APP_N = KC.LALT(KC.TAB)
APP_P = KC.LSFT(KC.LALT(KC.TAB))

# fmt: off
keyboard.keymap = [
    [   # 0
        KC.ESC,  KC.Q,    KC.W,   KC.E,    KC.R,    KC.T,                                          KC.Y,   KC.U,  KC.I,    KC.O,    KC.P,    KC.BSLS,
        KC.TAB,  KC.A,    KC.S,   H_D,     M_F,     KC.G,                                          KC.H,   M_J,   H_K,     KC.L,    KC.SCLN, KC.QUOT,
        LA_CAPS, KC.Z,    KC.X,   KC.C,    KC.V,    KC.B,    KC.DEL, KC.LGUI,    KC.RGUI, KC.BSPC, KC.N,   KC.M,  KC.COMM, KC.DOT,  KC.SLSH, KC.LALT,
        KC.LCTL, KC.MINS, KC.EQL, KC.LEFT, KC.RGHT,                                                        KC.UP, KC.DOWN, KC.LBRC, KC.RBRC, KC.RSFT,
                                                    L1_HOME, KC.SPC, KC.LSFT,    KC.RCTL, KC.ENT,  L2_END,
    ],
    [   # 1
        KC.NO,   KC.NO,   KC.NO,  KC.NO,   KC.NO,   KC.NO,                                          KC.NLCK,  KC.P7,   KC.P8, KC.P9,   KC.PMNS, KC.TRNS,
        KC.NO,   KC.NO,   KC.NO,  KC.NO,   KC.NO,   KC.NO,                                          KC.PAST,  KC.P4,   KC.P5, KC.P6,   KC.PPLS, KC.TRNS,
        KC.TRNS, KC.SLCK, KC.INS, KC.PAUS, KC.PSCR, KC.NO,   KC.TRNS, KC.TRNS,    KC.TRNS, KC.TRNS, KC.PSLS,  KC.P1,   KC.P2, KC.P3,   KC.PENT, KC.TRNS,
        KC.TRNS, KC.NO,   KC.NO,  DKT_P,   DKT_N,                                                             KC.PCMM, KC.P0, KC.PDOT, KC.PEQL, KC.TRNS,
                                                    KC.TRNS, KC.TRNS, KC.TRNS,    KC.TRNS, KC.RSFT, KC.MO(3),
    ],
    [   # 2
        KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,  KC.F6,                                           KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,
        KC.GRV,  KC.N1,   KC.N2,   KC.N3,   KC.N4,  KC.N5,                                           KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.TILD,
        KC.TRNS, KC.EXLM, KC.AT,   KC.HASH, KC.DLR, KC.LPRN,  KC.TRNS, KC.TRNS,    KC.TRNS, KC.TRNS, KC.RPRN, KC.PERC, KC.CIRC, KC.AMPR, KC.ASTR, KC.TRNS,
        KC.TRNS, KC.UNDS, KC.PLUS, APP_P,   APP_N,                                                            KC.PGUP, KC.PGDN, KC.LCBR, KC.RCBR, KC.TRNS,
                                                    KC.MO(3), KC.LCTL, KC.TRNS,    KC.TRNS, KC.TRNS, KC.TRNS,
    ],
    [   # 3
        KC.NO, KC.NO,  KC.NO, KC.NO, KC.NO,    KC.NO,                                  KC.NO,   KC.NO, KC.NO, KC.NO, KC.NO,    KC.NO,
        KC.NO, KC.NO,  KC.NO, KC.NO, KC.NO,    KC.NO,                                  KC.NO,   KC.NO, KC.NO, KC.NO, KC.NO,    KC.NO,
        KC.NO, KC.RLD, KC.NO, KC.NO, KC.RESET, KC.NO,   KC.NO, KC.NO,    KC.NO, KC.NO, KC.NO,   KC.NO, KC.NO, KC.NO, KC.NO,    KC.NO,
        KC.NO, KC.NO,  KC.NO, KC.NO, KC.NO,                                                     KC.NO, KC.NO, KC.NO, KC.NO,    KC.NO,
                                               KC.TRNS, KC.NO, KC.NO,    KC.NO, KC.NO, KC.TRNS,
    ],
]
# fmt:on
