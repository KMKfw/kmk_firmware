import gc
from micropython import const

import kmk.handlers.stock as handlers
from kmk.consts import UnicodeMode
from kmk.key_validators import (
    key_seq_sleep_validator,
    tap_dance_key_validator,
    unicode_mode_key_validator,
)
from kmk.types import AttrDict, UnicodeModeKeyMeta

FIRST_KMK_INTERNAL_KEY = const(1000)
NEXT_AVAILABLE_KEY = 1000

KEY_SIMPLE = const(0)
KEY_MODIFIER = const(1)
KEY_CONSUMER = const(2)


class KeyAttrDict(AttrDict):
    def __getattr__(self, key):
        try:
            return super(KeyAttrDict, self).__getattr__(key)
        except Exception:
            pass
        # Modifiers
        if key in ('LEFT_CONTROL', 'LCTRL', 'LCTL'):
            make_mod_key(code=0x01, names=('LEFT_CONTROL', 'LCTRL', 'LCTL'))
        elif key in ('LEFT_SHIFT', 'LSHIFT', 'LSFT'):
            make_mod_key(code=0x02, names=('LEFT_SHIFT', 'LSHIFT', 'LSFT'))
        elif key in ('LEFT_ALT', 'LALT'):
            make_mod_key(code=0x04, names=('LEFT_ALT', 'LALT'))
        elif key in ('LEFT_SUPER', 'LGUI', 'LCMD', 'LWIN'):
            make_mod_key(code=0x08, names=('LEFT_SUPER', 'LGUI', 'LCMD', 'LWIN'))
        elif key in ('RIGHT_CONTROL', 'RCTRL', 'RCTL'):
            make_mod_key(code=0x10, names=('RIGHT_CONTROL', 'RCTRL', 'RCTL'))
        elif key in ('RIGHT_SHIFT', 'RSHIFT', 'RSFT'):
            make_mod_key(code=0x20, names=('RIGHT_SHIFT', 'RSHIFT', 'RSFT'))
        elif key in ('RIGHT_ALT', 'RALT'):
            make_mod_key(code=0x40, names=('RIGHT_ALT', 'RALT'))
        elif key in ('RIGHT_SUPER', 'RGUI', 'RCMD', 'RWIN'):
            make_mod_key(code=0x80, names=('RIGHT_SUPER', 'RGUI', 'RCMD', 'RWIN'))
        # MEH = LCTL | LALT | LSFT# MEH = LCTL |
        elif key in ('MEH',):
            make_mod_key(code=0x07, names=('MEH',))
        # HYPR = LCTL | LALT | LSFT | LGUI
        elif key in ('HYPER', 'HYPR'):
            make_mod_key(code=0x0F, names=('HYPER', 'HYPR'))

        # Basic ASCII letters
        elif key in ('A',):
            make_key(code=4, names=('A',))
        elif key in ('B',):
            make_key(code=5, names=('B',))
        elif key in ('C',):
            make_key(code=6, names=('C',))
        elif key in ('D',):
            make_key(code=7, names=('D',))
        elif key in ('E',):
            make_key(code=8, names=('E',))
        elif key in ('F',):
            make_key(code=9, names=('F',))
        elif key in ('G',):
            make_key(code=10, names=('G',))
        elif key in ('H',):
            make_key(code=11, names=('H',))
        elif key in ('I',):
            make_key(code=12, names=('I',))
        elif key in ('J',):
            make_key(code=13, names=('J',))
        elif key in ('K',):
            make_key(code=14, names=('K',))
        elif key in ('L',):
            make_key(code=15, names=('L',))
        elif key in ('M',):
            make_key(code=16, names=('M',))
        elif key in ('N',):
            make_key(code=17, names=('N',))
        elif key in ('O',):
            make_key(code=18, names=('O',))
        elif key in ('P',):
            make_key(code=19, names=('P',))
        elif key in ('Q',):
            make_key(code=20, names=('Q',))
        elif key in ('R',):
            make_key(code=21, names=('R',))
        elif key in ('S',):
            make_key(code=22, names=('S',))
        elif key in ('T',):
            make_key(code=23, names=('T',))
        elif key in ('U',):
            make_key(code=24, names=('U',))
        elif key in ('V',):
            make_key(code=25, names=('V',))
        elif key in ('W',):
            make_key(code=26, names=('W',))
        elif key in ('X',):
            make_key(code=27, names=('X',))
        elif key in ('Y',):
            make_key(code=28, names=('Y',))
        elif key in ('Z',):
            make_key(code=29, names=('Z',))

        # Numbers
        # Aliases to play nicely with AttrDict, since KC.1 isn't a valid
        # attribute key in Python, but KC.N1 is
        elif key in ('1', 'N1'):
            make_key(code=30, names=('1', 'N1'))
        elif key in ('2', 'N2'):
            make_key(code=31, names=('2', 'N2'))
        elif key in ('3', 'N3'):
            make_key(code=32, names=('3', 'N3'))
        elif key in ('4', 'N4'):
            make_key(code=33, names=('4', 'N4'))
        elif key in ('5', 'N5'):
            make_key(code=34, names=('5', 'N5'))
        elif key in ('6', 'N6'):
            make_key(code=35, names=('6', 'N6'))
        elif key in ('7', 'N7'):
            make_key(code=36, names=('7', 'N7'))
        elif key in ('8', 'N8'):
            make_key(code=37, names=('8', 'N8'))
        elif key in ('9', 'N9'):
            make_key(code=38, names=('9', 'N9'))
        elif key in ('0', 'N0'):
            make_key(code=39, names=('0', 'N0'))

        # More ASCII standard keys
        elif key in ('ENTER', 'ENT', '\n'):
            make_key(code=40, names=('ENTER', 'ENT', '\n'))
        elif key in ('ESCAPE', 'ESC'):
            make_key(code=41, names=('ESCAPE', 'ESC'))
        elif key in ('BACKSPACE', 'BSPC', 'BKSP'):
            make_key(code=42, names=('BACKSPACE', 'BSPC', 'BKSP'))
        elif key in ('TAB', '\t'):
            make_key(code=43, names=('TAB', '\t'))
        elif key in ('SPACE', 'SPC', ' '):
            make_key(code=44, names=('SPACE', 'SPC', ' '))
        elif key in ('MINUS', 'MINS', '-'):
            make_key(code=45, names=('MINUS', 'MINS', '-'))
        elif key in ('EQUAL', 'EQL', '='):
            make_key(code=46, names=('EQUAL', 'EQL', '='))
        elif key in ('LBRACKET', 'LBRC', '['):
            make_key(code=47, names=('LBRACKET', 'LBRC', '['))
        elif key in ('RBRACKET', 'RBRC', ']'):
            make_key(code=48, names=('RBRACKET', 'RBRC', ']'))
        elif key in ('BACKSLASH', 'BSLASH', 'BSLS', '\\'):
            make_key(code=49, names=('BACKSLASH', 'BSLASH', 'BSLS', '\\'))
        elif key in ('SEMICOLON', 'SCOLON', 'SCLN', ';'):
            make_key(code=51, names=('SEMICOLON', 'SCOLON', 'SCLN', ';'))
        elif key in ('QUOTE', 'QUOT', "'"):
            make_key(code=52, names=('QUOTE', 'QUOT', "'"))
        elif key in ('GRAVE', 'GRV', 'ZKHK', '`'):
            make_key(code=53, names=('GRAVE', 'GRV', 'ZKHK', '`'))
        elif key in ('COMMA', 'COMM', ','):
            make_key(code=54, names=('COMMA', 'COMM', ','))
        elif key in ('DOT', '.'):
            make_key(code=55, names=('DOT', '.'))
        elif key in ('SLASH', 'SLSH'):
            make_key(code=56, names=('SLASH', 'SLSH'))

        # Function Keys
        elif key in ('F1',):
            make_key(code=58, names=('F1',))
        elif key in ('F2',):
            make_key(code=59, names=('F2',))
        elif key in ('F3',):
            make_key(code=60, names=('F3',))
        elif key in ('F4',):
            make_key(code=61, names=('F4',))
        elif key in ('F5',):
            make_key(code=62, names=('F5',))
        elif key in ('F6',):
            make_key(code=63, names=('F6',))
        elif key in ('F7',):
            make_key(code=64, names=('F7',))
        elif key in ('F8',):
            make_key(code=65, names=('F8',))
        elif key in ('F9',):
            make_key(code=66, names=('F9',))
        elif key in ('F10',):
            make_key(code=67, names=('F10',))
        elif key in ('F11',):
            make_key(code=68, names=('F11',))
        elif key in ('F12',):
            make_key(code=69, names=('F12',))
        elif key in ('F13',):
            make_key(code=104, names=('F13',))
        elif key in ('F14',):
            make_key(code=105, names=('F14',))
        elif key in ('F15',):
            make_key(code=106, names=('F15',))
        elif key in ('F16',):
            make_key(code=107, names=('F16',))
        elif key in ('F17',):
            make_key(code=108, names=('F17',))
        elif key in ('F18',):
            make_key(code=109, names=('F18',))
        elif key in ('F19',):
            make_key(code=110, names=('F19',))
        elif key in ('F20',):
            make_key(code=111, names=('F20',))
        elif key in ('F21',):
            make_key(code=112, names=('F21',))
        elif key in ('F22',):
            make_key(code=113, names=('F22',))
        elif key in ('F23',):
            make_key(code=114, names=('F23',))
        elif key in ('F24',):
            make_key(code=115, names=('F24',))

        # Lock Keys, Navigation, etc.
        elif key in ('CAPS_LOCK', 'CAPSLOCK', 'CLCK', 'CAPS'):
            make_key(code=57, names=('CAPS_LOCK', 'CAPSLOCK', 'CLCK', 'CAPS'))
        # FIXME: Investigate whether this key actually works, and
        #        uncomment when/if it does.
        # elif key in ('LOCKING_CAPS', 'LCAP'):
        #     # make_key(code=130, names=('LOCKING_CAPS', 'LCAP'))
        elif key in ('PRINT_SCREEN', 'PSCREEN', 'PSCR'):
            make_key(code=70, names=('PRINT_SCREEN', 'PSCREEN', 'PSCR'))
        elif key in ('SCROLL_LOCK', 'SCROLLLOCK', 'SLCK'):
            make_key(code=71, names=('SCROLL_LOCK', 'SCROLLLOCK', 'SLCK'))
        # FIXME: Investigate whether this key actually works, and
        #        uncomment when/if it does.
        # elif key in ('LOCKING_SCROLL', 'LSCRL'):
        #     make_key(code=132, names=('LOCKING_SCROLL', 'LSCRL'))
        elif key in ('PAUSE', 'PAUS', 'BRK'):
            make_key(code=72, names=('PAUSE', 'PAUS', 'BRK'))
        elif key in ('INSERT', 'INS'):
            make_key(code=73, names=('INSERT', 'INS'))
        elif key in ('HOME',):
            make_key(code=74, names=('HOME',))
        elif key in ('PGUP',):
            make_key(code=75, names=('PGUP',))
        elif key in ('DELETE', 'DEL'):
            make_key(code=76, names=('DELETE', 'DEL'))
        elif key in ('END',):
            make_key(code=77, names=('END',))
        elif key in ('PGDOWN', 'PGDN'):
            make_key(code=78, names=('PGDOWN', 'PGDN'))
        elif key in ('RIGHT', 'RGHT'):
            make_key(code=79, names=('RIGHT', 'RGHT'))
        elif key in ('LEFT',):
            make_key(code=80, names=('LEFT',))
        elif key in ('DOWN',):
            make_key(code=81, names=('DOWN',))
        elif key in ('UP',):
            make_key(code=82, names=('UP',))

        # Numpad
        elif key in ('NUM_LOCK', 'NUMLOCK', 'NLCK'):
            make_key(code=83, names=('NUM_LOCK', 'NUMLOCK', 'NLCK'))
        # FIXME: Investigate whether this key actually works, and
        #        uncomment when/if it does.
        # elif key in ('LOCKING_NUM', 'LNUM'):
        #     make_key(code=131, names=('LOCKING_NUM', 'LNUM'))
        elif key in ('KP_SLASH', 'NUMPAD_SLASH', 'PSLS'):
            make_key(code=84, names=('KP_SLASH', 'NUMPAD_SLASH', 'PSLS'))
        elif key in ('KP_ASTERISK', 'NUMPAD_ASTERISK', 'PAST'):
            make_key(code=85, names=('KP_ASTERISK', 'NUMPAD_ASTERISK', 'PAST'))
        elif key in ('KP_MINUS', 'NUMPAD_MINUS', 'PMNS'):
            make_key(code=86, names=('KP_MINUS', 'NUMPAD_MINUS', 'PMNS'))
        elif key in ('KP_PLUS', 'NUMPAD_PLUS', 'PPLS'):
            make_key(code=87, names=('KP_PLUS', 'NUMPAD_PLUS', 'PPLS'))
        elif key in ('KP_ENTER', 'NUMPAD_ENTER', 'PENT'):
            make_key(code=88, names=('KP_ENTER', 'NUMPAD_ENTER', 'PENT'))
        elif key in ('KP_1', 'P1', 'NUMPAD_1'):
            make_key(code=89, names=('KP_1', 'P1', 'NUMPAD_1'))
        elif key in ('KP_2', 'P2', 'NUMPAD_2'):
            make_key(code=90, names=('KP_2', 'P2', 'NUMPAD_2'))
        elif key in ('KP_3', 'P3', 'NUMPAD_3'):
            make_key(code=91, names=('KP_3', 'P3', 'NUMPAD_3'))
        elif key in ('KP_4', 'P4', 'NUMPAD_4'):
            make_key(code=92, names=('KP_4', 'P4', 'NUMPAD_4'))
        elif key in ('KP_5', 'P5', 'NUMPAD_5'):
            make_key(code=93, names=('KP_5', 'P5', 'NUMPAD_5'))
        elif key in ('KP_6', 'P6', 'NUMPAD_6'):
            make_key(code=94, names=('KP_6', 'P6', 'NUMPAD_6'))
        elif key in ('KP_7', 'P7', 'NUMPAD_7'):
            make_key(code=95, names=('KP_7', 'P7', 'NUMPAD_7'))
        elif key in ('KP_8', 'P8', 'NUMPAD_8'):
            make_key(code=96, names=('KP_8', 'P8', 'NUMPAD_8'))
        elif key in ('KP_9', 'P9', 'NUMPAD_9'):
            make_key(code=97, names=('KP_9', 'P9', 'NUMPAD_9'))
        elif key in ('KP_0', 'P0', 'NUMPAD_0'):
            make_key(code=98, names=('KP_0', 'P0', 'NUMPAD_0'))
        elif key in ('KP_DOT', 'PDOT', 'NUMPAD_DOT'):
            make_key(code=99, names=('KP_DOT', 'PDOT', 'NUMPAD_DOT'))
        elif key in ('KP_EQUAL', 'PEQL', 'NUMPAD_EQUAL'):
            make_key(code=103, names=('KP_EQUAL', 'PEQL', 'NUMPAD_EQUAL'))
        elif key in ('KP_COMMA', 'PCMM', 'NUMPAD_COMMA'):
            make_key(code=133, names=('KP_COMMA', 'PCMM', 'NUMPAD_COMMA'))
        elif key in ('KP_EQUAL_AS400', 'NUMPAD_EQUAL_AS400'):
            make_key(code=134, names=('KP_EQUAL_AS400', 'NUMPAD_EQUAL_AS400'))

        # Making life better for folks on tiny keyboards especially: exposes
        # the 'shifted' keys as raw keys. Under the hood we're still
        # sending Shift+(whatever key is normally pressed) to get these, so
        # for example `KC_AT` will hold shift and press 2.
        elif key in ('TILDE', 'TILD', '~'):
            make_shifted_key('GRAVE', names=('TILDE', 'TILD', '~'))
        elif key in ('EXCLAIM', 'EXLM', '!'):
            make_shifted_key('1', names=('EXCLAIM', 'EXLM', '!'))
        elif key in ('AT', '@'):
            make_shifted_key('2', names=('AT', '@'))
        elif key in ('HASH', 'POUND', '#'):
            make_shifted_key('3', names=('HASH', 'POUND', '#'))
        elif key in ('DOLLAR', 'DLR', '$'):
            make_shifted_key('4', names=('DOLLAR', 'DLR', '$'))
        elif key in ('PERCENT', 'PERC', '%'):
            make_shifted_key('5', names=('PERCENT', 'PERC', '%'))
        elif key in ('CIRCUMFLEX', 'CIRC', '^'):
            make_shifted_key('6', names=('CIRCUMFLEX', 'CIRC', '^'))
        elif key in ('AMPERSAND', 'AMPR', '&'):
            make_shifted_key('7', names=('AMPERSAND', 'AMPR', '&'))
        elif key in ('ASTERISK', 'ASTR', '*'):
            make_shifted_key('8', names=('ASTERISK', 'ASTR', '*'))
        elif key in ('LEFT_PAREN', 'LPRN', '('):
            make_shifted_key('9', names=('LEFT_PAREN', 'LPRN', '('))
        elif key in ('RIGHT_PAREN', 'RPRN', ')'):
            make_shifted_key('0', names=('RIGHT_PAREN', 'RPRN', ')'))
        elif key in ('UNDERSCORE', 'UNDS', '_'):
            make_shifted_key('MINUS', names=('UNDERSCORE', 'UNDS', '_'))
        elif key in ('PLUS', '+'):
            make_shifted_key('EQUAL', names=('PLUS', '+'))
        elif key in ('LEFT_CURLY_BRACE', 'LCBR', '{'):
            make_shifted_key('LBRACKET', names=('LEFT_CURLY_BRACE', 'LCBR', '{'))
        elif key in ('RIGHT_CURLY_BRACE', 'RCBR', '}'):
            make_shifted_key('RBRACKET', names=('RIGHT_CURLY_BRACE', 'RCBR', '}'))
        elif key in ('PIPE', '|'):
            make_shifted_key('BACKSLASH', names=('PIPE', '|'))
        elif key in ('COLON', 'COLN', ':'):
            make_shifted_key('SEMICOLON', names=('COLON', 'COLN', ':'))
        elif key in ('DOUBLE_QUOTE', 'DQUO', 'DQT', '"'):
            make_shifted_key('QUOTE', names=('DOUBLE_QUOTE', 'DQUO', 'DQT', '"'))
        elif key in ('LEFT_ANGLE_BRACKET', 'LABK', '<'):
            make_shifted_key('COMMA', names=('LEFT_ANGLE_BRACKET', 'LABK', '<'))
        elif key in ('RIGHT_ANGLE_BRACKET', 'RABK', '>'):
            make_shifted_key('DOT', names=('RIGHT_ANGLE_BRACKET', 'RABK', '>'))
        elif key in ('QUESTION', 'QUES', '?'):
            make_shifted_key('SLSH', names=('QUESTION', 'QUES', '?'))

        # International
        elif key in ('NONUS_HASH', 'NUHS'):
            make_key(code=50, names=('NONUS_HASH', 'NUHS'))
        elif key in ('NONUS_BSLASH', 'NUBS'):
            make_key(code=100, names=('NONUS_BSLASH', 'NUBS'))
        elif key in ('APP', 'APPLICATION', 'SEL', 'WINMENU'):
            make_key(code=101, names=('APP', 'APPLICATION', 'SEL', 'WINMENU'))

        elif key in ('INT1', 'RO'):
            make_key(code=135, names=('INT1', 'RO'))
        elif key in ('INT2', 'KANA'):
            make_key(code=136, names=('INT2', 'KANA'))
        elif key in ('INT3', 'JYEN'):
            make_key(code=137, names=('INT3', 'JYEN'))
        elif key in ('INT4', 'HENK'):
            make_key(code=138, names=('INT4', 'HENK'))
        elif key in ('INT5', 'MHEN'):
            make_key(code=139, names=('INT5', 'MHEN'))
        elif key in ('INT6',):
            make_key(code=140, names=('INT6',))
        elif key in ('INT7',):
            make_key(code=141, names=('INT7',))
        elif key in ('INT8',):
            make_key(code=142, names=('INT8',))
        elif key in ('INT9',):
            make_key(code=143, names=('INT9',))
        elif key in ('LANG1', 'HAEN'):
            make_key(code=144, names=('LANG1', 'HAEN'))
        elif key in ('LANG2', 'HAEJ'):
            make_key(code=145, names=('LANG2', 'HAEJ'))
        elif key in ('LANG3',):
            make_key(code=146, names=('LANG3',))
        elif key in ('LANG4',):
            make_key(code=147, names=('LANG4',))
        elif key in ('LANG5',):
            make_key(code=148, names=('LANG5',))
        elif key in ('LANG6',):
            make_key(code=149, names=('LANG6',))
        elif key in ('LANG7',):
            make_key(code=150, names=('LANG7',))
        elif key in ('LANG8',):
            make_key(code=151, names=('LANG8',))
        elif key in ('LANG9',):
            make_key(code=152, names=('LANG9',))

        # Consumer ("media") keys. Most known keys aren't supported here. A much
        # longer list used to exist in this file, but the codes were almost certainly
        # incorrect, conflicting with each other, or otherwise 'weird'. We'll add them
        # back in piecemeal as needed. PRs welcome.
        #
        # A super useful reference for these is http://www.freebsddiary.org/APC/usb_hid_usages.php
        # Note that currently we only have the PC codes. Recent MacOS versions seem to
        # support PC media keys, so I don't know how much value we would get out of
        # adding the old Apple-specific consumer codes, but again, PRs welcome if the
        # lack of them impacts you.
        elif key in ('AUDIO_MUTE', 'MUTE'):
            make_consumer_key(code=226, names=('AUDIO_MUTE', 'MUTE'))  # 0xE2
        elif key in ('AUDIO_VOL_UP', 'VOLU'):
            make_consumer_key(code=233, names=('AUDIO_VOL_UP', 'VOLU'))  # 0xE9
        elif key in ('AUDIO_VOL_DOWN', 'VOLD'):
            make_consumer_key(code=234, names=('AUDIO_VOL_DOWN', 'VOLD'))  # 0xEA
        elif key in ('MEDIA_NEXT_TRACK', 'MNXT'):
            make_consumer_key(code=181, names=('MEDIA_NEXT_TRACK', 'MNXT'))  # 0xB5
        elif key in ('MEDIA_PREV_TRACK', 'MPRV'):
            make_consumer_key(code=182, names=('MEDIA_PREV_TRACK', 'MPRV'))  # 0xB6
        elif key in ('MEDIA_STOP', 'MSTP'):
            make_consumer_key(code=183, names=('MEDIA_STOP', 'MSTP'))  # 0xB7
        elif key in ('MEDIA_PLAY_PAUSE', 'MPLY'):
            make_consumer_key(
                code=205, names=('MEDIA_PLAY_PAUSE', 'MPLY')
            )  # 0xCD (this may not be right)
        elif key in ('MEDIA_EJECT', 'EJCT'):
            make_consumer_key(code=184, names=('MEDIA_EJECT', 'EJCT'))  # 0xB8
        elif key in ('MEDIA_FAST_FORWARD', 'MFFD'):
            make_consumer_key(code=179, names=('MEDIA_FAST_FORWARD', 'MFFD'))  # 0xB3
        elif key in ('MEDIA_REWIND', 'MRWD'):
            make_consumer_key(code=180, names=('MEDIA_REWIND', 'MRWD'))  # 0xB4

        # Internal, diagnostic, or auxiliary/enhanced keys

        # NO and TRNS are functionally identical in how they (don't) mutate
        # the state, but are tracked semantically separately, so create
        # two keys with the exact same functionality
        elif key in ('NO',):
            make_key(
                names=('NO',),
                on_press=handlers.passthrough,
                on_release=handlers.passthrough,
            )
        elif key in ('TRANSPARENT', 'TRNS'):
            make_key(
                names=('TRANSPARENT', 'TRNS'),
                on_press=handlers.passthrough,
                on_release=handlers.passthrough,
            )

        elif key in ('RESET',):
            make_key(names=('RESET',), on_press=handlers.reset)
        elif key in ('BOOTLOADER',):
            make_key(names=('BOOTLOADER',), on_press=handlers.bootloader)
        elif key in ('DEBUG', 'DBG'):
            make_key(
                names=('DEBUG', 'DBG'),
                on_press=handlers.debug_pressed,
                on_release=handlers.passthrough,
            )
        elif key in ('GESC',):
            make_key(
                names=('GESC',),
                on_press=handlers.gesc_pressed,
                on_release=handlers.gesc_released,
            )
        elif key in ('BKDL',):
            make_key(
                names=('BKDL',),
                on_press=handlers.bkdl_pressed,
                on_release=handlers.bkdl_released,
            )
        elif key in ('GESC', 'GRAVE_ESC'):
            make_key(
                names=('GESC', 'GRAVE_ESC'),
                on_press=handlers.gesc_pressed,
                on_release=handlers.gesc_released,
            )

        # A dummy key to trigger a sleep_ms call in a sequence of other keys in a
        # simple sequence macro.
        elif key in ('MACRO_SLEEP_MS', 'SLEEP_IN_SEQ'):
            make_argumented_key(
                validator=key_seq_sleep_validator,
                names=('MACRO_SLEEP_MS', 'SLEEP_IN_SEQ'),
                on_press=handlers.sleep_pressed,
            )
        elif key in ('UC_MODE_NOOP', 'UC_DISABLE'):
            make_key(
                names=('UC_MODE_NOOP', 'UC_DISABLE'),
                meta=UnicodeModeKeyMeta(UnicodeMode.NOOP),
                on_press=handlers.uc_mode_pressed,
            )
        elif key in ('UC_MODE_LINUX', 'UC_MODE_IBUS'):
            make_key(
                names=('UC_MODE_LINUX', 'UC_MODE_IBUS'),
                meta=UnicodeModeKeyMeta(UnicodeMode.IBUS),
                on_press=handlers.uc_mode_pressed,
            )
        elif key in ('UC_MODE_MACOS', 'UC_MODE_OSX', 'US_MODE_RALT'):
            make_key(
                names=('UC_MODE_MACOS', 'UC_MODE_OSX', 'US_MODE_RALT'),
                meta=UnicodeModeKeyMeta(UnicodeMode.RALT),
                on_press=handlers.uc_mode_pressed,
            )
        elif key in ('UC_MODE_WINC',):
            make_key(
                names=('UC_MODE_WINC',),
                meta=UnicodeModeKeyMeta(UnicodeMode.WINC),
                on_press=handlers.uc_mode_pressed,
            )
        elif key in ('UC_MODE',):
            make_argumented_key(
                validator=unicode_mode_key_validator,
                names=('UC_MODE',),
                on_press=handlers.uc_mode_pressed,
            )
        elif key in ('TAP_DANCE', 'TD'):
            make_argumented_key(
                validator=tap_dance_key_validator,
                names=('TAP_DANCE', 'TD'),
                on_press=handlers.td_pressed,
                on_release=handlers.td_released,
            )
        elif key in ('HID_SWITCH', 'HID'):
            make_key(names=('HID_SWITCH', 'HID'), on_press=handlers.hid_switch)
        else:
            raise ValueError('Invalid key')
        return self.__getattr__(key)


# Global state, will be filled in througout this file, and
# anywhere the user creates custom keys
KC = KeyAttrDict()


class Key:
    def __init__(
        self,
        code,
        has_modifiers=None,
        no_press=False,
        no_release=False,
        on_press=handlers.default_pressed,
        on_release=handlers.default_released,
        meta=object(),
    ):
        self.code = code
        self.has_modifiers = has_modifiers
        # cast to bool() in case we get a None value
        self.no_press = bool(no_press)
        self.no_release = bool(no_press)

        self._pre_press_handlers = []
        self._post_press_handlers = []
        self._pre_release_handlers = []
        self._post_release_handlers = []
        self._handle_press = on_press
        self._handle_release = on_release
        self.meta = meta

    def __call__(self, no_press=None, no_release=None):
        if no_press is None and no_release is None:
            return self

        return Key(
            code=self.code,
            has_modifiers=self.has_modifiers,
            no_press=no_press,
            no_release=no_release,
        )

    def __repr__(self):
        return 'Key(code={}, has_modifiers={})'.format(self.code, self.has_modifiers)

    def on_press(self, state, coord_int, coord_raw):
        for fn in self._pre_press_handlers:
            if not fn(self, state, KC, coord_int, coord_raw):
                return None

        ret = self._handle_press(self, state, KC, coord_int, coord_raw)

        for fn in self._post_press_handlers:
            fn(self, state, KC, coord_int, coord_raw)

        return ret

    def on_release(self, state, coord_int, coord_raw):
        for fn in self._pre_release_handlers:
            if not fn(self, state, KC, coord_int, coord_raw):
                return None

        ret = self._handle_release(self, state, KC, coord_int, coord_raw)

        for fn in self._post_release_handlers:
            fn(self, state, KC, coord_int, coord_raw)

        return ret

    def clone(self):
        '''
        Return a shallow clone of the current key without any pre/post press/release
        handlers attached. Almost exclusively useful for creating non-colliding keys
        to use such handlers.
        '''

        return type(self)(
            code=self.code,
            has_modifiers=self.has_modifiers,
            no_press=self.no_press,
            no_release=self.no_release,
            on_press=self._handle_press,
            on_release=self._handle_release,
            meta=self.meta,
        )

    def before_press_handler(self, fn):
        '''
        Attach a callback to be run prior to the on_press handler for this key.
        Receives the following:

        - self (this Key instance)
        - state (the current InternalState)
        - KC (the global KC lookup table, for convenience)
        - coord_int (an internal integer representation of the matrix coordinate
          for the pressed key - this is likely not useful to end users, but is
          provided for consistency with the internal handlers)
        - coord_raw (an X,Y tuple of the matrix coordinate - also likely not useful)

        If return value of the provided callback is evaluated to False, press
        processing is cancelled. Exceptions are _not_ caught, and will likely
        crash KMK if not handled within your function.

        These handlers are run in attachment order: handlers provided by earlier
        calls of this method will be executed before those provided by later calls.
        '''

        self._pre_press_handlers.append(fn)
        return self

    def after_press_handler(self, fn):
        '''
        Attach a callback to be run after the on_release handler for this key.
        Receives the following:

        - self (this Key instance)
        - state (the current InternalState)
        - KC (the global KC lookup table, for convenience)
        - coord_int (an internal integer representation of the matrix coordinate
          for the pressed key - this is likely not useful to end users, but is
          provided for consistency with the internal handlers)
        - coord_raw (an X,Y tuple of the matrix coordinate - also likely not useful)

        The return value of the provided callback is discarded. Exceptions are _not_
        caught, and will likely crash KMK if not handled within your function.

        These handlers are run in attachment order: handlers provided by earlier
        calls of this method will be executed before those provided by later calls.
        '''

        self._post_press_handlers.append(fn)
        return self

    def before_release_handler(self, fn):
        '''
        Attach a callback to be run prior to the on_release handler for this
        key. Receives the following:

        - self (this Key instance)
        - state (the current InternalState)
        - KC (the global KC lookup table, for convenience)
        - coord_int (an internal integer representation of the matrix coordinate
          for the pressed key - this is likely not useful to end users, but is
          provided for consistency with the internal handlers)
        - coord_raw (an X,Y tuple of the matrix coordinate - also likely not useful)

        If return value of the provided callback evaluates to False, the release
        processing is cancelled. Exceptions are _not_ caught, and will likely crash
        KMK if not handled within your function.

        These handlers are run in attachment order: handlers provided by earlier
        calls of this method will be executed before those provided by later calls.
        '''

        self._pre_release_handlers.append(fn)
        return self

    def after_release_handler(self, fn):
        '''
        Attach a callback to be run after the on_release handler for this key.
        Receives the following:

        - self (this Key instance)
        - state (the current InternalState)
        - KC (the global KC lookup table, for convenience)
        - coord_int (an internal integer representation of the matrix coordinate
          for the pressed key - this is likely not useful to end users, but is
          provided for consistency with the internal handlers)
        - coord_raw (an X,Y tuple of the matrix coordinate - also likely not useful)

        The return value of the provided callback is discarded. Exceptions are _not_
        caught, and will likely crash KMK if not handled within your function.

        These handlers are run in attachment order: handlers provided by earlier
        calls of this method will be executed before those provided by later calls.
        '''

        self._post_release_handlers.append(fn)
        return self


class ModifierKey(Key):
    # FIXME this is atrocious to read. Please, please, please, strike down upon
    # this with great vengeance and furious anger.

    FAKE_CODE = const(-1)

    def __call__(self, modified_code=None, no_press=None, no_release=None):
        if modified_code is None and no_press is None and no_release is None:
            return self

        if modified_code is not None:
            if isinstance(modified_code, ModifierKey):
                new_keycode = ModifierKey(
                    ModifierKey.FAKE_CODE,
                    set() if self.has_modifiers is None else self.has_modifiers,
                    no_press=no_press,
                    no_release=no_release,
                )

                if self.code != ModifierKey.FAKE_CODE:
                    new_keycode.has_modifiers.add(self.code)

                if modified_code.code != ModifierKey.FAKE_CODE:
                    new_keycode.has_modifiers.add(modified_code.code)
            else:
                new_keycode = Key(
                    modified_code.code,
                    {self.code},
                    no_press=no_press,
                    no_release=no_release,
                )

            if modified_code.has_modifiers:
                new_keycode.has_modifiers |= modified_code.has_modifiers
        else:
            new_keycode = Key(self.code, no_press=no_press, no_release=no_release)

        return new_keycode

    def __repr__(self):
        return 'ModifierKey(code={}, has_modifiers={})'.format(
            self.code, self.has_modifiers
        )


class ConsumerKey(Key):
    pass


def register_key_names(key, names=tuple()):  # NOQA
    '''
    Names are globally unique. If a later key is created with
    the same name as an existing entry in `KC`, it will overwrite
    the existing entry.

    If a name entry is only a single letter, its entry in the KC
    object will not be case-sensitive (meaning `names=('A',)` is
    sufficient to create a key accessible by both `KC.A` and `KC.a`).
    '''

    for name in names:
        KC[name] = key

        if len(name) == 1:
            KC[name.upper()] = key
            KC[name.lower()] = key

    return key


def make_key(code=None, names=tuple(), type=KEY_SIMPLE, **kwargs):  # NOQA
    '''
    Create a new key, aliased by `names` in the KC lookup table.

    If a code is not specified, the key is assumed to be a custom
    internal key to be handled in a state callback rather than
    sent directly to the OS. These codes will autoincrement.

    See register_key_names() for details on the assignment.

    All **kwargs are passed to the Key constructor
    '''

    global NEXT_AVAILABLE_KEY

    if type == KEY_SIMPLE:
        constructor = Key
    elif type == KEY_MODIFIER:
        constructor = ModifierKey
    elif type == KEY_CONSUMER:
        constructor = ConsumerKey
    else:
        raise ValueError('Unrecognized key type')

    if code is None:
        code = NEXT_AVAILABLE_KEY
        NEXT_AVAILABLE_KEY += 1
    elif code >= FIRST_KMK_INTERNAL_KEY:
        # Try to ensure future auto-generated internal keycodes won't
        # be overridden by continuing to +1 the sequence from the provided
        # code
        NEXT_AVAILABLE_KEY = max(NEXT_AVAILABLE_KEY, code + 1)

    key = constructor(code=code, **kwargs)

    register_key_names(key, names)

    gc.collect()

    return key


def make_mod_key(*args, **kwargs):
    return make_key(*args, **kwargs, type=KEY_MODIFIER)


def make_shifted_key(target_name, names=tuple()):  # NOQA
    key = KC.LSFT(KC[target_name])

    register_key_names(key, names)

    return key


def make_consumer_key(*args, **kwargs):
    return make_key(*args, **kwargs, type=KEY_CONSUMER)


# Argumented keys are implicitly internal, so auto-gen of code
# is almost certainly the best plan here
def make_argumented_key(
    validator=lambda *validator_args, **validator_kwargs: object(),
    names=tuple(),  # NOQA
    *constructor_args,
    **constructor_kwargs,
):
    global NEXT_AVAILABLE_KEY

    def _argumented_key(*user_args, **user_kwargs):
        global NEXT_AVAILABLE_KEY

        meta = validator(*user_args, **user_kwargs)

        if meta:
            key = Key(
                NEXT_AVAILABLE_KEY, meta=meta, *constructor_args, **constructor_kwargs
            )

            NEXT_AVAILABLE_KEY += 1

            return key

        else:
            raise ValueError(
                'Argumented key validator failed for unknown reasons. '
                "This may not be the keymap's fault, as a more specific error "
                'should have been raised.'
            )

    for name in names:
        KC[name] = _argumented_key

    return _argumented_key
