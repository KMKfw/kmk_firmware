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

# keymap aliases
CUT = KC.LCTL(KC.X)
COPY = KC.LCTL(KC.C)
PASTE = KC.LCTL(KC.V)
REDO = KC.LCTL(KC.Y)
UNDO = KC.LCTL(KC.Z)
SALL = KC.LCTL(KC.A)
SLFT = KC.LSFT(KC.HOME)
SRGHT = KC.LSFT(KC.END)
TSKMGR = KC.LSFT(KC.LCTL(KC.ESC))
APP_N = KC.LALT(KC.TAB)
APP_P = KC.LSFT(KC.LALT(KC.TAB))
APP_X = KC.LALT(KC.F4)
Z_IN = KC.LCTL(KC.MINS)
Z_OUT = KC.LCTL(KC.EQL)
Z_RST = KC.CTL(KC.N0)

# fmt:off
keyboard.keymap = [
    [   # 0
        APP_P, KC.GRV,  KC.N1,   KC.N2,   KC.N3,   KC.N4,  KC.N5,                                           KC.N6,    KC.N7, KC.N8,   KC.N9,   KC.N0,   KC.PSCR, APP_N,
        SLFT,  KC.ESC,  KC.Q,    KC.W,    KC.E,    KC.R,   KC.T,                                            KC.Y,     KC.U,  KC.I,    KC.O,    KC.P,    KC.BSLS, SRGHT,
        COPY,  KC.TAB,  KC.A,    KC.S,    KC.D,    KC.F,   KC.G,                                            KC.H,     KC.J,  KC.K,    KC.L,    KC.SCLN, KC.QUOT, PASTE,
        CUT,   KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,   KC.B,     KC.HOME, KC.PGUP,    KC.VOLU, KC.END,  KC.N,     KC.M,  KC.COMM, KC.DOT,  KC.SLSH, KC.LALT, SALL,
        UNDO,  KC.LCTL, KC.LALT, KC.LGUI, KC.MINS, KC.EQL, KC.MO(1), KC.SPC,  KC.DEL,     KC.BSPC, KC.ENT,  KC.MO(2), KC.UP, KC.DOWN, KC.LBRC, KC.RBRC, KC.RSFT, REDO,
                                                           KC.UP,    KC.DOWN, KC.PGDN,    KC.VOLD, KC.LEFT, KC.RGHT,
    ],
    [   # 1
        KC.TRNS, KC.NO,  KC.NO, KC.NO,   KC.NO,  KC.NO,   KC.NO,                                      KC.NO,   KC.NO,   KC.NO, KC.NO,   KC.NO,   KC.NO, KC.TRNS,
        KC.TRNS, TSKMGR, APP_X, KC.SLCK, KC.INS, KC.PAUS, KC.NO,                                      KC.NLCK, KC.P7,   KC.P8, KC.P9,   KC.NO,   KC.NO, KC.TRNS,
        KC.TRNS, KC.F1,  KC.F2, KC.F3,   KC.F4,  KC.F5,   KC.F6,                                      KC.PAST, KC.P4,   KC.P5, KC.P6,   KC.PMNS, KC.NO, KC.TRNS,
        KC.TRNS, KC.F7,  KC.F8, KC.F9,   KC.F10, KC.F11,  KC.F12,  KC.NO, KC.NO,    Z_OUT,   KC.RCTL, KC.PSLS, KC.P1,   KC.P2, KC.P3,   KC.PPLS, KC.NO, KC.TRNS,
        KC.TRNS, KC.NO,  KC.NO, KC.NO,   KC.NO,  KC.NO,   KC.TRNS, KC.NO, KC.NO,    KC.RSFT, KC.PENT, KC.LALT, KC.PCMM, KC.P0, KC.PDOT, KC.NO,   KC.NO, KC.TRNS,
                                                          KC.NO,   KC.NO, KC.NO,    Z_IN,    KC.RGUI, Z_RST,
    ],
    [   # 2
        KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO,   KC.NO,   KC.NO,                                      KC.NO,   KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.TRNS,
        KC.TRNS, KC.NO, KC.NO, KC.NO, KC.BRIU, KC.VOLU, KC.NO,                                      KC.NO,   KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.TRNS,
        KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO,   KC.MUTE, KC.NO,                                      KC.NO,   KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.TRNS,
        KC.TRNS, KC.NO, KC.NO, KC.NO, KC.BRID, KC.VOLD, KC.NO,   KC.NO,   KC.NO,      KC.NO, KC.NO, KC.NO,   KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.TRNS,
        KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO,   KC.NO,   KC.MPRV, KC.MPLY, KC.MNXT,    KC.NO, KC.NO, KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.TRNS,
                                                        KC.NO,   KC.MSTP, KC.NO,      KC.NO, KC.NO, KC.NO,
    ],
]
# fmt:on
