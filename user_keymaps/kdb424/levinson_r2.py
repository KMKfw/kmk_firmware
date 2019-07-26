from kmk.boards.converter.keebio.levinson_r2 import KMKKeyboard
from kmk.consts import LeaderMode, UnicodeMode
from kmk.handlers.sequences import compile_unicode_string_sequences
from kmk.keys import KC

keyboard = KMKKeyboard()

# ------------------User level config variables ---------------------------------------
keyboard.leader_mode = LeaderMode.TIMEOUT
keyboard.unicode_mode = UnicodeMode.LINUX
keyboard.tap_time = 150
keyboard.leader_timeout = 2000
keyboard.debug_enabled = True

keyboard.rgb_config['num_pixels'] = 16
keyboard.rgb_config['val_limit'] = 150
keyboard.rgb_config['hue_step'] = 10
keyboard.rgb_config['sat_step'] = 5
keyboard.rgb_config['val_step'] = 5
keyboard.rgb_config['hue_default'] = 260
keyboard.rgb_config['sat_default'] = 100
keyboard.rgb_config['val_default'] = 20
keyboard.rgb_config['knight_effect_length'] = 6
keyboard.rgb_config['animation_mode'] = 'swirl'
keyboard.rgb_config['animation_speed'] = 2
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

# ---------------------- Keymap ---------------------------------------------------------

keyboard.keymap = [
    [
        # default
        KC.GESC, KC.QUOTE, KC.COMMA, KC.DOT, KC.P, KC.Y, KC.F, KC.G, KC.C, KC.R, KC.L, KC.BKSP,
        KC.TAB, KC.A, KC.O, KC.E, KC.U, KC.I, KC.D, KC.H, KC.T, KC.N, KC.S, KC.ENT,
        KC.LSFT, KC.SCLN, KC.Q, KC.J, KC.K, KC.X, KC.B, KC.M, KC.W, KC.V, KC.Z, KC.SLSH,
        KC.LCTRL, KC.LGUI, KC.LALT, KC.RGB_TOG, KC.MO(2), KC.LT(3, KC.SPC), KC.LT(3, KC.SPC), KC.MO(4), KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT,
    ],
    [
        # Gaming
        KC.TAB, KC.QUOT, KC.COMM, KC.DOT, KC.P, KC.Y, KC.F, KC.G, KC.C, KC.R, KC.L, KC.BKSP,
        KC.ESC, KC.A, KC.O, KC.E, KC.U, KC.I, KC.D, KC.H, KC.T, KC.N, KC.S, KC.ENT,
        KC.LSFT, KC.SCLN, KC.Q, KC.J, KC.K, KC.X, KC.B, KC.M, KC.W, KC.V, KC.Z, KC.SLSH,
        KC.LCTRL, KC.LGUI, KC.LALT, KC.F1, KC.F2, KC.SPC, KC.SPC, KC.MO(4), KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT,
    ],
    [
        # Raise1
        KC.TILD, KC.EXLM, KC.AT, KC.HASH, KC.DLR, KC.PERC, KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.DEL,
        KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.LBRC, KC.RBRC, KC.BSLS,
        KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.INS, KC.PGDN, KC.PGUP, KC.MINS,
        KC.RESET, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.NO, KC.NO, KC.EQL, KC.HOME, KC.VOLD, KC.VOLU, KC.END,
    ],
    [
        # Raise2
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.N7, KC.N8, KC.N9, KC.BKSP,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.N4, KC.N5, KC.N6, KC.NO,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.N1, KC.N2, KC.N3, KC.NO,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.N0, KC.N0, KC.PDOT, KC.ENT,
    ],
    [
        # Raise3
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F10, KC.F11, KC.F12, KC.LSHIFT(KC.INS),
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F7, KC.F8, KC.F9, KC.NO,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F4, KC.F5, KC.F6, KC.NO,
        KC.DF(0), KC.DF(1), KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.F1, KC.F2, KC.F3, KC.NO,
    ],
]

if __name__ == '__main__':
    keyboard.go()
