from kmk.boards.handwire_ghirkin import KMKKeyboard
from kmk.consts import UnicodeMode
from kmk.handlers.sequences import compile_unicode_string_sequences
from kmk.keys import KC

keyboard = KMKKeyboard()

# ------------------User level config variables ---------------------------------------
keyboard.unicode_mode = UnicodeMode.LINUX
keyboard.tap_time = 150
keyboard.leader_timeout = 2000
keyboard.debug_enabled = False

emoticons = compile_unicode_string_sequences({
    # Emoticons, but fancier
    'ANGRY_TABLE_FLIP': r'(ノಠ痊ಠ)ノ彡┻━┻',
    'CHEER': r'+｡:.ﾟヽ(´∀｡)ﾉﾟ.:｡+ﾟﾟ+｡:.ﾟヽ(*´∀)ﾉﾟ.:｡+ﾟ',
    'TABLE_FLIP': r'(╯°□°）╯︵ ┻━┻',
    'WAT': r'⊙.☉',
    'FF': r'凸(ﾟДﾟ#)',
    'F': r'（￣^￣）凸',
    'MEH': r'╮(￣_￣)╭',
    'YAY': r'o(^▽^)o',
})

# ---------------------- Leader Key Macros --------------------------------------------

keyboard.leader_dictionary = {
    'flip': emoticons.ANGRY_TABLE_FLIP,
    'cheer': emoticons.CHEER,
    'wat': emoticons.WAT,
    'ff': emoticons.FF,
    'f': emoticons.F,
    'meh': emoticons.MEH,
    'yay': emoticons.YAY,
}


# Custom Keys
_______ = KC.TRNS
XXXXXXX = KC.NO

LT1_X = KC.LT(1, KC.X)
SHFT_SCLN = KC.MT(KC.SCLN, KC.LSFT)
# BSPC = KC.TD(
#        KC.SPC,
#        KC.B,
# )
# ---------------------- Keymap ---------------------------------------------------------

keyboard.keymap = [
    # Layer 0
    [
        KC.QUOTE,  KC.COMMA,  KC.DOT,  KC.P,    KC.Y,    KC.F,    KC.G,    KC.C,    KC.R,    KC.L,
        KC.A,      KC.O,      KC.E,    KC.U,    KC.I,    KC.D,    KC.H,    KC.T,    KC.N,    KC.S,
        SHFT_SCLN, KC.Q,      KC.J,    KC.K,    LT1_X,   KC.SPC,  KC.M,    KC.W,    KC.V,   KC.Z,
    ],
    # Layer 1
    [
        KC.GESC,   KC.COMMA,  KC.DOT,  KC.P,    KC.Y,    KC.F,    KC.G,    KC.C,    KC.N0,   KC.BKSP,
        KC.N1,     KC.N2,     KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.ENT,
        SHFT_SCLN, KC.LGUI,   KC.J,    KC.K,    _______, KC.B,    KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT,
    ],
]

if __name__ == '__main__':
    keyboard.go()
