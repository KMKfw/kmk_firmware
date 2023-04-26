from kb import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.tapdance import TapDance

keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys())
keyboard.modules = [HoldTap(), Layers(), TapDance()]

LS_Z = KC.HT(KC.Z, KC.LSFT)
RS_SLSH = KC.HT(KC.SLSH, KC.RSFT)
LG_SPC = KC.LGUI(KC.SPC)
LY2_TAB = KC.LT(2, KC.TAB)
LY3_ENT = KC.LT(3, KC.ENT)
TD_ESC_C_SL_EMO = KC.TD(
    KC.HT(KC.ESC, KC.LCTL, prefer_hold=False),
    KC.LGUI(KC.SPC),
    KC.LCTL(KC.LGUI(KC.SPC))
)
LS_LBRC = KC.HT(KC.LBRC, KC.LSFT)
RS_BSLS = KC.HT(KC.BSLS, KC.RSFT)
TD_ESC_A_G_EMO = KC.TD(
    KC.HT(KC.ESC, KC.LALT, prefer_hold=False),
    KC.LGUI,
    KC.LGUI(KC.DOT)
)

keyboard.keymap = [
    [
        KC.Q, KC.W, KC.F,            KC.P,    KC.G,   KC.J,    KC.L,    KC.U,            KC.Y,   KC.BSPC,
        KC.A, KC.R, KC.S,            KC.T,    KC.D,   KC.H,    KC.N,    KC.E,            KC.I,   KC.O,
        LS_Z, KC.X, KC.C,            KC.V,    KC.B,   KC.K,    KC.M,    KC.COMM,         KC.DOT, RS_SLSH,
                    TD_ESC_C_SL_EMO, KC.LALT, LG_SPC, LY2_TAB, LY3_ENT, TD_ESC_C_SL_EMO,
    ],
    [
        KC.Q, KC.W, KC.F,           KC.P,   KC.G,   KC.J,    KC.L,    KC.U,          KC.Y,   KC.BSPC,
        KC.A, KC.R, KC.S,           KC.T,   KC.D,   KC.H,    KC.N,    KC.E,          KC.I,   KC.O,
        LS_Z, KC.X, KC.C,           KC.V,   KC.B,   KC.K,    KC.M,    KC.COMM,       KC.DOT, RS_SLSH,
                    TD_ESC_A_G_EMO, KC.CTL, KC.SPC, LY2_TAB, LY3_ENT, TD_ESC_A_G_EMO
    ],
    [
        KC.UNDS, KC.MINS, KC.PLUS, KC.EQL,  KC.COLN, KC.GRV,  KC.MRWD, KC.MPLY, KC.MFFD, KC.DEL,
        KC.LCBR, KC.LPRN, KC.RPRN, KC.RCBR, KC.PIPE, KC.ESC,  KC.LEFT, KC.UP,   KC.DOWN, KC.RGHT,
        LS_LBRC, KC.QUOT, KC.DQUO, KC.RBRC, KC.SCLN, KC.TILD, KC.VOLD, KC.MUTE, KC.VOLU, RS_BSLS,
                          KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
    ],
    [
        KC.EXLM, KC.AT, KC.HASH, KC.DLR, KC.PERC,  KC.CIRC, KC.AMPR, KC.ASTR, KC.CAPS, KC.BSPC,
        KC.N1,   KC.N2, KC.N3,   KC.N4,  KC.N5,    KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,
        KC.LSFT, KC.NO, KC.NO,   KC.NO,  KC.MO(4), KC.NO,   KC.NO,   KC.COMM, KC.DOT,  RS_SLSH,
                        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
    ],
    [
        KC.DF(0), KC.NO, KC.NO,   KC.NO,    KC.NO,   KC.NO,   KC.NO,   KC.NO,  KC.NO, KC.DF(1),
        KC.F1,    KC.F2, KC.F3,   KC.F4,    KC.F5,   KC.F6,   KC.F7,   KC.F8,  KC.F9, KC.F10,
        KC.F11,   KC.NO, KC.NO,   KC.RESET, KC.TRNS, KC.NO,   KC.NO,   KC.NO,  KC.NO, KC.F12,
                         KC.TRNS, KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
    ]
]
