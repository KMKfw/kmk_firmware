from kmk.keys import KC
from kmk.modules.combos import Chord


# Home row mods
# Left side
T_SHIFT = KC.HT(KC.T, KC.LSFT, prefer_hold=False, tap_time=200)
S_CTRL = KC.HT(KC.S, KC.LCTRL, prefer_hold=False, tap_time=200)
R_ALT = KC.HT(KC.R, KC.LALT, prefer_hold=False, tap_time=300)
A_META = KC.HT(KC.A, KC.LWIN, prefer_hold=False, tap_time=300)

# Right side
N_SHIFT = KC.HT(KC.N, KC.LSFT, prefer_hold=False, tap_time=200)
E_CTRL = KC.HT(KC.E, KC.LCTRL, prefer_hold=False, tap_time=200)
I_ALT = KC.HT(KC.I, KC.LALT, prefer_hold=False, tap_time=300)
O_META = KC.HT(KC.O, KC.LWIN, prefer_hold=False, tap_time=300)

# Define
XXXX = KC.NO
____ = KC.TRANSPARENT
SYMBOL = KC.MO(1)
MOD = KC.MO(2)


###########
# Swedish #
###########

# @
AT = KC.RALT(KC.N2)
# {}
L_CIRLYBRACKET = KC.RALT(KC.N7)
R_CIRLYBRACKET = KC.RALT(KC.N0)
CIRLYBRACKET = KC.HT(L_CIRLYBRACKET, R_CIRLYBRACKET)

# ()
L_PARENT = KC.RSFT(KC.N8)
R_PARENT = KC.RSFT(KC.N9)
PARENT = KC.HT(L_PARENT, R_PARENT)

# []
L_SQUERE_BRACKET = KC.RALT(KC.N8)
R_SQUERE_BRACKET = KC.RALT(KC.N9)
SQUERE_BRACKET = KC.HT(L_SQUERE_BRACKET, R_SQUERE_BRACKET)

# < | >
LESS_THAN = KC.NUBS
GREATER_THAN = KC.RSFT(KC.NUBS)
PIPE = KC.RALT(KC.NUBS)

# + ? - = *
MINUS = KC.SLASH
PLUS = KC.MINS
QUESTION = KC.RSFT(KC.MINS)
EQUAL = KC.RSFT(KC.N0)
MULTIPLY = KC.RSFT(KC.BSLASH)

# £ $ €
POUND = KC.RALT(KC.N3)
DOLLAR = KC.RALT(KC.N4)
EURO = KC.RALT(KC.N5)

# % &
PERCENT = KC.RSFT(KC.N5)
AND = KC.RSFT(KC.N6)

# / \
SLASH = KC.RSFT(KC.N7)
BACKSLASH = KC.RALT(KC.MINS)

# å ä ö
SWE_Å = KC.LBRC
SWE_Ä = KC.QUOT
SWE_Ö = KC.SCLN

# ^ ~
HAT = KC.RSFT(KC.RBRC)
TILDE = KC.RALT(KC.RBRC)

# " ' ´ `
DUB_QUOTE = KC.RSFT(KC.N2)
QUOTE = KC.BSLASH
R_QUOTE = KC.RALT(KC.BSLASH)
L_QUOTE = KC.RSFT(KC.EQUAL)

# (-_) (.:) (,;)
DASH = KC.HT(KC.SLASH, KC.RSFT(KC.SLASH))
DOT = KC.HT(KC.DOT, KC.RSFT(KC.DOT))
COMMA = KC.HT(KC.COMMA, KC.RSFT(KC.COMMA))

#####################
# End of definition #
#####################

COMBO_LAYER = {
    (1, 2): 3,
}


COMBOS = [
    #Left Side
    Chord((KC.F, KC.P), KC.ESC),
    Chord((S_CTRL, T_SHIFT), KC.TAB),

    # Right side
    Chord((KC.L, KC.U), KC.ENT),
    Chord((N_SHIFT, E_CTRL), KC.BSPACE),
    Chord((KC.H, COMMA), KC.DEL)
]

KEYMAP = [
    [# Colemak-DH
        # q w f p b      j l  u     y    bsp
        # a r s t g      m n  e     i    o
        # z x c d v      k h (,;) (.:) (-_)
        #    spc SYM    MOD SFT

        KC.Q,    KC.W,    KC.F,    KC.P,    KC.B,       KC.J,    KC.L,    KC.U,   KC.Y,   KC.BSPACE, \
        A_META,  R_ALT,  S_CTRL,  T_SHIFT, KC.G,        KC.M,    N_SHIFT, E_CTRL, I_ALT, O_META, \
        KC.Z,    KC.X,    KC.C,    KC.D,    KC.V,       KC.K,    KC.H,    COMMA,  DOT,  DASH, \
                            KC.SPACE,    SYMBOL,        MOD,     KC.RSFT,
    ],
    [# Symbol
        #     ! @ # {/} |    + - = * Å
        #     $ % & (/) /    ~ ' " Ö Ä
        #     X < > [/] \    ` ´ £ € ^
        #         spc SYM    MOD SFT
        KC.EXLM, AT,        KC.HASH,      CIRLYBRACKET,   PIPE,              PLUS,     MINUS,   EQUAL,     MULTIPLY, SWE_Å, \
        DOLLAR,  PERCENT,   AND,          PARENT,         SLASH,             TILDE,    QUOTE,   DUB_QUOTE, SWE_Ö,    SWE_Ä, \
        XXXX,    LESS_THAN, GREATER_THAN, SQUERE_BRACKET, BACKSLASH,         L_QUOTE,  R_QUOTE, POUND,     EURO,     HAT, \
                                            KC.SPACE,       SYMBOL,            MOD,      KC.RSFT,
    ],
    [# MOD
        # BRI+ BRI- VOL- VOL+  X        HOME  PG_DN PG_UP END BSP
        # META ALT  CTRL SHIFT X        X      ←     ↓     ↑     →
        # ESC Mctrl Mshift TAB   REP*     REP*  ENT   +     -   DEL
        #                   spc SYM    MOD SFT
        KC.BRIGHTNESS_DOWN, KC.BRIGHTNESS_UP, KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP, KC.MEDIA_PLAY_PAUSE,          KC.HOME, KC.PGDOWN, KC.PGUP, KC.END,   KC.BSPACE, \
        KC.LGUI,            KC.LALT,           KC.LCTRL,           KC.LSHIFT,       XXXX,                         XXXX,     KC.LEFT, KC.DOWN,   KC.UP,   KC.RIGHT, \
        KC.ESC,             KC.LGUI(KC.LCTRL), KC.LGUI(KC.LSHIFT), KC.TAB,          XXXX,                         XXXX,    KC.ENT,    PLUS,    MINUS,     KC.DEL, \
                                                                  KC.SPACE,        SYMBOL,                        MOD,     KC.RSFT,
    ],
    [# NUM
        # X f7 f8 f9 f10   X 7 8 9 BSP
        # X f4 f5 f6 f11   X 4 5 6 X
        # X f1 f2 f3 f12   0 1 2 3 X
        #            X X   X X
        XXXX, KC.F7, KC.F7, KC.F8, KC.F10,       XXXX,  KC.N7,  KC.N8, KC.N9, KC.BSPACE, \
        XXXX, KC.F4, KC.F5, KC.F6, KC.F11,       XXXX,  KC.N4, KC.N5, KC.N6, XXXX, \
        XXXX, KC.F1, KC.F2, KC.F3, KC.F12,       KC.N0, KC.N1, KC.N2, KC.N3, XXXX, \
                             XXXX,    XXXX,       XXXX,  XXXX,
    ]
]
