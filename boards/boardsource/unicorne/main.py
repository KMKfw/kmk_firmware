import supervisor

from kb import KMKKeyboard

from kmk.extensions.peg_oled_Display import (
    Oled,
    OledData,
    OledDisplayMode,
    OledReactionType,
)
from kmk.extensions.peg_rgb_matrix import Rgb_matrix
from kmk.handlers.sequences import send_string
from kmk.hid import HIDModes
from kmk.keys import KC
from kmk.modules.combos import Chord, Combos
from kmk.modules.holdtap import HoldTapRepeat
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.modules.oneshot import OneShot
from kmk.modules.split import Split, SplitSide, SplitType

supervisor.runtime.autoreload = False
keyboard = KMKKeyboard()
modtap = ModTap()
combos = Combos()
oneshot = OneShot()
layers = Layers()
oneshot.tap_time = 450


OS_LCTL = KC.OS(KC.LCTL)
OS_LSFT = KC.OS(KC.LSFT)
OS_LALT = KC.OS(KC.LALT)
keyboard.modules.append(oneshot)
keyboard.modules.append(layers)
keyboard.modules.append(modtap)
keyboard.modules.append(combos)

# oled
oled = Oled(
    OledData(
        corner_one={
            0: OledReactionType.STATIC,
            1: ['1 2 3 4 5 6', '', '', '', '', '', '', ''],
        },
        corner_two={
            0: OledReactionType.STATIC,
            1: [' 7 8 Layer', '', '', '', '', '', '', ' 7 8 Layer'],
        },
        corner_three={
            0: OledReactionType.LAYER,
            1: ['^', '  ^', '    ^', '      ^', '        ^', '          ^', '', ''],
        },
        corner_four={
            0: OledReactionType.LAYER,
            1: ['', '', '', '', '', '', ' ^', '   ^'],
        },
    ),
    toDisplay=OledDisplayMode.TXT,
    flip=True,
)
# oled
keyboard.extensions.append(oled)
# ledmap
rgb = Rgb_matrix(
    ledDisplay=[
        [255, 55, 55],
        [55, 55, 55],
        [55, 55, 55],
        [55, 55, 55],
        [55, 55, 55],
        [18, 209, 123],
        [255, 0, 0],
        [55, 55, 55],
        [55, 55, 55],
        [55, 55, 55],
        [55, 55, 55],
        [255, 55, 55],
        [255, 55, 55],
        [55, 55, 55],
        [0, 255, 217],
        [0, 255, 217],
        [0, 255, 217],
        [255, 0, 0],
        [0, 255, 217],
        [0, 255, 217],
        [0, 255, 217],
        [0, 255, 217],
        ]
    )
# ledmap
keyboard.extensions.append(rgb)

# TODO Comment one of these on each side
split_side = SplitSide.LEFT
# split_side = SplitSide.RIGHT
split = Split(data_pin=keyboard.rx, data_pin2=keyboard.tx, uart_flip=False)
keyboard.modules.append(split)

# Cleaner key names

_______ = KC.TRNS
XXXXXXX = KC.NO

LT1_SP = KC.LT(2, KC.SPC, prefer_hold=True, tap_time=250, repeat=HoldTapRepeat.TAP)
LT2_SP = KC.LT(3, KC.SPC, prefer_hold=True, tap_time=250, repeat=HoldTapRepeat.TAP)
TAB_SB = KC.LT(5, KC.TAB)
SUPER_L = KC.LM(4, KC.LGUI)

keyboard.keymap = [
    # DVORAK
    # ,-----------------------------------------.                    ,-----------------------------------------.
    # | Esc  |   '  |   ,  |   .  |   P  |   Y  |                    |   F  |   G  |   C  |   R  |   L  | BKSP |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # | Tab  |   A  |   O  |   E  |   U  |   I  |                    |   D  |   H  |   T  |   N  |   S  |  ENT |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # | Shft |   ;  |   Q  |   J  |   K  |   X  |-------.    ,-------|   B  |   M  |   W  |   V  |   Z  |   /  |
    # `-----------------------------------------/       /     \      \-----------------------------------------'
    #                          | LALT | LGUI | /LT1_SP /       \LT2_SP\  |  Ctl |  Up  |
    #                          |      |      |/       /         \      \ |      |      |
    #                          `---------------------'           '------''-------------'
    #
    [
        # DVORAK
        KC.ESC,   KC.QUOT, KC.COMM, KC.DOT,  KC.P,    KC.Y,                      KC.F,    KC.G,    KC.C,    KC.R,    KC.L,    KC.BSPC, \
        TAB_SB,   KC.A,    KC.O,    KC.E,    KC.U,    KC.I,                      KC.D,    KC.H,    KC.T,    KC.N,    KC.S,    KC.ENT, \
        OS_LSFT,  KC.SCLN, KC.Q,    KC.J,    KC.K,    KC.X,                      KC.B,    KC.M,    KC.W,    KC.V,    KC.Z,    KC.SLSH, \
                                        OS_LALT, SUPER_L, LT1_SP,   LT2_SP,  OS_LCTL, KC.NO,
    ],

    # GAMING
    # ,-----------------------------------------.                    ,-----------------------------------------.
    # | Tab  |   '  |   ,  |   .  |   P  |   Y  |                    |   F  |   G  |   C  |   R  |   L  | BKSP |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # | Ctl  |   A  |   O  |   E  |   U  |   I  |                    |   D  |   H  |   T  |   N  |   S  |  ENT |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # | Shft |   ;  |   Q  |   J  |   K  |   X  |-------.    ,-------|   B  |   M  |   W  |   V  |   Z  |   /  |
    # `-----------------------------------------/       /     \      \-----------------------------------------'
    #                          | LALT | LGUI | / Space /       \LT2_SP\  |  Ctl |  Up  |
    #                          |      |      |/       /         \      \ |      |      |
    #                          `---------------------'           '------''-------------'
    #
    [
        # GAMING
        KC.ESC,   KC.QUOT, KC.COMM, KC.DOT,  KC.P,    KC.Y,                     KC.F,    KC.G,    KC.C,    KC.R,    KC.L,    KC.BSPC, \
        KC.LCTL,  KC.A,    KC.O,    KC.E,    KC.U,    KC.I,                     KC.D,    KC.H,    KC.T,    KC.N,    KC.S,    KC.ENT, \
        KC.LSFT,  KC.SCLN, KC.Q,    KC.J,    KC.K,    KC.X,                     KC.B,    KC.M,    KC.W,    KC.V,    KC.Z,    KC.SLSH, \
                                            KC.LALT, KC.SPC,  KC.SPC,   LT2_SP,   KC.LCTL, KC.UP,
    ],
    # RAISE1
    # ,-----------------------------------------.                    ,-----------------------------------------.
    # |      |      |      |      |      |      |                    |      |      |   7  |  8   |  9   |      |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # |      |      |      |      |      |      |                    |      |      |   4  |  5   |  6   |   \  |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # |      |      |      |      |      |Reset |-------.    ,-------|      |      |   1  |  2   |  3   |   -  |
    # `-----------------------------------------/       /     \      \-----------------------------------------'
    #                          | LALT | LGUI | /LT1_SP /       \LT2_SP\  |   =  |  0   |
    #                          |      |      |/       /         \      \ |      |      |
    #                          `---------------------'           '------''-------------'
    #
    [
        # RAISE1
        KC.GRV,  _______, _______, _______, _______, _______,                   XXXXXXX, XXXXXXX, KC.N7,   KC.N8,   KC.N9,    KC.DEL,  \
        _______, _______, _______, _______, _______, _______,                   XXXXXXX, XXXXXXX, KC.N4,   KC.N5,   KC.N6,    KC.BSLS, \
        _______, _______, _______, _______, _______, KC.RLD,                    XXXXXXX, XXXXXXX, KC.N1,   KC.N2,   KC.N3,    KC.MINS, \
                                            _______, _______, _______, _______, KC.EQL,  KC.N0,
    ],
    # RAISE2
    # ,-----------------------------------------.                    ,-----------------------------------------.
    # |      |  F9  |  F10 |  F11 |  F12 |      |                    |      |      |      |      |      | SIns |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # |      |  F5  |  F6  |  F7  |  F8  |      |                    |      | Left | Down |  Up  |Right |      |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # |      |  F1  |  F2  |  F3  |  F4  |      |-------.    ,-------|      |      |      |      |      |   \  |
    # `-----------------------------------------/       /     \      \-----------------------------------------'
    #                          | LALT | LGUI | /LT1_SP /       \LT2_SP\  |Dvorak|Gaming|
    #                          |      |      |/       /         \      \ |      |      |
    #                          `---------------------'           '------''-------------'
    #

    [
        # RAISE2
        _______, KC.F9,   KC.F10,  KC.F11,  KC.F12,  _______,                     _______, _______, _______, KC.LBRC, KC.RBRC, KC.LSHIFT(KC.INS), \
        _______, KC.F5,   KC.F6,   KC.F7,   KC.F8,   _______,                     KC.HOME, KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT, KC.END,  \
        _______, KC.F1,   KC.F2,   KC.F3,   KC.F4,   _______,                     _______, _______, _______, _______, _______, KC.BSLS, \
                                            _______, _______,  _______, _______,  KC.DF(0),   KC.DF(1),
    ],
    # GUI
    # ,-----------------------------------------.                    ,-----------------------------------------.
    # |      |  1   |   2  |   3  |   4  |  5   |                    |      |      |      |      |      |      |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # |      |  6   |   7  |   8  |   9  |  0   |                    |      |      |      |      |      |      |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # |      |      |      |      |      |      |-------.    ,-------|      |      |      |      |      |      |
    # `-----------------------------------------/       /     \      \-----------------------------------------'
    #                          | LALT | LGUI | /LT1_SP /       \LT2_SP\  |      |      |
    #                          |      |      |/       /         \      \ |      |      |
    #                          `---------------------'           '------''-------------'

    [
        # GUI
        _______, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                       _______, _______, _______, _______, _______, _______, \
        _______, KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,                       _______, _______, _______, _______, _______, _______, \
        _______, _______, _______, _______, _______, _______,                     _______, _______, _______, _______, _______, _______, \

                                            _______, _______,  _______, _______,  _______, _______ \
    ],
     # SYMBOLS
     # ,-----------------------------------------.                    ,-----------------------------------------.
     # |      |  !   |   @  |   #  |   $  |  %   |                    |   ^  |   &  |   *  |   (  |  )   | Del  |
     # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
     # |      |      |      |      |      |      |                    |      |      |      |   [  |  ]   |      |
     # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
     # |      |      |      |      |      |      |-------.    ,-------|      |      |      |      |      |      |
     # `-----------------------------------------/       /     \      \-----------------------------------------'
     #                          | LALT | LGUI | /LT1_SP /       \LT2_SP\  |      |      |
     #                          |      |      |/       /         \      \ |      |      |
     #                          `---------------------'           '------''-------------'
     #
    [
        # SYMBOLS
        _______, KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC,                     KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.DEL, \
        _______, _______, _______, _______, _______, _______,                     _______, _______, _______, KC.LBRC, KC.RBRC, _______, \
        _______, _______, _______, _______, _______, _______,                     _______, _______, _______, _______, _______, _______, \
                                            _______, _______,  _______, _______,  _______, _______,
    ]

]

combos.combos = [
    Chord((KC.QUOT, KC.COMM), send_string('>_>')),
    Chord((KC.COMM, KC.DOT), send_string('><')),
    Chord((KC.C, KC.L), send_string("C'est la vie")),
    Chord((KC.BKSP, KC.L), KC.LCTL(KC.BKSP)),
    Chord((KC.R, KC.L), KC.LCTL(KC.V)),
    Chord((KC.V, KC.Z), KC.LCTL(KC.Z)),

]


if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.USB)
