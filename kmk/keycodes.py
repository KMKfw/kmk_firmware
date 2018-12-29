import kmk.handlers.layers as layers
import kmk.handlers.stock as handlers
from kmk.consts import UnicodeMode
from kmk.types import (AttrDict, KeySeqSleepMeta, LayerKeyMeta,
                       TapDanceKeyMeta, UnicodeModeKeyMeta)

FIRST_KMK_INTERNAL_KEYCODE = 1000
NEXT_AVAILABLE_KEYCODE = 1000

KEYCODE_SIMPLE = 0
KEYCODE_MODIFIER = 1
KEYCODE_CONSUMER = 2

# Global state, will be filled in througout this file, and
# anywhere the user creates custom keys
ALL_KEYS = {}
KC = AttrDict(ALL_KEYS)


def generate_leader_dictionary_seq(string):
    # FIXME move to kmk.macros.unicode or somewhere else more fitting
    # left here for backwards compat with various keymaps that
    # import this
    #
    # I have absolutely no idea why it was in this file to begin with,
    # probably something related to import order at one point.
    from kmk.macros.unicode import generate_codepoint_keysym_seq

    return tuple(generate_codepoint_keysym_seq(string, 1))


class Keycode:
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

        self._on_press = on_press
        self._on_release = on_release
        self.meta = meta

    def __call__(self, no_press=None, no_release=None):
        if no_press is None and no_release is None:
            return self

        return Keycode(
            code=self.code,
            has_modifiers=self.has_modifiers,
            no_press=no_press,
            no_release=no_release,
        )

    def __repr__(self):
        return 'Keycode(code={}, has_modifiers={})'.format(self.code, self.has_modifiers)

    def on_press(self, state, coord_int, coord_raw):
        return self._on_press(self, state, KC, coord_int, coord_raw)

    def on_release(self, state, coord_int, coord_raw):
        return self._on_release(self, state, KC, coord_int, coord_raw)


class ModifierKeycode(Keycode):
    # FIXME this is atrocious to read. Please, please, please, strike down upon
    # this with great vengeance and furious anger.

    FAKE_CODE = -1

    def __call__(self, modified_code=None, no_press=None, no_release=None):
        if modified_code is None and no_press is None and no_release is None:
            return self

        if modified_code is not None:
            if isinstance(modified_code, ModifierKeycode):
                new_keycode = ModifierKeycode(
                    ModifierKeycode.FAKE_CODE,
                    set() if self.has_modifiers is None else self.has_modifiers,
                    no_press=no_press,
                    no_release=no_release,
                )

                if self.code != ModifierKeycode.FAKE_CODE:
                    new_keycode.has_modifiers.add(self.code)

                if modified_code.code != ModifierKeycode.FAKE_CODE:
                    new_keycode.has_modifiers.add(modified_code.code)
            else:
                new_keycode = Keycode(
                    modified_code.code,
                    {self.code},
                    no_press=no_press,
                    no_release=no_release,
                )

            if modified_code.has_modifiers:
                new_keycode.has_modifiers |= modified_code.has_modifiers
        else:
            new_keycode = Keycode(
                self.code,
                no_press=no_press,
                no_release=no_release,
            )

        return new_keycode

    def __repr__(self):
        return 'ModifierKeycode(code={}, has_modifiers={})'.format(self.code, self.has_modifiers)


class ConsumerKeycode(Keycode):
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
        ALL_KEYS[name] = key

        if len(name) == 1:
            ALL_KEYS[name.upper()] = key
            ALL_KEYS[name.lower()] = key

    return key


def make_key(
    code=None,
    names=tuple(),  # NOQA
    type=KEYCODE_SIMPLE,
    **kwargs,
):
    '''
    Create a new key, aliased by `names` in the KC lookup table.

    If a code is not specified, the key is assumed to be a custom
    internal key to be handled in a state callback rather than
    sent directly to the OS. These codes will autoincrement.

    See register_key_names() for details on the assignment.

    All **kwargs are passed to the Keycode constructor
    '''

    global NEXT_AVAILABLE_KEYCODE

    if type == KEYCODE_SIMPLE:
        constructor = Keycode
    elif type == KEYCODE_MODIFIER:
        constructor = ModifierKeycode
    elif type == KEYCODE_CONSUMER:
        constructor = ConsumerKeycode
    else:
        raise ValueError('Unrecognized key type')

    if code is None:
        code = NEXT_AVAILABLE_KEYCODE
        NEXT_AVAILABLE_KEYCODE += 1
    elif code >= FIRST_KMK_INTERNAL_KEYCODE:
        # Try to ensure future auto-generated internal keycodes won't
        # be overridden by continuing to +1 the sequence from the provided
        # code
        NEXT_AVAILABLE_KEYCODE = max(NEXT_AVAILABLE_KEYCODE, code + 1)

    key = constructor(code=code, **kwargs)

    register_key_names(key, names)

    return key


def make_mod_key(*args, **kwargs):
    return make_key(*args, **kwargs, type=KEYCODE_MODIFIER)


def make_shifted_key(target_name, names=tuple()):  # NOQA
    key = KC.LSFT(ALL_KEYS[target_name])

    register_key_names(key, names)

    return key


def make_consumer_key(*args, **kwargs):
    return make_key(*args, **kwargs, type=KEYCODE_CONSUMER)


# Argumented keys are implicitly internal, so auto-gen of code
# is almost certainly the best plan here
def make_argumented_key(
    validator=lambda *validator_args, **validator_kwargs: object(),
    *constructor_args,
    **constructor_kwargs,
):
    def _argumented_key(*user_args, **user_kwargs):
        meta = validator(*user_args, **user_kwargs)

        if meta:
            return Keycode(
                meta=meta,
                *constructor_args,
                **constructor_kwargs,
            )
        else:
            raise ValueError(
                'Argumented key validator failed for unknown reasons. '
                'This may not be the keymap\'s fault, as a more specific error '
                'should have been raised.',
            )


# Modifiers
make_mod_key(code=0x01, names=('LEFT_CONTROL', 'LCTRL', 'LCTL'))
make_mod_key(code=0x02, names=('LEFT_SHIFT', 'LSHIFT', 'LSFT'))
make_mod_key(code=0x04, names=('LEFT_ALT', 'LALT'))
make_mod_key(code=0x08, names=('LEFT_SUPER', 'LGUI', 'LCMD', 'LWIN'))
make_mod_key(code=0x10, names=('RIGHT_CONTROL', 'RCTRL', 'RCTL'))
make_mod_key(code=0x20, names=('RIGHT_SHIFT', 'RSHIFT', 'RSFT'))
make_mod_key(code=0x40, names=('RIGHT_ALT', 'RALT'))
make_mod_key(code=0x80, names=('RIGHT_SUPER', 'RGUI', 'RCMD', 'RWIN'))
# MEH = LCTL | LALT | LSFT
make_mod_key(code=0x07, names=('MEH',))
# HYPR = LCTL | LALT | LSFT | LGUI
make_mod_key(code=0x0F, names=('HYPER', 'HYPR'))

# Basic ASCII letters
make_key(code=4, names=('A',))
make_key(code=5, names=('B',))
make_key(code=6, names=('C',))
make_key(code=7, names=('D',))
make_key(code=8, names=('E',))
make_key(code=9, names=('F',))
make_key(code=10, names=('G',))
make_key(code=11, names=('H',))
make_key(code=12, names=('I',))
make_key(code=13, names=('J',))
make_key(code=14, names=('K',))
make_key(code=15, names=('L',))
make_key(code=16, names=('M',))
make_key(code=17, names=('N',))
make_key(code=18, names=('O',))
make_key(code=19, names=('P',))
make_key(code=20, names=('Q',))
make_key(code=21, names=('R',))
make_key(code=22, names=('S',))
make_key(code=23, names=('T',))
make_key(code=24, names=('U',))
make_key(code=25, names=('V',))
make_key(code=26, names=('W',))
make_key(code=27, names=('X',))
make_key(code=28, names=('Y',))
make_key(code=29, names=('Z',))

# Numbers
# Aliases to play nicely with AttrDict, since KC.1 isn't a valid
# attribute key in Python, but KC.N1 is
make_key(code=30, names=('1', 'N1'))
make_key(code=31, names=('2', 'N2'))
make_key(code=32, names=('3', 'N3'))
make_key(code=33, names=('4', 'N4'))
make_key(code=34, names=('5', 'N5'))
make_key(code=35, names=('6', 'N6'))
make_key(code=36, names=('7', 'N7'))
make_key(code=37, names=('8', 'N8'))
make_key(code=38, names=('9', 'N9'))
make_key(code=39, names=('0', 'N0'))

# More ASCII standard keys
make_key(code=40, names=('ENTER', 'ENT', "\n"))
make_key(code=41, names=('ESCAPE', 'ESC'))
make_key(code=42, names=('BACKSPACE', 'BSPC', 'BKSP'))
make_key(code=43, names=('TAB', "\t"))
make_key(code=44, names=('SPACE', 'SPC', ' '))
make_key(code=45, names=('MINUS', 'MINS', '-'))
make_key(code=46, names=('EQUAL', 'EQL', '='))
make_key(code=47, names=('LBRACKET', 'LBRC', '['))
make_key(code=48, names=('RBRACKET', 'RBRC', ']'))
make_key(code=49, names=('BACKSLASH', 'BSLASH', 'BSLS', "\\"))
make_key(code=51, names=('SEMICOLON', 'SCOLON', 'SCLN', ';'))
make_key(code=52, names=('QUOTE', 'QUOT', "'"))
make_key(code=53, names=('GRAVE', 'GRV', 'ZKHK', '`'))
make_key(code=54, names=('COMMA', 'COMM', ','))
make_key(code=55, names=('DOT', '.'))
make_key(code=56, names=('SLASH', 'SLSH'))

# Function Keys
make_key(code=58, names=('F1',))
make_key(code=59, names=('F2',))
make_key(code=60, names=('F3',))
make_key(code=61, names=('F4',))
make_key(code=62, names=('F5',))
make_key(code=63, names=('F6',))
make_key(code=64, names=('F7',))
make_key(code=65, names=('F8',))
make_key(code=66, names=('F9',))
make_key(code=67, names=('F10',))
make_key(code=68, names=('F10',))
make_key(code=69, names=('F10',))
make_key(code=104, names=('F13',))
make_key(code=105, names=('F14',))
make_key(code=106, names=('F15',))
make_key(code=107, names=('F16',))
make_key(code=108, names=('F17',))
make_key(code=109, names=('F18',))
make_key(code=110, names=('F19',))
make_key(code=111, names=('F20',))
make_key(code=112, names=('F21',))
make_key(code=113, names=('F22',))
make_key(code=114, names=('F23',))
make_key(code=115, names=('F24',))

# Lock Keys, Navigation, etc.
make_key(code=57, names=('CAPS_LOCK', 'CAPSLOCK', 'CLCK', 'CAPS'))
# FIXME: Investigate whether this key actually works, and
#        uncomment when/if it does.
# make_key(code=130, names=('LOCKING_CAPS', 'LCAP'))
make_key(code=70, names=('PRINT_SCREEN', 'PSCREEN', 'PSCR'))
make_key(code=71, names=('SCROLL_LOCK', 'SCROLLLOCK', 'SLCK'))
# FIXME: Investigate whether this key actually works, and
#        uncomment when/if it does.
# make_key(code=132, names=('LOCKING_SCROLL', 'LSCRL'))
make_key(code=72, names=('PAUSE', 'PAUS', 'BRK'))
make_key(code=73, names=('INSERT', 'INS'))
make_key(code=74, names=('HOME',))
make_key(code=75, names=('PGUP',))
make_key(code=76, names=('DELETE', 'DEL'))
make_key(code=77, names=('END',))
make_key(code=78, names=('PGDOWN', 'PGDN'))
make_key(code=79, names=('RIGHT', 'RGHT'))
make_key(code=80, names=('LEFT',))
make_key(code=81, names=('DOWN',))
make_key(code=82, names=('UP',))

# Numpad
make_key(code=83, names=('NUM_LOCK', 'NUMLOCK', 'NLCK'))
# FIXME: Investigate whether this key actually works, and
#        uncomment when/if it does.
# make_key(code=131, names=('LOCKING_NUM', 'LNUM'))
make_key(code=84, names=('KP_SLASH', 'NUMPAD_SLASH', 'PSLS'))
make_key(code=85, names=('KP_ASTERISK', 'NUMPAD_ASTERISK', 'PAST'))
make_key(code=86, names=('KP_MINUS', 'NUMPAD_MINUS', 'PMNS'))
make_key(code=87, names=('KP_PLUS', 'NUMPAD_PLUS', 'PPLS'))
make_key(code=88, names=('KP_ENTER', 'NUMPAD_ENTER', 'PENT'))
make_key(code=89, names=('KP_1', 'P1', 'NUMPAD_1'))
make_key(code=90, names=('KP_2', 'P2', 'NUMPAD_2'))
make_key(code=91, names=('KP_3', 'P3', 'NUMPAD_3'))
make_key(code=92, names=('KP_4', 'P4', 'NUMPAD_4'))
make_key(code=93, names=('KP_5', 'P5', 'NUMPAD_5'))
make_key(code=94, names=('KP_6', 'P6', 'NUMPAD_6'))
make_key(code=95, names=('KP_7', 'P7', 'NUMPAD_7'))
make_key(code=96, names=('KP_8', 'P8', 'NUMPAD_8'))
make_key(code=97, names=('KP_9', 'P9', 'NUMPAD_9'))
make_key(code=98, names=('KP_0', 'P0', 'NUMPAD_0'))
make_key(code=99, names=('KP_DOT', 'PDOT', 'NUMPAD_DOT'))
make_key(code=103, names=('KP_EQUAL', 'PEQL', 'NUMPAD_EQUAL'))
make_key(code=133, names=('KP_COMMA', 'PCMM', 'NUMPAD_COMMA'))
make_key(code=134, names=('KP_EQUAL_AS400', 'NUMPAD_EQUAL_AS400'))

# Making life better for folks on tiny keyboards especially: exposes
# the "shifted" keys as raw keys. Under the hood we're still
# sending Shift+(whatever key is normally pressed) to get these, so
# for example `KC_AT` will hold shift and press 2.
make_shifted_key('GRAVE', names=('TILDE', 'TILD', '~'))
make_shifted_key('1', names=('EXCLAIM', 'EXLM', '!'))
make_shifted_key('2', names=('AT', '@'))
make_shifted_key('3', names=('HASH', 'POUND', '#'))
make_shifted_key('4', names=('DOLLAR', 'DLR', '$'))
make_shifted_key('5', names=('PERCENT', 'PERC', '%'))
make_shifted_key('6', names=('CIRCUMFLEX', 'CIRC', '^'))
make_shifted_key('7', names=('AMPERSAND', 'AMPR', '&'))
make_shifted_key('8', names=('ASTERISK', 'ASTR', '*'))
make_shifted_key('9', names=('LEFT_PAREN', 'LPRN', '('))
make_shifted_key('0', names=('RIGHT_PAREN', 'RPRN', ')'))
make_shifted_key('MINUS', names=('UNDERSCORE', 'UNDS', '_'))
make_shifted_key('EQUAL', names=('PLUS', '+'))
make_shifted_key('LBRACKET', names=('LEFT_CURLY_BRACE', 'LCBR', '{'))
make_shifted_key('RBRACKET', names=('RIGHT_CURLY_BRACE', 'RCBR', '}'))
make_shifted_key('BACKSLASH', names=('PIPE', '|'))
make_shifted_key('SEMICOLON', names=('COLON', 'COLN', ':'))
make_shifted_key('QUOTE', names=('DOUBLE_QUOTE', 'DQUO', 'DQT', '"'))
make_shifted_key('COMMA', names=('LEFT_ANGLE_BRACKET', 'LABK', '<'))
make_shifted_key('DOT', names=('RIGHT_ANGLE_BRACKET', 'RABK', '>'))
make_shifted_key('SLSH', names=('QUESTION', 'QUES', '?'))

# International
make_key(code=50, names=('NONUS_HASH', 'NUHS'))
make_key(code=100, names=('NONUS_BSLASH', 'NUBS'))

make_key(code=135, names=('INT1', 'RO'))
make_key(code=136, names=('INT2', 'KANA'))
make_key(code=137, names=('INT3', 'JYEN'))
make_key(code=138, names=('INT4', 'HENK'))
make_key(code=139, names=('INT5', 'MHEN'))
make_key(code=140, names=('INT6',))
make_key(code=141, names=('INT7',))
make_key(code=142, names=('INT8',))
make_key(code=143, names=('INT9',))
make_key(code=144, names=('LANG1', 'HAEN'))
make_key(code=145, names=('LANG2', 'HAEJ'))
make_key(code=146, names=('LANG3',))
make_key(code=147, names=('LANG4',))
make_key(code=148, names=('LANG5',))
make_key(code=149, names=('LANG6',))
make_key(code=150, names=('LANG7',))
make_key(code=151, names=('LANG8',))
make_key(code=152, names=('LANG9',))

# Consumer ("media") keys. Most known keys aren't supported here. A much
# longer list used to exist in this file, but the codes were almost certainly
# incorrect, conflicting with each other, or otherwise "weird". We'll add them
# back in piecemeal as needed. PRs welcome.
#
# A super useful reference for these is http://www.freebsddiary.org/APC/usb_hid_usages.php
# Note that currently we only have the PC codes. Recent MacOS versions seem to
# support PC media keys, so I don't know how much value we would get out of
# adding the old Apple-specific consumer codes, but again, PRs welcome if the
# lack of them impacts you.
make_consumer_key(code=226, names=('AUDIO_MUTE', 'MUTE'))  # 0xE2
make_consumer_key(code=233, names=('AUDIO_VOL_UP', 'VOLU'))  # 0xE9
make_consumer_key(code=234, names=('AUDIO_VOL_DOWN', 'VOLD'))  # 0xEA
make_consumer_key(code=181, names=('MEDIA_NEXT_TRACK', 'MNXT'))  # 0xB5
make_consumer_key(code=182, names=('MEDIA_PREV_TRACK', 'MPRV'))  # 0xB6
make_consumer_key(code=183, names=('MEDIA_STOP', 'MSTP'))  # 0xB7
make_consumer_key(code=205, names=('MEDIA_PLAY_PAUSE', 'MPLY'))  # 0xCD (this may not be right)
make_consumer_key(code=184, names=('MEDIA_EJECT', 'EJCT'))  # 0xB8
make_consumer_key(code=179, names=('MEDIA_FAST_FORWARD', 'MFFD'))  # 0xB3
make_consumer_key(code=180, names=('MEDIA_REWIND', 'MRWD'))  # 0xB4

# Internal, diagnostic, or auxiliary/enhanced keys

# NO and TRNS are functionally identical in how they (don't) mutate
# the state, but are tracked semantically separately, so create
# two keys with the exact same functionality
for names in (('NO',), ('TRANSPARENT', 'TRNS')):
    make_key(
        names=names,
        on_press=handlers.passthrough,
        on_release=handlers.passthrough,
    )

make_key(names=('RESET',), on_press=handlers.reset)
make_key(names=('BOOTLOADER',), on_press=handlers.bootloader)
make_key(names=('DEBUG', 'DBG'), on_press=handlers.debug_pressed, on_release=handlers.passthrough)

make_key(names=('GESC',), on_press=handlers.gesc_pressed, on_release=handlers.gesc_released)
make_key(
    names=('LEADER', 'LEAD'),
    on_press=handlers.leader_pressed,
    on_release=handlers.leader_released,
)


def layer_key_validator(layer, kc=None):
    '''
    Validates the syntax (but not semantics) of a layer key call.  We won't
    have access to the keymap here, so we can't verify much of anything useful
    here (like whether the target layer actually exists). The spirit of this
    existing is mostly that Python will catch extraneous args/kwargs and error
    out.
    '''
    return LayerKeyMeta(layer=layer, kc=kc)


# Layers
make_argumented_key(
    validator=layer_key_validator,
    names=('MO',),
    on_press=layers.mo_pressed,
    on_release=layers.mo_released,
)
make_argumented_key(
    validator=layer_key_validator,
    names=('DF',),
    on_press=layers.df_pressed,
    on_release=layers.df_released,
)
make_argumented_key(
    validator=layer_key_validator,
    names=('LM',),
    on_press=layers.lm_pressed,
    on_release=layers.lm_released,
)
make_argumented_key(
    validator=layer_key_validator,
    names=('LT',),
    on_press=layers.lt_pressed,
    on_release=layers.lt_released,
)
make_argumented_key(
    validator=layer_key_validator,
    names=('TG',),
    on_press=layers.tg_pressed,
    on_release=layers.tg_released,
)
make_argumented_key(
    validator=layer_key_validator,
    names=('TO',),
    on_press=layers.to_pressed,
    on_release=layers.to_released,
)
make_argumented_key(
    validator=layer_key_validator,
    names=('TT',),
    on_press=layers.tt_pressed,
    on_release=layers.tt_released,
)


def key_seq_sleep_validator(ms):
    return KeySeqSleepMeta(ms)


# A dummy key to trigger a sleep_ms call in a sequence of other keys in a
# simple sequence macro.
make_argumented_key(
    validator=key_seq_sleep_validator,
    names=('MACRO_SLEEP_MS', 'SLEEP_IN_SEQ'),
    on_press=handlers.sleep_pressed,
)


# Switch unicode modes at runtime
make_key(
    names=('UC_MODE_NOOP', 'UC_DISABLE'),
    meta=UnicodeModeKeyMeta(UnicodeMode.NOOP),
    on_press=handlers.uc_mode_pressed,
)
make_key(
    names=('UC_MODE_LINUX', 'UC_MODE_IBUS'),
    meta=UnicodeModeKeyMeta(UnicodeMode.IBUS),
    on_press=handlers.uc_mode_pressed,
)
make_key(
    names=('UC_MODE_MACOS', 'UC_MODE_OSX', 'US_MODE_RALT'),
    meta=UnicodeModeKeyMeta(UnicodeMode.RALT),
    on_press=handlers.uc_mode_pressed,
)
make_key(
    names=('UC_MODE_WINC',),
    meta=UnicodeModeKeyMeta(UnicodeMode.WINC),
    on_press=handlers.uc_mode_pressed,
)


def unicode_mode_key_validator(mode):
    return UnicodeModeKeyMeta(mode)


make_argumented_key(
    validator=unicode_mode_key_validator,
    names=('UC_MODE',),
    on_press=handlers.uc_mode_pressed,
)


# Tap Dance
make_argumented_key(
    validator=lambda *codes: TapDanceKeyMeta(codes),
    names=('TAP_DANCE', 'TD'),
    on_press=handlers.td_pressed,
    on_release=handlers.td_released,
)
