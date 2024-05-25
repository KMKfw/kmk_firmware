from kmk.keys import KC
from kmk.modules.combos import Chord

# Home row mods
# Left side
T_SHIFT = KC.HT(KC.T, KC.LSFT, prefer_hold=False, tap_time=200)
S_CTRL = KC.HT(KC.S, KC.LCTRL, prefer_hold=False, tap_time=200)
R_ALT = KC.HT(KC.R, KC.LALT, prefer_hold=False, tap_time=300)
A_META = KC.HT(KC.A, KC.LWIN, prefer_hold=False, tap_time=300)

D_WM = KC.HT(KC.D, KC.MO(5), prefer_hold=False, tap_time=300)
SPACE_NUM = KC.HT(KC.SPACE, KC.MO(3), prefer_hold=False, tap_time=300)


# Right side
N_SHIFT = KC.HT(KC.N, KC.LSFT, prefer_hold=False, tap_time=200)
E_CTRL = KC.HT(KC.E, KC.LCTRL, prefer_hold=False, tap_time=200)
I_ALT = KC.HT(KC.I, KC.LALT, prefer_hold=False, tap_time=300)
O_META = KC.HT(KC.O, KC.LWIN, prefer_hold=False, tap_time=300)

# Define
XXXX = KC.NO
____ = KC.TRANSPARENT
SYMBOL = KC.LT(1, KC.TO(6))

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
HOLD_QUOTE = KC.HT(QUOTE, DUB_QUOTE)

# (-_) (.:) (,;)
DASH = KC.HT(KC.SLASH, KC.RSFT(KC.SLASH))
DOT = KC.HT(KC.DOT, KC.RSFT(KC.DOT))
COMMA = KC.HT(KC.COMMA, KC.RSFT(KC.COMMA))

# Zoom CTRL(+) CTRL(-)  CTRL(0)
ZOOM_IN = KC.LCTRL(PLUS)
ZOOM_OUT = KC.LCTRL(MINUS)
ZOOM_RESET = KC.LCTRL(KC.N0)


# WM MOVEMENT
# GO
GO_LEFT = KC.LGUI(KC.LEFT)
GO_DOWN = KC.LGUI(KC.DOWN)
GO_UP = KC.LGUI(KC.UP)
GO_RIGHT = KC.LGUI(KC.RIGHT)
# MOVE
MOVE_LEFT = KC.LGUI(KC.LSFT(KC.LEFT))
MOVE_DOWN = KC.LGUI(KC.LSFT(KC.DOWN))
MOVE_UP = KC.LGUI(KC.LSFT(KC.UP))
MOVE_RIGHT = KC.LGUI(KC.LSFT(KC.RIGHT))
# JUMP
JUMP_LEFT = KC.LGUI(KC.LCTRL(KC.LEFT))
JUMP_DOWN = KC.LGUI(KC.LCTRL(KC.DOWN))
JUMP_UP = KC.LGUI(KC.LCTRL(KC.UP))
JUMP_RIGHT = KC.LGUI(KC.LCTRL(KC.RIGHT))

# MOUSE
MOUSE_LEFT = KC.MS_LEFT
MOUSE_DOWN = KC.MS_DOWN
MOUSE_UP = KC.MS_UP
MOUSE_RIGHT = KC.MS_RIGHT

LEFT_CLICK = KC.MB_LMB
RIGHT_CLICK = KC.MB_RMB

SCROLL_UP = KC.MW_UP
SCROLL_DOWN = KC.MW_DOWN
MOUSE_ESC = KC.NO


#####################
# End of definition #
#####################

COMBO_LAYER = {
    (1, 2): 4,  # Switch to F NUM layer
}

COMBOS = [
    # Left Side
    Chord((KC.F, KC.P), KC.ESC),
    Chord((S_CTRL, T_SHIFT), KC.TAB),
    Chord((MOUSE_UP, MOUSE_ESC), KC.ESC),
    # Right side
    Chord((KC.L, KC.U), KC.ENT),
    Chord((N_SHIFT, E_CTRL), KC.BSPACE),
    Chord((KC.H, COMMA), KC.DEL),
]

# fmt: off
KEYMAP = [
    [  # Colemak-DH 0
        # q w f p b      j l  u     y    '
        # a r s t g      m n  e     i    o
        # z x c d v      k h (,;) (.:) (-_)
        #    spc SYM    MOD SFT

        KC.Q, KC.W, KC.F, KC.P, KC.B,               KC.J, KC.L, KC.U, KC.Y, HOLD_QUOTE,
        A_META, R_ALT, S_CTRL, T_SHIFT, KC.G,       KC.M, N_SHIFT, E_CTRL, I_ALT, O_META,
        KC.Z, KC.X, KC.C, D_WM, KC.V,              KC.K, KC.H, COMMA, DOT, DASH,
        SPACE_NUM, SYMBOL,                           MOD, KC.RSFT,
    ],
    [  # Symbol 1
        #     ! @ # {/} ?    + - = * Å
        #     $ % & (/) /    ~ ' " Ö Ä
        #     | < > [/] \    ` ´ £ € ^
        #         spc SYM    MOD SFT
        KC.EXLM, AT, KC.HASH, CIRLYBRACKET, QUESTION,                   PLUS, MINUS, EQUAL, MULTIPLY, SWE_Å,
        DOLLAR, PERCENT, AND, PARENT, SLASH,                            TILDE, QUOTE, DUB_QUOTE, SWE_Ö, SWE_Ä,
        PIPE, LESS_THAN, GREATER_THAN, SQUERE_BRACKET, BACKSLASH,       L_QUOTE, R_QUOTE, POUND, EURO, HAT,
        KC.SPACE, SYMBOL,                                               MOD, KC.RSFT,
    ],
    [  # MOD 2
        # BRI+ BRI- VOL- VOL+ MUTE      HOME  PG_DN  PG_UP   END      BSP
        # META ALT  CTRL SHIFT INSERT              X     ←      ↓       ↑        →
        # ESC PLAY/PAUSE Mshift PSCR PSCR        X     ENT    CTRL(+) CTRL(-)  CTRL(0)
        #                   spc SYM    MOD SFT
        KC.BRIGHTNESS_DOWN, KC.BRIGHTNESS_UP, KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP, KC.AUDIO_MUTE,     KC.HOME, KC.PGDOWN, KC.PGUP, KC.END, KC.BSPACE,
        KC.LGUI, KC.LALT, KC.LCTRL, KC.LSHIFT, KC.INSERT,                                               XXXX, KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT,
        KC.ESC, KC.MEDIA_PLAY_PAUSE, KC.MEDIA_PREV_TRACK, KC.MEDIA_NEXT_TRACK, KC.PSCREEN,                              XXXX, KC.ENT, ZOOM_IN, ZOOM_OUT, ZOOM_RESET,
        KC.SPACE, SYMBOL,                                                                                  MOD, KC.RSFT,
    ],
    [  # NUM 3
        # X     X    X   X     X   * 7 8 9 BSP
        # META ALT  CTRL SHIFT X   / 4 5 6 X
        # X     X    X   X     X   - 1 2 3 X
        #                X     X   + 0
        XXXX, XXXX, XXXX, XXXX, XXXX,                       MULTIPLY, KC.N7, KC.N8, KC.N9, KC.BSPACE,
        KC.LGUI, KC.LALT, KC.LCTRL, KC.LSHIFT, XXXX,        SLASH, KC.N4, KC.N5, KC.N6, XXXX,
        XXXX, XXXX, XXXX, XXXX, XXXX,                       MINUS, KC.N1, KC.N2, KC.N3, XXXX,
        XXXX, XXXX,                                         PLUS, KC.N0,
    ],
    [  # F NUM 4
        # X     X    X   X     X   X f7 f8 f9 f10
        # META ALT  CTRL SHIFT X   X f4 f5 f6 f11
        # X     X    X   X     X   X f1 f2 f3 f12
        #                X     X   X X
        XXXX, XXXX, XXXX, XXXX, XXXX,                        XXXX, KC.F7, KC.F7, KC.F8, KC.F10,
        KC.LGUI, KC.LALT, KC.LCTRL, KC.LSHIFT, XXXX,         XXXX, KC.F4, KC.F5, KC.F6, KC.F11,
        XXXX, XXXX, XXXX, XXXX, XXXX,                        XXXX, KC.F1, KC.F2, KC.F3, KC.F12,
        XXXX, XXXX,                                          XXXX, XXXX,
    ],
    [  # WM 5
        # X     X    X   X     X   X ML MD MU MR
        # META ALT  CTRL SHIFT X   X GL GD GU GR
        # X     X    X   X     X   X JL JD JU JR
        #                X     X   X X
        XXXX, XXXX, XXXX, XXXX, XXXX,                        XXXX, MOVE_LEFT, MOVE_DOWN, MOVE_UP, MOVE_RIGHT,
        KC.LGUI, KC.LALT, KC.LCTRL, KC.LSHIFT, XXXX,         XXXX, GO_LEFT, GO_DOWN, GO_UP, GO_RIGHT,
        XXXX, XXXX, XXXX, XXXX, XXXX,                        XXXX, JUMP_LEFT, JUMP_DOWN, JUMP_UP, JUMP_RIGHT,
        XXXX, XXXX,                                          XXXX, XXXX,
    ],
    [  # MOUSE 6
        XXXX, XXXX, MOUSE_UP, MOUSE_ESC, XXXX,                        SCROLL_UP, XXXX, XXXX, XXXX, XXXX,
        XXXX, MOUSE_LEFT, MOUSE_DOWN, MOUSE_RIGHT, XXXX,         SCROLL_DOWN, LEFT_CLICK, RIGHT_CLICK, XXXX, XXXX,
        XXXX, XXXX, XXXX, XXXX, XXXX,                            XXXX, XXXX, XXXX, XXXX, XXXX,
        XXXX, KC.TO(0),                                          XXXX, XXXX,
    ],
]
# fmt: on
