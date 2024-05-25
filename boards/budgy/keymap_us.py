from kmk.keys import KC
from kmk.modules.combos import Chord

# Home row mods
# Left side
F_SHIFT = KC.HT(KC.F, KC.LSFT, prefer_hold=False, tap_time=200)
D_CTRL = KC.HT(KC.D, KC.LCTRL, prefer_hold=False, tap_time=200)
S_ALT = KC.HT(KC.S, KC.LALT, prefer_hold=False, tap_time=300)
A_META = KC.HT(KC.A, KC.LWIN, prefer_hold=False, tap_time=300)

# Right side
J_SHIFT = KC.HT(KC.J, KC.LSFT, prefer_hold=False, tap_time=200)
K_CTRL = KC.HT(KC.K, KC.LCTRL, prefer_hold=False, tap_time=200)
L_ALT = KC.HT(KC.L, KC.LALT, prefer_hold=False, tap_time=300)
SEMICOLON_META = KC.HT(KC.SCLN, KC.LWIN, prefer_hold=False, tap_time=300)

# Define
XXXX = KC.NO
____ = KC.TRANSPARENT
SYMBOL = KC.MO(1)
MOD = KC.MO(2)


# {}
CIRLYBRACKET = KC.HT(KC.LSFT(KC.LBRACKET), KC.LSFT(KC.RBRACKET))

# ()
PARENT = KC.HT(KC.LPRN, KC.RPRN)

# []
SQUERE_BRACKET = KC.HT(KC.LBRACKET, KC.RBRACKET)


# (,<) (.>) (/?)
DOT = KC.HT(KC.DOT, KC.RSFT(KC.DOT))
COMMA = KC.HT(KC.COMMA, KC.RSFT(KC.COMMA))
SLASH = KC.HT(KC.SLASH, KC.RSFT(KC.SLASH))

#####################
# End of definition #
#####################

COMBO_LAYER = {
    (1, 2): 3,
}


COMBOS = [
    # Left Side
    Chord((KC.E, KC.R), KC.ESC),
    Chord((D_CTRL, F_SHIFT), KC.TAB),
    # Right side
    Chord((KC.U, KC.I), KC.ENT),
    Chord((J_SHIFT, K_CTRL), KC.BSPACE),
    Chord((KC.M, COMMA), KC.DEL),
]
# fmt: off
KEYMAP = [
    [  # Qwerty
        # q w e r t      y u  i     o    p
        # a s d f g      h j  k     l    ;
        # z x c v b      n m (,<) (.>) (/?)
        #    spc SYM    MOD SFT
        KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,       KC.Y,    KC.U,    KC.I,   KC.O,   KC.P,
        A_META,  S_ALT,  D_CTRL,  F_SHIFT, KC.G,        KC.H,    J_SHIFT, K_CTRL, L_ALT, SEMICOLON_META,
        KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,       KC.N,    KC.M,    COMMA,  DOT,  SLASH,
                            KC.SPACE,    SYMBOL,        MOD,     KC.RSFT,
    ],
    [  # Symbol
        #     ! @ # {/} ?    + - = * X
        #     $ % & (/) /    ~ ' " X X
        #     | < > [/] \    ` X X X ^
        #         spc SYM    MOD SFT
        KC.EXLM, KC.AT,        KC.HASH,      CIRLYBRACKET,   KC.RSFT(KC.SLSH),              KC.PLUS,     KC.MINUS,   KC.EQUAL, KC.ASTR, XXXX,
        KC.DOLLAR,  KC.PERCENT,   KC.AMPR,          PARENT,         SLASH,             KC.TILDE,    KC.QUOTE, KC.RSFT(KC.QUOTE), XXXX,    XXXX,
        KC.PIPE,    KC.RSFT(KC.COMM), KC.RSFT(KC.DOT), SQUERE_BRACKET, KC.BSLASH,         KC.GRV,  XXXX, XXXX,     XXXX,     KC.CIRC,
                                             KC.SPACE,       SYMBOL,            MOD,      KC.RSFT,
    ],
    [  # MOD
        # BRI+ BRI- VOL- VOL+  X        HOME  PG_DN PG_UP END BSP
        # META ALT  CTRL SHIFT X        X      ←     ↓     ↑     →
        # ESC Mctrl Mshift TAB   REP*     REP*  ENT   +     -   DEL
        #                   spc SYM    MOD SFT
        KC.BRIGHTNESS_DOWN, KC.BRIGHTNESS_UP, KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP, KC.MEDIA_PLAY_PAUSE,          KC.HOME, KC.PGDOWN, KC.PGUP, KC.END,   KC.BSPACE,
        KC.LGUI,            KC.LALT,           KC.LCTRL,           KC.LSHIFT,       XXXX,                         XXXX,     KC.LEFT, KC.DOWN,   KC.UP,   KC.RIGHT,
        KC.ESC,             KC.LGUI(KC.LCTRL), KC.LGUI(KC.LSHIFT), KC.TAB,          XXXX,                         XXXX,    KC.ENT,    KC.PLUS,    KC.MINUS,     KC.DEL,
                                                                   KC.SPACE,        SYMBOL,                        MOD,     KC.RSFT,
    ],
    [  # NUM
        # X f7 f8 f9 f10   X 7 8 9 BSP
        # X f4 f5 f6 f11   X 4 5 6 X
        # X f1 f2 f3 f12   0 1 2 3 X
        #            X X   X X
        XXXX, KC.F7, KC.F7, KC.F8, KC.F10,       XXXX,  KC.N7,  KC.N8, KC.N9, KC.BSPACE,
        XXXX, KC.F4, KC.F5, KC.F6, KC.F11,       XXXX,  KC.N4, KC.N5, KC.N6, XXXX,
        XXXX, KC.F1, KC.F2, KC.F3, KC.F12,       KC.N0, KC.N1, KC.N2, KC.N3, XXXX,
                            XXXX,    XXXX,       XXXX,  XXXX,
    ]
]
# fmt: on
