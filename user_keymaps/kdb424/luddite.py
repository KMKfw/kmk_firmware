from kmk.boards.converter.fourtypercentclub.luddite import Firmware
from kmk.consts import LeaderMode, UnicodeMode
from kmk.handlers.sequences import compile_unicode_string_sequences
from kmk.keys import KC, make_key

keyboard = Firmware()

# ---------------------------------- Config  --------------------------------------------

keyboard.leader_mode = LeaderMode.ENTER
keyboard.unicode_mode = UnicodeMode.LINUX
keyboard.tap_time = 150
keyboard.leader_timeout = 999999999999
keyboard.rgb_num_pixels = 16
keyboard.rgb_hue_default = 260
keyboard.rgb_sat_default = 100
keyboard.rgb_val_default = 20
keyboard.rgb_knight_effect_length = 6
keyboard.rgb_animation_mode = 'static'
keyboard.rgb_animation_speed = 3
keyboard.debug_enabled = True


# ---------------------- Custom Functions --------------------------------------------


def portal_lights(*args, **kwargs):
    keyboard.pixels.disable_auto_write = True
    keyboard.pixels.rgb_animation_mode = 'User'
    for i in range(0, 9):
        keyboard.pixels.set_hsv(21, 100, 100, i)
    for i in range(10, 16):
        keyboard.pixels.set_hsv(220, 100, 100, i)
    keyboard.pixels.show()


def portal_off(*args, **kwargs):
    keyboard.pixels.disable_auto_write = False
    keyboard.pixels.off()
    keyboard.pixels.rgb_animation_mode = 'static'

# ---------------------- Custom Keys --------------------------------------------


LON = make_key(on_press=portal_lights)
LOFF = make_key(on_press=portal_off)

_______ = KC.TRNS
XXXXXXX = KC.NO
HOME = KC.MT(KC.HOME, KC.LSFT)
END = KC.MT(KC.END, KC.RSFT)


BASE = 0
FN1 = 1

# ---------------------- Leader Key Macros --------------------------------------------

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


keyboard.leader_dictionary = {
    'flip': emoticons.ANGRY_TABLE_FLIP,
    'cheer': emoticons.CHEER,
    'wat': emoticons.WAT,
    'ff': emoticons.FF,
    'f': emoticons.F,
    'meh': emoticons.MEH,
    'yay': emoticons.YAY,
    'p': LON,
    'po': LOFF,

}
# ---------------------- Keymap ---------------------------------------------------------


keyboard.keymap = [
    [
        [KC.GESC, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7],
        [KC.N8,   KC.N9,   KC.N0,   KC.LBRC, KC.RBRC, KC.BSPC, KC.LEAD, KC.QUOT],
        [KC.COMM, KC.DOT,  KC.P,    KC.Y,    KC.F,    KC.G,    KC.C,    KC.R],
        [KC.L,    KC.SLSH, KC.EQL,  KC.BSLS, KC.TAB,  KC.A,    KC.O,    KC.E],
        [KC.U,    KC.I,    KC.D,    KC.H,    KC.T,    KC.N,    KC.S,    KC.MINS],
        [KC.ENT,  KC.LSFT, KC.SCLN, KC.Q,    KC.J,    KC.K,    KC.X,    KC.B],
        [KC.M,    KC.W,    KC.V,    KC.Z,    KC.RSFT, KC.LCTL, KC.LGUI, KC.MO(FN1)],
        [KC.SPC,  KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT],
    ],

    [
        [KC.GESC, KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.F7],
        [KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.DEL,  KC.RGB_TOG, _______],
        [_______, _______, _______, _______, _______, _______, _______, _______],
        [_______, _______, KC.VOLU, _______, _______, _______, _______, _______],
        [_______, _______, _______, _______, _______, _______, _______, KC.VOLD],
        [_______, _______, _______, _______, _______, _______, _______, _______],
        [_______, _______, _______, _______, _______, KC.RGB_M_K,  _______, _______],
        [_______, KC.LALT, KC.RGB_M_S, LON,     LOFF],
    ],
]

if __name__ == '__main__':
    keyboard.go()
