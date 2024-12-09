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

G_A = KC.HT(KC.A, KC.LGUI)
H_W = KC.HT(KC.W, KC.HYPR)
A_S = KC.HT(KC.s, KC.LALT)
M_E = KC.HT(KC.E, KC.MEH)
C_D = KC.HT(KC.D, KC.LCTL)
S_F = KC.HT(KC.F, KC.LSFT)
S_J = KC.HT(KC.J, KC.RSFT)
C_K = KC.HT(KC.D, KC.RCTL)
M_I = KC.HT(KC.I, KC.MEH)
A_L = KC.HT(KC.L, KC.LALT)
H_O = KC.HT(KC.O, KC.HYPR)
G_SCLN = KC.HT(KC.SCLN, KC.RGUI)
ALTCTL = KC.LALT(KC.LCTL)

# fmt:off
keyboard.keymap = [
    [   # 0
        KC.Q,     H_W,     M_E, KC.R,     KC.T,                                             KC.Y, KC.U,     M_I,     H_O,    KC.P,
        G_A,      A_S,     C_D,  S_F,     KC.G,                                             KC.H,  S_J,     C_K,     A_L,  G_SCLN,
        KC.Z,    KC.X,    KC.C, KC.V,     KC.B,                                             KC.N, KC.M, KC.COMM,  KC.DOT, KC.SLSH,
              KC.LEFT, KC.RGHT,       KC.MO(1),  KC.SPC,  KC.DEL,      KC.BSPC, KC.ENT, KC.MO(2),         KC.UP, KC.DOWN,
                                        KC.ESC,  KC.HOME, KC.BSLS,     KC.QUOT, KC.END,   KC.TAB,
    ],
    [  #1
        KC.F1,   KC.F2,   KC.F3,  KC.F4,  KC.INS,                                       KC.NLCK,  KC.P7,  KC.P8,   KC.P9,  KC.PMNS,
        KC.F5,   KC.F6,   KC.F7,  KC.F8, KC.PSCR,                                       KC.PAST,  KC.P4,  KC.P5,   KC.P6,  KC.PPLS,
        KC.F9,  KC.F10,  KC.F11, KC.F12, KC.PAUS,                                       KC.PSLS,  KC.P1,  KC.P2,   KC.P3,  KC.PENT,
               KC.CAPS, KC.TRNS,         KC.TRNS, KC.NO, KC.NO,      KC.LALT, KC.RSFT, KC.MO(3),          KC.P0, KC.PDOT,
                                           KC.NO, KC.NO, KC.NO,      KC.RGUI, KC.RCTL,   ALTCTL,
    ],
    [  #2
        KC.EXLM,   KC.AT, KC.HASH,  KC.DLR,  KC.PERC,                                      KC.CIRC, KC.AMPR, KC.ASTR,  KC.GRV, KC.TILD,
        KC.N1,     KC.N2,   KC.N3,   KC.N4,    KC.N5,                                        KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,
        KC.MINS, KC.PLUS, KC.LBRC, KC.LPRN,  KC.LCBR,                                      KC.RCBR, KC.RPRN, KC.RBRC, KC.UNDS,  KC.EQL,
                 KC.PGDN, KC.PGUP,          KC.MO(3), KC.LSFT, KC.LALT,      KC.NO, KC.NO, KC.TRNS,          KC.TRNS, KC.SLCK,
                                              ALTCTL, KC.LCTL, KC.LGUI,      KC.NO, KC.NO,   KC.NO,
    ],
    [  #3
        KC.NO,    KC.NO, KC.NO,    KC.NO,   KC.NO,                                  KC.NO,  KC.NO, KC.NO, KC.NO, KC.NO,
        KC.NO,    KC.NO, KC.NO, KC.RESET,   KC.NO,                                  KC.NO, KC.RLD, KC.NO, KC.NO, KC.NO,
        KC.NO,    KC.NO, KC.NO,    KC.NO,   KC.NO,                                  KC.NO,  KC.NO, KC.NO, KC.NO, KC.NO,
                  KC.NO, KC.NO,           KC.TRNS, KC.NO, KC.NO,    KC.NO, KC.NO, KC.TRNS,         KC.NO, KC.NO,
                                            KC.NO, KC.NO, KC.NO,    KC.NO, KC.NO, KC.NO,
    ],
]
# fmt:on
