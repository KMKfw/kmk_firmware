import gc
from micropython import const

import kmk.handlers.stock as handlers
from kmk.consts import UnicodeMode
from kmk.key_validators import key_seq_sleep_validator, unicode_mode_key_validator
from kmk.types import UnicodeModeKeyMeta

DEBUG_OUTPUT = False

FIRST_KMK_INTERNAL_KEY = const(1000)
NEXT_AVAILABLE_KEY = 1000

KEY_SIMPLE = const(0)
KEY_MODIFIER = const(1)
KEY_CONSUMER = const(2)

ALL_ALPHAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALL_NUMBERS = '1234567890'
# since KC.1 isn't valid Python, alias to KC.N1
ALL_NUMBER_ALIASES = tuple(f'N{x}' for x in ALL_NUMBERS)


def maybe_make_mod_key(code, names, *args, **kwargs):
    def closure(candidate):
        if candidate in names:
            return make_mod_key(code=code, names=names, *args, **kwargs)

    return closure


def maybe_make_key(code, names, *args, **kwargs):
    def closure(candidate):
        if candidate in names:
            return make_key(code=code, names=names, *args, **kwargs)

    return closure


def maybe_make_shifted_key(code, names, *args, **kwargs):
    def closure(candidate):
        if candidate in names:
            return make_shifted_key(code=code, names=names, *args, **kwargs)

    return closure


def maybe_make_consumer_key(code, names, *args, **kwargs):
    def closure(candidate):
        if candidate in names:
            return make_consumer_key(code=code, names=names, *args, **kwargs)

    return closure


def maybe_make_argumented_key(
    validator=lambda *validator_args, **validator_kwargs: object(),
    names=tuple(),  # NOQA
    *constructor_args,
    **constructor_kwargs,
):
    def closure(candidate):
        if candidate in names:
            return make_argumented_key(
                validator, names, *constructor_args, **constructor_kwargs
            )

    return closure


def maybe_make_alpha_key():
    def closure(candidate):
        if len(candidate) == 1:
            candidate_upper = candidate.upper()
            if candidate_upper in ALL_ALPHAS:
                return make_key(
                    code=4 + ALL_ALPHAS.index(candidate_upper),
                    names=(
                        candidate_upper,
                        candidate.lower(),
                    ),
                )

    return closure


def maybe_make_numeric_key():
    def closure(candidate):
        if candidate in ALL_NUMBERS or candidate in ALL_NUMBER_ALIASES:
            try:
                offset = ALL_NUMBERS.index(candidate)
            except ValueError:
                offset = ALL_NUMBER_ALIASES.index(candidate)

            return make_key(
                code=30 + offset,
                names=(ALL_NUMBERS[offset], ALL_NUMBER_ALIASES[offset]),
            )

    return closure


KEY_GENERATION_FUNCTIONS = (
    # NO and TRNS are functionally identical in how they (don't) mutate
    # the state, but are tracked semantically separately, so create
    # two keys with the exact same functionality
    maybe_make_key(
        None,
        ('NO', 'XXXXXXX'),
        on_press=handlers.passthrough,
        on_release=handlers.passthrough,
    ),
    maybe_make_key(
        None,
        ('TRANSPARENT', 'TRNS'),
        on_press=handlers.passthrough,
        on_release=handlers.passthrough,
    ),
    maybe_make_alpha_key(),
    maybe_make_numeric_key(),
    maybe_make_key(None, ('RESET',), on_press=handlers.reset),
    maybe_make_key(None, ('BOOTLOADER',), on_press=handlers.bootloader),
    maybe_make_key(
        None,
        ('DEBUG', 'DBG'),
        on_press=handlers.debug_pressed,
        on_release=handlers.passthrough,
    ),
    maybe_make_key(
        None,
        ('BKDL',),
        on_press=handlers.bkdl_pressed,
        on_release=handlers.bkdl_released,
    ),
    maybe_make_key(
        None,
        ('GESC', 'GRAVE_ESC'),
        on_press=handlers.gesc_pressed,
        on_release=handlers.gesc_released,
    ),
    # A dummy key to trigger a sleep_ms call in a sequence of other keys in a
    # simple sequence macro.
    maybe_make_argumented_key(
        key_seq_sleep_validator,
        ('MACRO_SLEEP_MS', 'SLEEP_IN_SEQ'),
        on_press=handlers.sleep_pressed,
    ),
    maybe_make_key(
        None,
        ('UC_MODE_NOOP', 'UC_DISABLE'),
        on_press=handlers.uc_mode_pressed,
        meta=UnicodeModeKeyMeta(UnicodeMode.NOOP),
    ),
    maybe_make_key(
        None,
        ('UC_MODE_LINUX', 'UC_MODE_IBUS'),
        on_press=handlers.uc_mode_pressed,
        meta=UnicodeModeKeyMeta(UnicodeMode.IBUS),
    ),
    maybe_make_key(
        None,
        ('UC_MODE_MACOS', 'UC_MODE_OSX', 'US_MODE_RALT'),
        on_press=handlers.uc_mode_pressed,
        meta=UnicodeModeKeyMeta(UnicodeMode.RALT),
    ),
    maybe_make_key(
        None,
        ('UC_MODE_WINC',),
        on_press=handlers.uc_mode_pressed,
        meta=UnicodeModeKeyMeta(UnicodeMode.WINC),
    ),
    maybe_make_argumented_key(
        unicode_mode_key_validator, ('UC_MODE',), on_press=handlers.uc_mode_pressed
    ),
    maybe_make_key(None, ('HID_SWITCH', 'HID'), on_press=handlers.hid_switch),
    maybe_make_key(None, ('BLE_REFRESH',), on_press=handlers.ble_refresh),
    maybe_make_mod_key(0x01, ('LEFT_CONTROL', 'LCTRL', 'LCTL')),
    maybe_make_mod_key(0x02, ('LEFT_SHIFT', 'LSHIFT', 'LSFT')),
    maybe_make_mod_key(0x04, ('LEFT_ALT', 'LALT', 'LOPT')),
    maybe_make_mod_key(0x08, ('LEFT_SUPER', 'LGUI', 'LCMD', 'LWIN')),
    maybe_make_mod_key(0x10, ('RIGHT_CONTROL', 'RCTRL', 'RCTL')),
    maybe_make_mod_key(0x20, ('RIGHT_SHIFT', 'RSHIFT', 'RSFT')),
    maybe_make_mod_key(0x40, ('RIGHT_ALT', 'RALT', 'ROPT')),
    maybe_make_mod_key(0x80, ('RIGHT_SUPER', 'RGUI', 'RCMD', 'RWIN')),
    # MEH = LCTL | LALT | LSFT# MEH = LCTL |
    maybe_make_mod_key(0x07, ('MEH',)),
    # HYPR = LCTL | LALT | LSFT | LGUI
    maybe_make_mod_key(0x0F, ('HYPER', 'HYPR')),
    # More ASCII standard keys
    maybe_make_key(40, ('ENTER', 'ENT', '\n')),
    maybe_make_key(41, ('ESCAPE', 'ESC')),
    maybe_make_key(42, ('BACKSPACE', 'BSPC', 'BKSP')),
    maybe_make_key(43, ('TAB', '\t')),
    maybe_make_key(44, ('SPACE', 'SPC', ' ')),
    maybe_make_key(45, ('MINUS', 'MINS', '-')),
    maybe_make_key(46, ('EQUAL', 'EQL', '=')),
    maybe_make_key(47, ('LBRACKET', 'LBRC', '[')),
    maybe_make_key(48, ('RBRACKET', 'RBRC', ']')),
    maybe_make_key(49, ('BACKSLASH', 'BSLASH', 'BSLS', '\\')),
    maybe_make_key(51, ('SEMICOLON', 'SCOLON', 'SCLN', ';')),
    maybe_make_key(52, ('QUOTE', 'QUOT', "'")),
    maybe_make_key(53, ('GRAVE', 'GRV', 'ZKHK', '`')),
    maybe_make_key(54, ('COMMA', 'COMM', ',')),
    maybe_make_key(55, ('DOT', '.')),
    maybe_make_key(56, ('SLASH', 'SLSH', '/')),
    # Function Keys
    maybe_make_key(58, ('F1',)),
    maybe_make_key(59, ('F2',)),
    maybe_make_key(60, ('F3',)),
    maybe_make_key(61, ('F4',)),
    maybe_make_key(62, ('F5',)),
    maybe_make_key(63, ('F6',)),
    maybe_make_key(64, ('F7',)),
    maybe_make_key(65, ('F8',)),
    maybe_make_key(66, ('F9',)),
    maybe_make_key(67, ('F10',)),
    maybe_make_key(68, ('F11',)),
    maybe_make_key(69, ('F12',)),
    maybe_make_key(104, ('F13',)),
    maybe_make_key(105, ('F14',)),
    maybe_make_key(106, ('F15',)),
    maybe_make_key(107, ('F16',)),
    maybe_make_key(108, ('F17',)),
    maybe_make_key(109, ('F18',)),
    maybe_make_key(110, ('F19',)),
    maybe_make_key(111, ('F20',)),
    maybe_make_key(112, ('F21',)),
    maybe_make_key(113, ('F22',)),
    maybe_make_key(114, ('F23',)),
    maybe_make_key(115, ('F24',)),
    # Lock Keys, Navigation, etc.
    maybe_make_key(57, ('CAPS_LOCK', 'CAPSLOCK', 'CLCK', 'CAPS')),
    # FIXME: Investigate whether this key actually works, and
    #        uncomment when/if it does.
    # maybe_make_key(130, ('LOCKING_CAPS', 'LCAP')),
    maybe_make_key(70, ('PRINT_SCREEN', 'PSCREEN', 'PSCR')),
    maybe_make_key(71, ('SCROLL_LOCK', 'SCROLLLOCK', 'SLCK')),
    # FIXME: Investigate whether this key actually works, and
    #        uncomment when/if it does.
    # maybe_make_key(132, ('LOCKING_SCROLL', 'LSCRL')),
    maybe_make_key(72, ('PAUSE', 'PAUS', 'BRK')),
    maybe_make_key(73, ('INSERT', 'INS')),
    maybe_make_key(74, ('HOME',)),
    maybe_make_key(75, ('PGUP',)),
    maybe_make_key(76, ('DELETE', 'DEL')),
    maybe_make_key(77, ('END',)),
    maybe_make_key(78, ('PGDOWN', 'PGDN')),
    maybe_make_key(79, ('RIGHT', 'RGHT')),
    maybe_make_key(80, ('LEFT',)),
    maybe_make_key(81, ('DOWN',)),
    maybe_make_key(82, ('UP',)),
    # Numpad
    maybe_make_key(83, ('NUM_LOCK', 'NUMLOCK', 'NLCK')),
    # FIXME: Investigate whether this key actually works, and
    #        uncomment when/if it does.
    # maybe_make_key(131, ('LOCKING_NUM', 'LNUM')),
    maybe_make_key(84, ('KP_SLASH', 'NUMPAD_SLASH', 'PSLS')),
    maybe_make_key(85, ('KP_ASTERISK', 'NUMPAD_ASTERISK', 'PAST')),
    maybe_make_key(86, ('KP_MINUS', 'NUMPAD_MINUS', 'PMNS')),
    maybe_make_key(87, ('KP_PLUS', 'NUMPAD_PLUS', 'PPLS')),
    maybe_make_key(88, ('KP_ENTER', 'NUMPAD_ENTER', 'PENT')),
    maybe_make_key(89, ('KP_1', 'P1', 'NUMPAD_1')),
    maybe_make_key(90, ('KP_2', 'P2', 'NUMPAD_2')),
    maybe_make_key(91, ('KP_3', 'P3', 'NUMPAD_3')),
    maybe_make_key(92, ('KP_4', 'P4', 'NUMPAD_4')),
    maybe_make_key(93, ('KP_5', 'P5', 'NUMPAD_5')),
    maybe_make_key(94, ('KP_6', 'P6', 'NUMPAD_6')),
    maybe_make_key(95, ('KP_7', 'P7', 'NUMPAD_7')),
    maybe_make_key(96, ('KP_8', 'P8', 'NUMPAD_8')),
    maybe_make_key(97, ('KP_9', 'P9', 'NUMPAD_9')),
    maybe_make_key(98, ('KP_0', 'P0', 'NUMPAD_0')),
    maybe_make_key(99, ('KP_DOT', 'PDOT', 'NUMPAD_DOT')),
    maybe_make_key(103, ('KP_EQUAL', 'PEQL', 'NUMPAD_EQUAL')),
    maybe_make_key(133, ('KP_COMMA', 'PCMM', 'NUMPAD_COMMA')),
    maybe_make_key(134, ('KP_EQUAL_AS400', 'NUMPAD_EQUAL_AS400')),
    # Making life better for folks on tiny keyboards especially: exposes
    # the 'shifted' keys as raw keys. Under the hood we're still
    # sending Shift+(whatever key is normally pressed) to get these, so
    # for example `KC_AT` will hold shift and press 2.
    maybe_make_shifted_key(30, ('EXCLAIM', 'EXLM', '!')),
    maybe_make_shifted_key(31, ('AT', '@')),
    maybe_make_shifted_key(32, ('HASH', 'POUND', '#')),
    maybe_make_shifted_key(33, ('DOLLAR', 'DLR', '$')),
    maybe_make_shifted_key(34, ('PERCENT', 'PERC', '%')),
    maybe_make_shifted_key(35, ('CIRCUMFLEX', 'CIRC', '^')),
    maybe_make_shifted_key(36, ('AMPERSAND', 'AMPR', '&')),
    maybe_make_shifted_key(37, ('ASTERISK', 'ASTR', '*')),
    maybe_make_shifted_key(38, ('LEFT_PAREN', 'LPRN', '(')),
    maybe_make_shifted_key(39, ('RIGHT_PAREN', 'RPRN', ')')),
    maybe_make_shifted_key(45, ('UNDERSCORE', 'UNDS', '_')),
    maybe_make_shifted_key(46, ('PLUS', '+')),
    maybe_make_shifted_key(47, ('LEFT_CURLY_BRACE', 'LCBR', '{')),
    maybe_make_shifted_key(48, ('RIGHT_CURLY_BRACE', 'RCBR', '}')),
    maybe_make_shifted_key(49, ('PIPE', '|')),
    maybe_make_shifted_key(51, ('COLON', 'COLN', ':')),
    maybe_make_shifted_key(52, ('DOUBLE_QUOTE', 'DQUO', 'DQT', '"')),
    maybe_make_shifted_key(53, ('TILDE', 'TILD', '~')),
    maybe_make_shifted_key(54, ('LEFT_ANGLE_BRACKET', 'LABK', '<')),
    maybe_make_shifted_key(55, ('RIGHT_ANGLE_BRACKET', 'RABK', '>')),
    maybe_make_shifted_key(56, ('QUESTION', 'QUES', '?')),
    # International
    maybe_make_key(50, ('NONUS_HASH', 'NUHS')),
    maybe_make_key(100, ('NONUS_BSLASH', 'NUBS')),
    maybe_make_key(101, ('APP', 'APPLICATION', 'SEL', 'WINMENU')),
    maybe_make_key(135, ('INT1', 'RO')),
    maybe_make_key(136, ('INT2', 'KANA')),
    maybe_make_key(137, ('INT3', 'JYEN')),
    maybe_make_key(138, ('INT4', 'HENK')),
    maybe_make_key(139, ('INT5', 'MHEN')),
    maybe_make_key(140, ('INT6',)),
    maybe_make_key(141, ('INT7',)),
    maybe_make_key(142, ('INT8',)),
    maybe_make_key(143, ('INT9',)),
    maybe_make_key(144, ('LANG1', 'HAEN')),
    maybe_make_key(145, ('LANG2', 'HAEJ')),
    maybe_make_key(146, ('LANG3',)),
    maybe_make_key(147, ('LANG4',)),
    maybe_make_key(148, ('LANG5',)),
    maybe_make_key(149, ('LANG6',)),
    maybe_make_key(150, ('LANG7',)),
    maybe_make_key(151, ('LANG8',)),
    maybe_make_key(152, ('LANG9',)),
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
    maybe_make_consumer_key(226, ('AUDIO_MUTE', 'MUTE')),  # 0xE2
    maybe_make_consumer_key(233, ('AUDIO_VOL_UP', 'VOLU')),  # 0xE9
    maybe_make_consumer_key(234, ('AUDIO_VOL_DOWN', 'VOLD')),  # 0xEA
    maybe_make_consumer_key(181, ('MEDIA_NEXT_TRACK', 'MNXT')),  # 0xB5
    maybe_make_consumer_key(182, ('MEDIA_PREV_TRACK', 'MPRV')),  # 0xB6
    maybe_make_consumer_key(183, ('MEDIA_STOP', 'MSTP')),  # 0xB7
    maybe_make_consumer_key(
        205, ('MEDIA_PLAY_PAUSE', 'MPLY')
    ),  # 0xCD (this may not be right)
    maybe_make_consumer_key(184, ('MEDIA_EJECT', 'EJCT')),  # 0xB8
    maybe_make_consumer_key(179, ('MEDIA_FAST_FORWARD', 'MFFD')),  # 0xB3
    maybe_make_consumer_key(180, ('MEDIA_REWIND', 'MRWD')),  # 0xB4
)


class KeyAttrDict:
    __cache = {}

    def __setitem__(self, key, value):
        if DEBUG_OUTPUT:
            print(f'__setitem__ {key}, {value}')
        self.__cache.__setitem__(key, value)

    def __getattr__(self, key):
        if DEBUG_OUTPUT:
            print(f'__getattr__ {key}')
        return self.__getitem__(key)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except Exception:
            return default

    def clear(self):
        self.__cache.clear()

    def __getitem__(self, key):
        if DEBUG_OUTPUT:
            print(f'__getitem__ {key}')
        try:
            return self.__cache[key]
        except Exception:
            for func in KEY_GENERATION_FUNCTIONS:
                result = func(key)
                if result is not None:
                    return result

        raise ValueError('Invalid key')


# Global state, will be filled in throughout this file, and
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
        self.no_release = bool(no_release)

        self._handle_press = on_press
        self._handle_release = on_release
        self.meta = meta

    def __call__(self, no_press=None, no_release=None):
        if no_press is None and no_release is None:
            return self

        return type(self)(
            code=self.code,
            has_modifiers=self.has_modifiers,
            no_press=no_press,
            no_release=no_release,
            on_press=self._handle_press,
            on_release=self._handle_release,
            meta=self.meta,
        )

    def __repr__(self):
        return 'Key(code={}, has_modifiers={})'.format(self.code, self.has_modifiers)

    def on_press(self, state, coord_int=None, coord_raw=None):
        if hasattr(self, '_pre_press_handlers'):
            for fn in self._pre_press_handlers:
                if not fn(self, state, KC, coord_int, coord_raw):
                    return None

        ret = self._handle_press(self, state, KC, coord_int, coord_raw)

        if hasattr(self, '_post_press_handlers'):
            for fn in self._post_press_handlers:
                fn(self, state, KC, coord_int, coord_raw)

        return ret

    def on_release(self, state, coord_int=None, coord_raw=None):
        if hasattr(self, '_pre_release_handlers'):
            for fn in self._pre_release_handlers:
                if not fn(self, state, KC, coord_int, coord_raw):
                    return None

        ret = self._handle_release(self, state, KC, coord_int, coord_raw)

        if hasattr(self, '_post_release_handlers'):
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

        if not hasattr(self, '_pre_press_handlers'):
            self._pre_press_handlers = []
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

        if not hasattr(self, '_post_press_handlers'):
            self._post_press_handlers = []
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

        if not hasattr(self, '_pre_release_handlers'):
            self._pre_release_handlers = []
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

        if not hasattr(self, '_post_release_handlers'):
            self._post_release_handlers = []
        self._post_release_handlers.append(fn)
        return self


class ModifierKey(Key):
    FAKE_CODE = const(-1)

    def __call__(self, modified_key=None, no_press=None, no_release=None):
        if modified_key is None:
            return super().__call__(no_press=no_press, no_release=no_release)

        modifiers = set()
        code = modified_key.code

        if self.code != ModifierKey.FAKE_CODE:
            modifiers.add(self.code)
        if self.has_modifiers:
            modifiers |= self.has_modifiers
        if modified_key.has_modifiers:
            modifiers |= modified_key.has_modifiers

        if isinstance(modified_key, ModifierKey):
            if modified_key.code != ModifierKey.FAKE_CODE:
                modifiers.add(modified_key.code)
            code = ModifierKey.FAKE_CODE

        return type(modified_key)(
            code=code,
            has_modifiers=modifiers,
            no_press=no_press,
            no_release=no_release,
            on_press=modified_key._handle_press,
            on_release=modified_key._handle_release,
            meta=modified_key.meta,
        )

    def __repr__(self):
        return 'ModifierKey(code={}, has_modifiers={})'.format(
            self.code, self.has_modifiers
        )


class ConsumerKey(Key):
    pass


def make_key(code=None, names=tuple(), type=KEY_SIMPLE, **kwargs):  # NOQA
    '''
    Create a new key, aliased by `names` in the KC lookup table.

    If a code is not specified, the key is assumed to be a custom
    internal key to be handled in a state callback rather than
    sent directly to the OS. These codes will autoincrement.

    Names are globally unique. If a later key is created with
    the same name as an existing entry in `KC`, it will overwrite
    the existing entry.

    Names are case sensitive.

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

    for name in names:
        KC[name] = key

    gc.collect()

    return key


def make_mod_key(code, names, *args, **kwargs):
    return make_key(code, names, *args, **kwargs, type=KEY_MODIFIER)


def make_shifted_key(code, names):
    return make_key(code, names, has_modifiers={KC.LSFT.code})


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
