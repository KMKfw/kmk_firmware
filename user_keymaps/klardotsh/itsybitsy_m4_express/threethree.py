from kmk.consts import DiodeOrientation, UnicodeModes
from kmk.entrypoints.handwire.circuitpython_samd51 import main
from kmk.firmware import Firmware
from kmk.keycodes import KC
from kmk.macros.rotary_encoder import VolumeRotaryEncoder
from kmk.macros.simple import send_string, simple_key_sequence
from kmk.macros.unicode import unicode_string_sequence
from kmk.pins import Pin as P
from kmk.types import AttrDict

DEBUG_ENABLE = True

cols = (P.A4, P.A5, P.D7)
rows = (P.D12, P.D11, P.D10)

diode_orientation = DiodeOrientation.COLUMNS
unicode_mode = UnicodeModes.LINUX

encoders = [
    VolumeRotaryEncoder(P.A3, P.A2, 6, 0.6),
]

emoticons = AttrDict({
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

for k, v in emoticons.items():
    emoticons[k] = unicode_string_sequence(v)

MACRO_HELLO_WORLD = simple_key_sequence([
    KC.LSHIFT(KC.H),
    KC.E,
    KC.L,
    KC.L,
    KC.O,

    KC.SPACE,

    KC.MACRO_SLEEP_MS(500),

    KC.LSHIFT(KC.K),
    KC.LSHIFT(KC.M),
    KC.LSHIFT(KC.K),
    KC.EXCLAIM,
])

keymap = [
    [
        [KC.GESC,              KC.HYPR,     KC.RESET],
        [KC.MO(1),             KC.B,     KC.MUTE],
        [KC.LT(2, KC.EXCLAIM), KC.HASH,  KC.ENTER],
    ],
    [
        [KC.MUTE, KC.B, KC.C],
        [KC.TRNS,   KC.D, KC.E],
        [KC.F,    KC.G, KC.H],
    ],
    [
        [emoticons.CELEBRATORY_GLITTER, emoticons.SHRUGGIE, emoticons.ANGRY_TABLE_FLIP],
        [emoticons.BEER,                emoticons.FLAG_CA,  emoticons.FLAG_US],
        [KC.TRNS,                       KC.P,               MACRO_HELLO_WORLD],
    ],
]

if __name__ == '__main__':
    main()
