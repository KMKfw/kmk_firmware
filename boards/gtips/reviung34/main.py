from kb import KMKKeyboard

from kmk.extensions.peg_rgb_matrix import Rgb_matrix
from kmk.keys import KC
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()

# Adding extensions
# ledmap
rgb = Rgb_matrix(
    ledDisplay=[
        [55, 55, 55],
        [55, 55, 55],
        [55, 55, 55],
        [55, 55, 55],
        [55, 55, 55],
        [55, 55, 55],
        [55, 55, 55],
        [55, 55, 55],
        [55, 55, 55],
    ],
    split=False,
    rightSide=False,
    disable_auto_write=True,
)
keyboard.extensions.append(rgb)
keyboard.modules.append(Layers())

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(2)
RAISE = KC.MO(1)

# fmt:off
keyboard.keymap = [
    [   # QWERTY
        KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,               KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,
        KC.A,    KC.S,    KC.D,    KC.F,    KC.G,               KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN,
        KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,               KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH,
                                       LOWER,  KC.SPC,     KC.BSPC,    RAISE,
    ],
    [   # RAISE
        KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,              KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,
        KC.TAB,  KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT,            XXXXXXX, KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC,
        KC.LCTL, KC.GRV,  KC.LGUI, KC.LALT, XXXXXXX,            XXXXXXX, XXXXXXX, XXXXXXX, KC.BSLS, KC.QUOT,
                                     XXXXXXX, XXXXXXX,      XXXXXXX, XXXXXXX,
    ],
    [   # LOWER
        KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC,            KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN,
        KC.ESC,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,            XXXXXXX, KC.UNDS, KC.PLUS, KC.LCBR, KC.RCBR,
        KC.CAPS, KC.TILD, XXXXXXX, XXXXXXX, XXXXXXX,            XXXXXXX, XXXXXXX, XXXXXXX, KC.PIPE, KC.DQT,
                                     XXXXXXX, XXXXXXX,       KC.ENT,  KC.DEL,
    ],
]
# fmt:on

if __name__ == '__main__':
    keyboard.go()
