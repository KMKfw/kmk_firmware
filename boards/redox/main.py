from kb import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.split import Split

keyboard = KMKKeyboard()

keyboard.extensions.append(MediaKeys())
keyboard.modules.append(HoldTap())
keyboard.modules.append(Layers())
keyboard.modules.append(MouseKeys())

split = Split(
    data_pin=keyboard.data_pin
    # data_pin2=keyboard.data_pin2
)
keyboard.modules.append(split)

LT_GRV = KC.LT(2, KC.GRV)
LT_MINS = KC.LT(2, KC.MINS)
LT_PGUP = KC.LT(3, KC.PGUP)
LT_END = KC.LT(3, KC.END)
LA_PAST = KC.HT(KC.PAST, KC.LALT)
LC_BSLS = KC.HT(KC.BSLS, KC.LCTL)

# fmt:off
keyboard.keymap = [
    [   # QWERTY
        LT_GRV,  KC.N1,   KC.N2,   KC.N3,   KC.N4, KC.N5,                                       KC.N6, KC.N7, KC.N8,   KC.N9,   KC.N0,   LT_MINS,
        KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,  KC.T, KC.MO(1),                     KC.MO(1), KC.Y,  KC.U, KC.I,    KC.O,    KC.P,    KC.EQL,
        KC.ESC,  KC.A,    KC.S,    KC.D,    KC.F,  KC.G, KC.LBRC,                       KC.RBRC, KC.H,  KC.J, KC.K,    KC.L,    KC.SCLN, KC.QUOT,
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,  KC.B, LT_PGUP, KC.PGDN,    KC.HOME,   LT_END, KC.N,  KC.M, KC.COMM, KC.DOT,  KC.SLSH, KC.RSFT,
        KC.LGUI, KC.PPLS, KC.PMNS, LA_PAST,   LC_BSLS,   KC.BSPC, KC.DEL,      KC.ENT,   KC.SPC,   KC.RALT,   KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT,
    ],
    [   # SYMB
        KC.TRNS, KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,                                            KC.F6, KC.F7, KC.F8, KC.F9,   KC.F10,  KC.NO,
        KC.TRNS, KC.EXLM, KC.AT,   KC.LCBR, KC.RCBR, KC.PIPE, KC.TRNS,                      KC.TRNS, KC.PSLS, KC.P7, KC.P8, KC.P9,   KC.PMNS, KC.NO,
        KC.TRNS, KC.HASH, KC.DLR,  KC.LBRC, KC.RBRC, KC.GRV,  KC.TRNS,                      KC.TRNS, KC.PAST, KC.P4, KC.P5, KC.P6,   KC.PPLS, KC.NO,
        KC.TRNS, KC.PERC, KC.CIRC, KC.LPRN, KC.RPRN, KC.TILD, KC.TRNS, KC.TRNS,    KC.TRNS, KC.TRNS, KC.NO,   KC.P1, KC.P2, KC.P3,   KC.PENT, KC.NO,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,      KC.TRNS,     KC.TRNS, KC.TRNS,    KC.TRNS, KC.TRNS,     KC.RALT,    KC.P0, KC.PDOT, KC.PENT, KC.NO,
    ],
    [   # NAV
        KC.TRNS, KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,                                          KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.NO,   KC.NO,    KC.MS_UP, KC.NO,    KC.MW_UP, KC.NO,   KC.TRNS,                        KC.TRNS, KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,
        KC.NO,   KC.MS_LT, KC.MS_DN, KC.MS_RT, KC.WW_DN, KC.NO,   KC.TRNS,                        KC.TRNS, KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT, KC.NO,   KC.NO,
        KC.NO,   KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.TRNS,  KC.TRNS,     KC.TRNS, KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,
        KC.NO,   KC.NO,    KC.NO,    KC.NO,       KC.MB_LMB,      KC.MB_RMB, KC.TRNS,    KC.TRNS, KC.TRNS,       KC.NO,      KC.NO,   KC.NO,   KC.NO,   KC.NO,

    ],
    [   # ADJUST
        KC.NO, KC.F1,    KC.F2, KC.F3, KC.F4, KC.F5,                                    KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.NO,
        KC.NO, KC.RESET, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,                    KC.NO,   KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,  KC.NO,
        KC.NO, KC.NO,    KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,                    KC.NO,   KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,  KC.NO,
        KC.NO, KC.NO,    KC.NO, KC.NO, KC.NO, KC.NO, KC.TRNS, KC.NO,    KC.NO, KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,  KC.NO,
        KC.NO, KC.NO,    KC.NO, KC.NO,     KC.NO,    KC.NO,   KC.NO,    KC.NO, KC.NO,       KC.NO,    KC.NO, KC.NO, KC.NO,  KC.NO,
    ]
]
# fmt:on

if __name__ == '__main__':
    keyboard.go()
