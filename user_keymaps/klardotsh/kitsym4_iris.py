from kmk.boards.kitsym4_iris import Firmware
from kmk.consts import LeaderMode, UnicodeMode
from kmk.keycodes import KC
from kmk.keycodes import generate_leader_dictionary_seq as glds
from kmk.macros.simple import send_string
from kmk.macros.unicode import compile_unicode_string_sequences as cuss

keyboard = Firmware()

keyboard.debug_enabled = True
keyboard.unicode_mode = UnicodeMode.LINUX
keyboard.tap_time = 750

emoticons = cuss({
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
})

WPM = send_string("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Bibendum arcu vitae elementum curabitur vitae nunc sed. Facilisis sed odio morbi quis.")

keyboard.leader_mode = LeaderMode.TIMEOUT
keyboard.leader_dictionary = {
    glds('hello'): send_string('hello world from kmk macros'),
    glds('wpm'): WPM,
    glds('atf'): emoticons.ANGRY_TABLE_FLIP,
    glds('tf'): emoticons.TABLE_FLIP,
    glds('fca'): emoticons.FLAG_CA,
    glds('fus'): emoticons.FLAG_US,
    glds('cel'): emoticons.CELEBRATORY_GLITTER,
}

_______ = KC.TRNS
xxxxxxx = KC.NO
HELLA_TD = KC.TD(
    KC.A,
    KC.B,
    send_string('macros in a tap dance? I think yes'),
    KC.TG(1),
)


keyboard.keymap = [
    [
        [KC.GESC, KC.N1,   KC.N2,    KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,    KC.N0,   KC.BSPC],
        [KC.TAB,  KC.QUOT, KC.COMM,  KC.DOT,  KC.P,    KC.Y,    KC.F,    KC.G,    KC.C,    KC.R,     KC.L,    KC.SLSH],
        [KC.LGUI, KC.A,    KC.O,     KC.E,    KC.U,    KC.I,    KC.D,    KC.H,    KC.T,    KC.N,     KC.S,    KC.ENTER],
        [KC.LCTL, KC.SCLN, KC.Q,     KC.J,    KC.K,    KC.X,    KC.B,    KC.M,    KC.W,    KC.V,     KC.Z,    KC.LALT],
        [xxxxxxx, xxxxxxx, KC.MO(2), KC.LEFT, KC.RGHT, KC.LSFT, KC.SPC,  KC.UP,   KC.DOWN, KC.MO(1), xxxxxxx, xxxxxxx],
    ],
    [
        [_______, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx, KC.F10,  KC.F11,  KC.F12,  xxxxxxx,  xxxxxxx, _______],
        [xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx, KC.F7,   KC.F8,   KC.F9,   xxxxxxx,  xxxxxxx, KC.EQUAL],
        [xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, KC.INS,  KC.F4,   KC.F5,   KC.F6,   xxxxxxx,  xxxxxxx, xxxxxxx],
        [xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx, KC.F1,   KC.F2,   KC.F3,   xxxxxxx,  xxxxxxx, _______],
        [xxxxxxx, xxxxxxx, xxxxxxx,  KC.HOME, KC.END,  _______, xxxxxxx, KC.PGUP, KC.PGDN, _______,  xxxxxxx, xxxxxxx],
    ],
    [
        [KC.MUTE, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.LBRC,  KC.RBRC, KC.DEL],
        [xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, KC.BSLS],
        [KC.RGUI, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, KC.MINS],
        [xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, KC.RALT],
        [xxxxxxx, xxxxxxx, _______,  KC.HOME, KC.END,  _______, KC.VOLD, KC.PGUP, KC.PGDN, KC.VOLU,  xxxxxxx, xxxxxxx],
    ],
]

if __name__ == '__main__':
    keyboard.go()
