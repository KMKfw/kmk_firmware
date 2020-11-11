from kb import KMKKeyboard
from kmk.consts import LeaderMode, UnicodeMode
from kmk.extensions.ble_split import BLE_Split
from kmk.extensions.layers import Layers
from kmk.extensions.rgb import RGB
from kmk.handlers.sequences import compile_unicode_string_sequences as cuss
from kmk.handlers.sequences import send_string
from kmk.keys import KC

keyboard = KMKKeyboard()

keyboard.debug_enabled = False
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
    'SHRUG_EMOJI': r'🤷',

    # Emoticons, but fancier
    'ANGRY_TABLE_FLIP': r'(ノಠ痊ಠ)ノ彡┻━┻',
    'CELEBRATORY_GLITTER': r'+｡:.ﾟヽ(´∀｡)ﾉﾟ.:｡+ﾟﾟ+｡:.ﾟヽ(*´∀)ﾉﾟ.:｡+ﾟ',
    'SHRUGGIE': r'¯\_(ツ)_/¯',
    'TABLE_FLIP': r'(╯°□°）╯︵ ┻━┻',
})

WPM = send_string('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Bibendum arcu vitae elementum curabitur vitae nunc sed. Facilisis sed odio morbi quis.')

keyboard.leader_mode = LeaderMode.ENTER
keyboard.leader_dictionary = {
    'hello': send_string('hello world from kmk macros'),
    'wpm': WPM,
    'atf': emoticons.ANGRY_TABLE_FLIP,
    'tf': emoticons.TABLE_FLIP,
    'fca': emoticons.FLAG_CA,
    'fus': emoticons.FLAG_US,
    'cel': emoticons.CELEBRATORY_GLITTER,
    'shr': emoticons.SHRUGGIE,
    'shre': emoticons.SHRUG_EMOJI,
    'poop': emoticons.POOP,
    'joy': emoticons.FACE_JOY,
    'ls': KC.LGUI(KC.HOME),  # Lock screen
    'cw': KC.LGUI(KC.END),  # Close window
    'dbg': KC.DBG,
}

_______ = KC.TRNS
xxxxxxx = KC.NO
HELLA_TD = KC.TD(
    KC.A,
    KC.B,
    send_string('macros in a tap dance? I think yes'),
    KC.TG(1),
)

rgb_ext = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=keyboard.rgb_num_pixels)
layers_ext = Layers()
#
# TODO Comment one of these on each side
# Left is 0, Right is 1
split_side = 0
split_side = 1
split = BLE_Split(split_side=split_side)

extensions = [rgb_ext, split, layers_ext]


keyboard.keymap = [
    [
        KC.GESC, KC.N1,   KC.N2,   KC.N3,  KC.N4, KC.N5,                     KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.BSPC,
        KC.TAB,  KC.QUOT, KC.COMM, KC.DOT, KC.P,  KC.Y,                      KC.F,  KC.G,  KC.C,  KC.R,  KC.L,  KC.SLSH,
        KC.LGUI, KC.A,    KC.O,    KC.E,   KC.U,  KC.I,                      KC.D,  KC.H,  KC.T,  KC.N,  KC.S,  KC.ENTER,
        KC.LCTL, KC.SCLN, KC.Q,    KC.J,   KC.K,  KC.X,  KC.MO(2), KC.MO(1), KC.B,  KC.M,  KC.W,  KC.V,  KC.Z,  KC.LALT,
                                    KC.LEFT, KC.RGHT,    KC.LSFT,  KC.SPC,     KC.UP, KC.DOWN,
    ],
    [
        _______, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,                   KC.F10, KC.F11, KC.F12, xxxxxxx, xxxxxxx, _______,
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,                   KC.F7,  KC.F8,  KC.F9,  xxxxxxx, xxxxxxx, KC.EQUAL,
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.INS,                    KC.F4,  KC.F5,  KC.F6,  xxxxxxx, xxxxxxx, xxxxxxx,
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.LEAD, _______, KC.F1,  KC.F2,  KC.F3,  xxxxxxx, xxxxxxx, _______,
                                      KC.HOME, KC.END,        _______, xxxxxxx,    KC.PGUP, KC.PGDN,
    ],
    [
        KC.MUTE, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx,                   xxxxxxx, xxxxxxx, xxxxxxx, KC.LBRC,  KC.RBRC, KC.DEL,
        xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx,                   xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, KC.BSLS,
        KC.RGUI, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx,                   xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, KC.MINS,
        xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, xxxxxxx, xxxxxxx, _______, KC.VOLU, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,  xxxxxxx, KC.RALT,
                                      KC.HOME, KC.END,         _______, KC.VOLD,    KC.PGUP, KC.PGDN,
    ],
]

if __name__ == '__main__':
    keyboard.go()
