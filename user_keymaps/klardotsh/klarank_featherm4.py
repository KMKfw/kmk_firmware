from kb import KMKKeyboard

from kmk.consts import UnicodeMode
from kmk.handlers.sequences import compile_unicode_string_sequences as cuss
from kmk.handlers.sequences import send_string
from kmk.keys import KC, make_key
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()
layers = Layers()
keyboard.modules = [layers]

keyboard.debug_enabled = False
keyboard.unicode_mode = UnicodeMode.LINUX
keyboard.tap_time = 750

emoticons = cuss(
    {
        # Emojis
        'BEER': r'🍺',
        'BEER_TOAST': r'🍻',
        'FACE_CUTE_SMILE': r'😊',
        'FACE_HEART_EYES': r'😍',
        'FACE_JOY': r'😂',
        'FACE_SWEAT_SMILE': r'😅',
        'FACE_THINKING': r'🤔',
        'FIRE': r'🔥',
        'FLAG_CA': r'🇨🇦',
        'FLAG_US': r'🇺🇸',
        'HAND_CLAP': r'👏',
        'HAND_HORNS': r'🤘',
        'HAND_OK': r'👌',
        'HAND_THUMB_DOWN': r'👎',
        'HAND_THUMB_UP': r'👍',
        'HAND_WAVE': r'👋',
        'HEART': r'❤️',
        'MAPLE_LEAF': r'🍁',
        'POOP': r'💩',
        'TADA': r'🎉',
        # Emoticons, but fancier
        'ANGRY_TABLE_FLIP': r'(ノಠ痊ಠ)ノ彡┻━┻',
        'CELEBRATORY_GLITTER': r'+｡:.ﾟヽ(´∀｡)ﾉﾟ.:｡+ﾟﾟ+｡:.ﾟヽ(*´∀)ﾉﾟ.:｡+ﾟ',
        'SHRUGGIE': r'¯\_(ツ)_/¯',
        'TABLE_FLIP': r'(╯°□°）╯︵ ┻━┻',
    }
)

WPM = send_string(
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Bibendum arcu vitae elementum curabitur vitae nunc sed. Facilisis sed odio morbi quis.'
)

_______ = KC.TRNS
xxxxxxx = KC.NO
HELLA_TD = KC.TD(
    KC.A,
    KC.B,
    send_string('macros in a tap dance? I think yes'),
    KC.TG(1),
)


def shrek_is_life(*args, **kwargs):
    '''
    Proof macros are a thing and don't actually have to care about the state. At all.
    '''

    print('⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆')
    print('⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿')
    print('⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀')
    print('⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀')
    print('⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠛⠉')


# Spew shrek when hitting a fully custom key
# This won't modify internal state at all
SHREK_IS_LOVE = make_key(on_press=shrek_is_life)

# Also spew shrek every time I try to use Alt. It's a dev board, after all.
KC.LALT.before_press_handler(shrek_is_life)

# But also give me a normal alt if I want it. Shrek isn't ALWAYS life.
BORING_ALT = KC.LALT.clone()

# fmt:off
keyboard.keymap = [
    [
        KC.GESC, KC.QUOT, KC.COMM,            KC.DOT,   KC.P,     KC.Y,    KC.F,    KC.G,     KC.C,    KC.R,    KC.L,  KC.BSPC,
        KC.TAB,  KC.A,    KC.O,               KC.E,     KC.U,     KC.I,    KC.D,    KC.H,     KC.T,    KC.N,    KC.S,  KC.ENT,
        KC.LGUI, KC.SCLN, KC.Q,               KC.J,     KC.K,     KC.X,    KC.B,    KC.M,     KC.W,    KC.V,    KC.Z,  KC.LALT,
        KC.LCTL, KC.NO,   KC.LSHIFT(KC.LGUI), KC.MO(2), KC.MO(3), KC.LSFT, KC.SPC,  KC.MO(1), KC.LEFT, KC.DOWN, KC.UP, KC.RGHT,
    ],

    [
        KC.GESC, xxxxxxx, xxxxxxx, KC.F10, KC.F11, KC.F12, xxxxxxx, KC.PSLS, KC.N7, KC.N8,  KC.N9,   KC.BSPC,
        KC.TAB,  xxxxxxx, xxxxxxx, KC.F7,  KC.F8,  KC.F9,  xxxxxxx, KC.PAST, KC.N4, KC.N5,  KC.N6,   _______,
        KC.LGUI, xxxxxxx, xxxxxxx, KC.F4,  KC.F5,  KC.F6,  xxxxxxx, KC.PMNS, KC.N1, KC.N2,  KC.N3,   _______,
        KC.LCTL, xxxxxxx, _______, KC.F1,  KC.F2,  KC.F3,  KC.SPC,  _______, KC.N0, KC.DOT, xxxxxxx, KC.EQL,
    ],

    [
        KC.GESC, SHREK_IS_LOVE, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.BSLS, KC.LBRC, KC.RBRC, KC.DEL,
        KC.TAB,  xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.MINS,
        KC.LGUI, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.LBRC, xxxxxxx, xxxxxxx, KC.INS,
        KC.LCTL, xxxxxxx, _______, _______, xxxxxxx, _______, xxxxxxx, xxxxxxx, KC.HOME, KC.PGDN, KC.PGUP, KC.END,
    ],

    [
        KC.GRV,  KC.EXLM, KC.AT,    KC.HASH, KC.DLR,  KC.PERC, KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.SLSH,
        KC.TAB,  xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.MINS,
        KC.LGUI, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, BORING_ALT,
        KC.LCTL, KC.DBG,  HELLA_TD, xxxxxxx, _______, _______, xxxxxxx, xxxxxxx, KC.MUTE, KC.VOLD, KC.VOLU, xxxxxxx,
    ],
]
# fmt:on

if __name__ == '__main__':
    keyboard.go()
