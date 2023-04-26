from kb import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.tapdance import TapDance

keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys())
keyboard.modules.append(HoldTap())
keyboard.modules.append(Layers())
keyboard.modules.append(TapDance())

LS_Z = KC.HT(KC.Z, KC.LSFT)
RS_SLSH = KC.HT(KC.SLSH, KC.RSFT)
TD_ESC_CTL_SL_EMO = KC.TD(
    KC.MT(KC.ESC, KC.LCTL, prefer_hold=False),
    KC.LGUI(KC.SPC),
    KC.LCTL(KC.LGUI(KC.SPC))
)
LG_SPC = KC.HT(KC.SPC, KC.LGUI)
LY1_TAB = KC.MO(1, KC.TAB)
LY2_ENT = KC.MO(2, KC.ENT)
LS_LBRC = KC.HT(KC.LBRC, KC.LSFT)
RS_BSLS = KC.HT(KC.BSLS, KC.RSFT)
RS_SLSH = KC.HY(KC.SLSH, KC.RSFT)
LY5_TAB = KC.MO(5, KC.TAB)
LY6_ENT = KC.MO(6, KC.ENT)
TD_ESC_A_G_EMO = KC.TD(
    KC.MT(KC.ESC, KC.LALT, prefer_hold=False),
    KC.LGUI,
    KC.LGUI(KC.DOT)
)
keyboard.keymap = [
    [
        KC.Q, KC.W, KC.F,              KC.P,    KC.G,   KC.J,    KC.L,    KC.U,              KC.Y,   KC.BSPC,
        KC.A, KC.R, KC.S,              KC.T,    KC.D,   KC.H,    KC.N,    KC.E,              KC.I,   KC.O,
        LS_Z, KC.X, KC.C,              KC.V,    KC.B,   KC.K,    KC.M,    KC.COMM,           KC.DOT, RS_SLSH,
                    TD_ESC_CTL_SL_EMO, KC.LALT, LG_SPC, LY1_TAB, LY2_ENT, TD_ESC_CTL_SL_EMO
    ],
    [
        KC.UNDS, KC.MINS, KC.PLUS, KC.EQL,  KC.COLN, KC.GRV,  KC.MRWD, KC.MPLY, KC.MFFD, KC.DEL,
        KC.LCBR, KC.LPRN, KC.RPRN, KC.RCBR, KC.PIPE, KC.ESC,  KC.LEFT, KC.UP,   KC.DOWN, KC.RGHT,
        LS_LBRC, KC.QUOT, KC.DQUO, KC.RBRC, KC.SCLN, KC.TILD, KC.VOLD, KC.MUTE, KC.VOLU, RS_BSLS,
                          KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
    ],
    [
        KC.EXLM, KC.AT, KC.HASH, KC.DLR,  KC.PERC,  KC.CIRC, KC.AMPR, KC.ASTR, KC.CAPS, KC.BSPC,
        KC.N1,   KC.N2, KC.N3,   KC.N4,   KC.N5,    KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,
        KC.LSFT, KC.NO, KC.NO,   KC.NO,   KC.MO(3), KC.NO,   KC.NO,   KC.COMM, KC.DOT,  RS_SLSH,
                        KC.TRNS, KC.TRNS, KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS
    ],
    [
        KC.NO,  KC.NO, KC.NO,   KC.NO,    KC.NO,   KC.NO,   KC.NO,   KC.NO,  KC.NO, KC.TO(4),
        KC.F1,  KC.F2, KC.F3,   KC.F4,    KC.F5,   KC.F6,   KC.F7,   KC.F8,  KC.F9, KC.F10,
        KC.F11, KC.NO, KC.NO,   KC.RESET, KC.TRNS, KC.NO,   KC.NO,   KC.NO,  KC.NO, KC.F12,
                       KC.TRNS, KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
    ],
    [
        KC.Q, KC.W, KC.F,           KC.P,    KC.G,   KC.J,    KC.L,    KC.U,           KC.Y,   KC.BSPC,
        KC.A, KC.R, KC.S,           KC.T,    KC.D,   KC.H,    KC.N,    KC.E,           KC.I,   KC.O,
        LS_Z, KC.X, KC.C,           KC.V,    KC.B,   KC.K,    KC.M,    KC.COMM,        KC.DOT, RS_SLSH,
                    TD_ESC_A_G_EMO, KC.LCTL, KC.SPC, LY5_TAB, LY6_ENT, TD_ESC_A_G_EMO
    ],
    [
        KC.UNDS, KC.MINS, KC.PLUS, KC.EQL,  KC.COLN, KC.GRV,  KC.MRWD, KC.MPLY, KC.MFFD, KC.DEL,
        KC.LCBR, KC.LPRN, KC.RPRN, KC.RCBR, KC.PIPE, KC.ESC,  KC.LEFT, KC.UP,   KC.DOWN, KC.RGHT,
        LS_LBRC, KC.QUOT, KC.DQUO, KC.RBRC, KC.SCLN, KC.TILD, KC.VOLD, KC.MUTE, KC.VOLU, RS_BSLS,
                          KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
    ],
    [
        KC.EXLM, KC.AT, KC.HASH, KC.DLR,  KC.PERC,  KC.CIRC, KC.AMPR, KC.ASTR, KC.CAPS, KC.BSPC,
        KC.N1,   KC.N2, KC.N3,   KC.N4,   KC.N5,    KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,
        KC.LSFT, KC.NO, KC.NO,   KC.NO,   KC.MO(7), KC.NO,   KC.NO,   KC.COMM, KC.DOT,  RS_SLSH,
                        KC.TRNS, KC.TRNS, KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS
    ],
    [
        KC.NO,  KC.NO, KC.NO,   KC.NO,    KC.NO,   KC.NO,   KC.NO,   KC.NO,  KC.NO, KC.TO(0),
        KC.F1,  KC.F2, KC.F3,   KC.F4,    KC.F5,   KC.F6,   KC.F7,   KC.F8,  KC.F9, KC.F10,
        KC.F11, KC.NO, KC.NO,   KC.RESET, KC.TRNS, KC.NO,   KC.NO,   KC.NO,  KC.NO, KC.F12,
                       KC.TRNS, KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
    ]
]
