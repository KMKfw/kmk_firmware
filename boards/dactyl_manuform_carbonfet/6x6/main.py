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

M_DEL = KC.HT(KC.DEL, KC.MEH)
H_BSPC = KC.HT(KC.BSPC, KC.HYPR)
A_TAB = KC.HT(KC.TAB, KC.LALT)
ALTCTL = KC.LALT(KC.LCTL)
SFTGUI = KC.LSFT(KC.LGUI)

# fmt:off
keyboard.keymap = [
    [   # 0
        KC.F1,   KC.F2,   KC.F3,   KC.F4, KC.F5,   KC.F6,                                         KC.F7, KC.F8,   KC.F9,  KC.F10,  KC.F11,  KC.F12,
        KC.ESC,  KC.N1,   KC.N2,   KC.N3, KC.N4,   KC.N5,                                         KC.N6, KC.N7,   KC.N8,   KC.N9,   KC.N0,  KC.GRV,
        KC.CAPS,  KC.Q,    KC.W,    KC.E,  KC.R,    KC.T,                                          KC.Y,  KC.U,    KC.I,    KC.O,    KC.P, KC.BSLS,
        KC.LSFT,  KC.A,    KC.S,    KC.D,  KC.F,    KC.G,                                          KC.H,  KC.J,    KC.K,    KC.L, KC.SCLN, KC.RSFT,
        KC.LCTL,  KC.Z,    KC.X,    KC.C,  KC.V,    KC.B,                                          KC.N,  KC.M, KC.COMM,  KC.DOT, KC.SLSH, KC.RCTL,
                        KC.LEFT, KC.RGHT,       KC.MO(1), KC.SPC, KC.LALT,      KC.LALT, KC.ENT, KC.MO(2),        KC.UP, KC.DOWN,
                                                 KC.HOME,  M_DEL, KC.LGUI,       KC.RGUI, H_BSPC, KC.END,
    ],
    [  #1
        KC.F13,   KC.F14,  KC.F15,  KC.F16,     KC.F17,     KC.F18,                                       KC.F19,  KC.F20,  KC.F21,  KC.F22,  KC.F23,  KC.F24,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,    KC.TRNS,    KC.TRNS,                                      KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,    KC.TRNS,    KC.TRNS,                                      KC.NLCK,   KC.P7,   KC.P8,   KC.P9, KC.PMNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.UNDS, KC.MINS, KC.KC.LBRC, KC.KC.RBRC,                                      KC.PAST,   KC.P4,   KC.P5,   KC.P6, KC.PPLS, KC.TRNS,
        KC.TRNS, KC.TRNS,  KC.EQL, KC.PLUS, KC.KC.LCBR, KC.KC.RCBR,                                      KC.PSLS,   KC.P1,   KC.P2,   KC.P3, KC.PENT, KC.TRNS,
                          KC.TRNS, KC.TRNS,                KC.TRNS, KC.NO, KC.NO,      KC.LALT, KC.RSFT,  SFTGUI,            KC.P0, KC.PDOT,
                                                             KC.NO, KC.NO, KC.NO,      KC.RGUI, KC.RCTL,  ALTCTL,
    ],
    [  #2
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                                      KC.TRNS,  KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                                      KC.TRNS,  KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.PGUP,  KC.INS,                                      KC.TRNS,  KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.PSCR,                                      KC.TRNS, KC.RESET, KC.NO,    KC.TRNS,  KC.RLD, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.PGDN, KC.PAUS,                                      KC.TRNS,  KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
                          KC.TRNS, KC.TRNS,           SFTGUI, KC.LSFT, KC.LALT,      KC.NO, KC.NO, KC.TRNS,            KC.TRNS, KC.SLCK,
                                                      ALTCTL, KC.LCTL, KC.LGUI,      KC.NO, KC.NO,   KC.NO,
    ],
]
# fmt:on
