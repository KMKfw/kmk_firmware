# Created by https://github.com/JakobEdvardsson/

import board

from kb import KMKKeyboard, isRight

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide, SplitType
from kmk.modules.holdtap import HoldTap
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.combos import Combos, Chord, Sequence


keyboard = KMKKeyboard()

layers = Layers()

# Split
split_side = SplitSide.RIGHT if isRight else SplitSide.LEFT

data_pin = board.GP1 if split_side == SplitSide.LEFT else board.GP0
data_pin2 = board.GP0 if split_side == SplitSide.LEFT else board.GP1

split = Split(
    split_side=split_side,
    split_type=SplitType.UART,
    split_flip=False,
    data_pin=data_pin,
    data_pin2=data_pin2
)

# Hold tap
holdtap = HoldTap()
# optional: set a custom tap timeout in ms
# holdtap.tap_time = 300
mediaKeys = MediaKeys()

# combo_layer
combo_layers = {
  (1, 2): 3,
}
layerCombo = Layers(combo_layers)

# Combo
combos = Combos()

keyboard.modules = [layers, layerCombo, split, holdtap, mediaKeys, combos]

combos.combos = [
    #Left Side
    Chord((KC.W, KC.F), KC.ESC),
    Chord((KC.F, KC.P), KC.TAB),

    # Right side
    Chord((KC.L, KC.U), KC.ENT),
    Chord((KC.U, KC.Y), KC.BSPACE)
]

# Hold tap
# Left side
T_SHIFT = KC.HT(KC.T, KC.LSFT)
S_CTRL = KC.HT(KC.S, KC.LCTRL)
R_ALT = KC.HT(KC.R, KC.LALT)
A_META = KC.HT(KC.A, KC.LWIN)

# Right side
N_SHIFT = KC.HT(KC.N, KC.LSFT)
E_CTRL = KC.HT(KC.E, KC.LCTRL)
I_ALT = KC.HT(KC.I, KC.LALT)
O_META = KC.HT(KC.O, KC.LWIN)


# Define
XXXX = KC.LCTL
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


# Inspired by https://keymapdb.com/keymaps/kkga/
# https://github.com/kkga/config/blob/625d91022c4163e0dad674270d5a147692eaf9b2/.config/qmk/dacman4x6/keymap.c


keyboard.keymap = [
     [# QWERTY -0

    # Cords
      #Left Side
        # W + F = ESC
        # F + P = TAB
      # Right side
        # L + U = ENT
        # U + Y = BSPACE
        # q+f = ESC

        # q w f p b      j l  u     y    bsp
        # a r s t g      m n  e     i    o
        # z x c d v      k h (,;) (.:) (-_)
        #    spc SYM    MOD SFT

        KC.Q,    KC.W,    KC.F,    KC.P,    KC.B,       KC.J,    KC.L,    KC.U,   KC.Y,   KC.BSPACE,\
        A_META,  R_ALT,  S_CTRL,  T_SHIFT, KC.G,        KC.M,    N_SHIFT, E_CTRL, I_ALT, O_META,\
        KC.Z,    KC.X,    KC.C,    KC.D,    KC.V,       KC.K,    KC.H,    COMMA,  DOT,  DASH,\
                            KC.SPACE,    SYMBOL,        MOD,     KC.RSFT,
    ],
    [# Symbol -1  
        #     ! @ # {/} |    + - = * Å              
        #     $ % & (/) /    ~ ' " Ö Ä
        #     X < > [/] \    ` ´ £ € ^
        #         spc SYM    MOD SFT
        KC.EXLM, AT,        KC.HASH,      CIRLYBRACKET,   PIPE,              PLUS,     MINUS,   EQUAL,     MULTIPLY, SWE_Å,\
        DOLLAR,  PERCENT,   AND,          PARENT,         SLASH,             TILDE,    QUOTE,   DUB_QUOTE, SWE_Ö,    SWE_Ä,\
        XXXX,    LESS_THAN, GREATER_THAN, SQUERE_BRACKET, BACKSLASH,         L_QUOTE,  R_QUOTE, POUND,     EURO,     HAT,\
                                          KC.SPACE,       SYMBOL,            MOD,      KC.RSFT,
    ],
    [# MOD -2
        # BRI+ BRI- VOL- VOL+  X        HOME  PG_DN PG_UP END X
        # META ALT  CTRL SHIFT X        ←     ↓     ↑     →   BSP
        # ESC  X    X    TAB   REP*     REP*  ENT   X     X   DEL
        #                   spc SYM    MOD SFT
        KC.BRIGHTNESS_DOWN, KC.BRIGHTNESS_UP, KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP, KC.MEDIA_PLAY_PAUSE,          KC.HOME, KC.PGDOWN, KC.PGUP, KC.END,   KC.BSPACE,\
        KC.LGUI,            KC.ALT,           KC.CTRL,           KC.LSHIFT,       XXXX,                         KC.LEFT, KC.DOWN,   KC.UP,   KC.RIGHT, KC.BSPACE,\
        KC.ESC,             XXXX,             XXXX,              KC.TAB,          XXXX,                         XXXX,    KC.ENT,    XXXX,    XXXX,     KC.DEL,\
                                                                 KC.SPACE,        SYMBOL,                        MOD,     KC.RSFT,
    ],
    [# NUM -3
        # X f7 f8 f9 f10   X 7 8 9 X
        # X f4 f5 f6 f11   X 4 5 6 X
        # X f1 f2 f3 f12   0 1 2 3 X
        #            X X   X X
        XXXX, KC.F7, KC.F7, KC.F8, KC.F10,       XXXX,  KC.N7,  KC.N8, KC.N9, KC.BSPACE,\
        XXXX, KC.F4, KC.F5, KC.F6, KC.F11,       XXXX,  KC.N4, KC.N5, KC.N6, XXXX,\
        XXXX, KC.F1, KC.F2, KC.F3, KC.F12,       KC.N0, KC.N1, KC.N2, KC.N3, XXXX,\
                            XXXX,    XXXX,       XXXX,  XXXX,
    ]
]

if __name__ == '__main__':
    keyboard.go()