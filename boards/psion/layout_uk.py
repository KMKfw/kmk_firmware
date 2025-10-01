from kmk.keys import KC
from kmk.modules.combos import Sequence

# Layer keys
FNKEY = KC.MO(1)

# Shift keys overrides
# One for both right shift and left shift
# fmt: off
COMBOS = [
    # Add DEL to Backspace
    Sequence((KC.LSFT, KC.BSPC), KC.DEL, fast_reset=False),
    Sequence((KC.RSFT, KC.BSPC), KC.DEL, fast_reset=False),

    # Add CAPS LOCK to Tab
    Sequence((KC.LSFT, KC.TAB), KC.CAPS, fast_reset=False),
    Sequence((KC.RSFT, KC.TAB), KC.CAPS, fast_reset=False),

    # Add ~ to '
    Sequence((KC.LSFT, KC.QUOT), KC.TILD, fast_reset=False),
    Sequence((KC.RSFT, KC.QUOT), KC.TILD, fast_reset=False),

    # Add ? to .
    Sequence((KC.LSFT, KC.DOT), KC.LSFT(KC.SLSH), fast_reset=False),
    Sequence((KC.RSFT, KC.DOT), KC.RSFT(KC.SLSH), fast_reset=False),

    # Add / to ,
    Sequence((KC.LSFT, KC.COMM), KC.SLSH, fast_reset=False),
    Sequence((KC.RSFT, KC.COMM), KC.SLSH, fast_reset=False),
]
# fmt: on

# fmt: off
KEYMAP = [
    # Base layer
    [
        KC.NO,   KC.N1,              KC.N2,   KC.N3,              KC.N4,              KC.N5,              KC.N6,            KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,
        KC.NO,   KC.N7,              KC.N8,   KC.N9,              KC.N0,              KC.BSPC,            KC.QUOT,          KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,
        KC.ESC,  KC.Q,               KC.W,    KC.E,               KC.R,               KC.T,               KC.Y,             KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,
        KC.NO,   KC.U,               KC.I,    KC.O,               KC.P,               KC.L,               KC.ENT,           KC.NO,   KC.NO,   KC.NO,   KC.LALT, KC.N0,
        KC.NO,   KC.TAB,             KC.A,    KC.S,               KC.D,               KC.F,               KC.G,             KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.LCTL,
        KC.NO,   KC.H,               KC.J,    KC.K,               KC.M,               KC.DOT,             KC.DOWN,          KC.NO,   KC.NO,   FNKEY,   KC.NO,   KC.NO,
        KC.NO,   KC.Z,               KC.X,    KC.C,               KC.V,               KC.B,               KC.N,             KC.NO,   KC.RSFT, KC.NO,   KC.NO,   KC.NO,
        KC.NO,   KC.NO,              KC.SPC,  KC.UP,              KC.COMM,            KC.LEFT,            KC.RGHT,          KC.LSFT, KC.NO,   KC.NO,   KC.NO,   KC.NO
     ],

     # FN layer
    [
        KC.TRNS, KC.LSHIFT(KC.MINS), KC.BSLS, KC.NUBS,            KC.LSHIFT(KC.QUOT), KC.LSHIFT(KC.COMM), KC.LSFT(KC.DOT),  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.LBRC,            KC.RBRC, KC.LSHIFT(KC.LBRC), KC.LSHIFT(KC.RBRC), KC.TRNS,            KC.LSFT(KC.SCLN), KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.PWR,  KC.TRNS,            KC.TRNS, KC.RALT(KC.E),      KC.TRNS,            KC.TRNS,            KC.PAST,          KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.PSLS,            KC.PPLS, KC.PMNS,            KC.EQUAL,           KC.SCLN,            KC.TRNS,          KC.TRNS, KC.TRNS, KC.TRNS, KC.LGUI, KC.TRNS,
        KC.TRNS, KC.CAPS,            KC.TRNS, KC.TRNS,            KC.TRNS,            KC.TRNS,            KC.TRNS,          KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS,            KC.TRNS, KC.TRNS,            KC.TRNS,            KC.TRNS,            KC.PGDN,          KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS,            KC.TRNS, KC.TRNS,            KC.TRNS,            KC.TRNS,            KC.TRNS,          KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS,            KC.TRNS, KC.PGUP,            KC.TRNS,            KC.HOME,            KC.END,           KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
     ],
]
# fmt: on
