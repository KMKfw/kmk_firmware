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
ALTCTL = KC.LALT(KC.LCTL)
SFTGUI = KC.LSFT(KC.LGUI)

# fmt:off
keyboard.keymap = [
    [   # 0
        KC.ESC,    KC.N1,   KC.N2,   KC.N3, KC.N4,    KC.N5, KC.PSCR,                        KC.INS,    KC.N6, KC.N7,   KC.N8,   KC.N9,   KC.N0,  KC.GRV,
        KC.TAB,     KC.Q,    KC.W,    KC.E,  KC.R,     KC.T, KC.MINS,                        KC.EQL,     KC.Y,  KC.U,    KC.I,    KC.O,    KC.P, KC.BSLS,
        KC.CAPS,    KC.A,    KC.S,    KC.D,  KC.F,     KC.G, KC.LBRC,                       KC.RBRC,     KC.H,  KC.J,    KC.K,    KC.L, KC.SCLN, KC.QUOT,
        KC.LSFT,    KC.Z,    KC.X,    KC.C,  KC.V,     KC.B,                                             KC.N,  KC.M, KC.COMM,  KC.DOT, KC.SLSH, KC.RSFT,
        KC.LCTL, KC.LGUI, KC.LEFT, KC.RGHT,        KC.MO(1),  KC.SPC,  KC.DEL,      KC.BSPC, KC.ENT, KC.MO(2),          KC.UP, KC.DOWN, KC.RGUI, KC.RCTL,
                                                    KC.LALT, KC.HOME, KC.PGUP,      KC.PGDN, KC.END,  KC.RALT,
    ],
    [  #1
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                      KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                      KC.TRNS, KC.NLCK,   KC.P7,   KC.P8,   KC.P9, KC.PMNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                      KC.TRNS, KC.PAST,   KC.P4,   KC.P5,   KC.P6, KC.PPLS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                                        KC.PSLS,   KC.P1,   KC.P2,   KC.P3, KC.PENT, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,          KC.TRNS,   KC.NO, KC.NO,      KC.LALT, KC.RSFT,  SFTGUI,            KC.P0, KC.PDOT, KC.TRNS, KC.TRNS,
                                                       KC.NO,   KC.NO, KC.NO,      KC.RGUI, KC.RCTL,  ALTCTL,
    ],
    [  #2
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                      KC.TRNS, KC.TRNS,  KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS,   KC.F1,   KC.F2,   KC.F3,   KC.F4, KC.TRNS, KC.TRNS,                      KC.TRNS, KC.TRNS,  KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS,   KC.F1,   KC.F2,   KC.F3,   KC.F4, KC.PAUS, KC.TRNS,                      KC.TRNS, KC.TRNS, KC.RESET, KC.NO,    KC.TRNS,  KC.RLD, KC.TRNS,
        KC.TRNS,   KC.F9,  KC.F10,  KC.F11,  KC.F12, KC.TRNS,                                        KC.TRNS,  KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
                          KC.TRNS, KC.TRNS,           SFTGUI, KC.LSFT, KC.LALT,      KC.NO,   KC.NO, KC.TRNS,            KC.TRNS, KC.SLCK,
                                                      ALTCTL, KC.LCTL, KC.LGUI,      KC.NO,   KC.NO,   KC.NO,
    ],
]
# fmt:on
