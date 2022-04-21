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
ALL_NUMBER_ALIASES = [f'N{x}' for x in ALL_NUMBERS]


def maybe_make_alpha(candidate):
    # Basic ASCII letters/numbers don't need anything fancy, so check those
    # in the laziest way
    upper_candidate = candidate.upper()
    if upper_candidate in ALL_ALPHAS:
        return make_key(
            code=4 + ALL_ALPHAS.index(upper_candidate),
            names=[
                upper_candidate,
                candidate.lower(),
            ],
        )


def maybe_make_numeric(candidate):
    if candidate in ALL_NUMBERS or candidate in ALL_NUMBER_ALIASES:
        try:
            offset = ALL_NUMBERS.index(candidate)
        except ValueError:
            offset = ALL_NUMBER_ALIASES.index(candidate)

        return make_key(
            code=30 + offset,
            names=[ALL_NUMBERS[offset], ALL_NUMBER_ALIASES[offset]],
        )


def maybe_make_mod_key(candidate, names, code):
    if candidate in names:
        return make_mod_key(code=code, names=names)


def maybe_make_key(candidate, names, code=None, **kwargs):
    if candidate in names:
        return make_key(code=code, names=names, **kwargs)


def maybe_make_shifted_key(candidate, names, code):
    if candidate in names:
        return make_shifted_key(code=code, names=names)


def maybe_make_consumer_key(candidate, names, code):
    if candidate in names:
        return make_consumer_key(code=code, names=names)


def maybe_make_argumented_key(
    candidate,
    names,
    validator=lambda *validator_args, **validator_kwargs: object(),
    *constructor_args,
    **constructor_kwargs,
):
    if candidate in names:
        return make_argumented_key(
            validator=validator, names=names, **constructor_args, **constructor_kwargs
        )


KEY_FUNCTIONS = [
    # Try all the other weird special cases to get them out of our way:
    # This need to be done before or ALPHAS because NO will be parsed as alpha
    # Internal, diagnostic, or auxiliary/enhanced keys
    # NO and TRNS are functionally identical in how they (don't) mutate
    # the state, but are tracked semantically separately, so create
    # two keys with the exact same functionality
    lambda key: maybe_make_key(
        key,
        ['NO', 'XXXXXXX'],
        on_press=handlers.passthrough,
        on_release=handlers.passthrough,
    ),
    lambda key: maybe_make_key(
        key,
        ['TRANSPARENT', 'TRNS'],
        on_press=handlers.passthrough,
        on_release=handlers.passthrough,
    ),
    lambda key: maybe_make_alpha(key),
    lambda key: maybe_make_numeric(key),
    lambda key: maybe_make_key(key, ['RESET'], on_press=handlers.reset),
    lambda key: maybe_make_key(key, ['BOOTLOADER'], on_press=handlers.bootloader),
    lambda key: maybe_make_key(
        key,
        ['DEBUG', 'DBG'],
        on_press=handlers.debug_pressed,
        on_release=handlers.passthrough,
    ),
    lambda key: maybe_make_key(
        key, ['BKDL'], on_press=handlers.bkdl_pressed, on_release=handlers.bkdl_released
    ),
    lambda key: maybe_make_key(
        key,
        ['GESC', 'GRAVE_ESC'],
        on_press=handlers.gesc_pressed,
        on_release=handlers.gesc_released,
    ),
    # A dummy key to trigger a sleep_ms call in a sequence of other keys in a
    # simple sequence macro.
    lambda key: maybe_make_argumented_key(
        key,
        ['MACRO_SLEEP_MS', 'SLEEP_IN_SEQ'],
        validator=key_seq_sleep_validator,
        on_press=handlers.sleep_pressed,
    ),
    lambda key: maybe_make_key(
        key,
        ['UC_MODE_NOOP', 'UC_DISABLE'],
        meta=UnicodeModeKeyMeta(UnicodeMode.NOOP),
        on_press=handlers.uc_mode_pressed,
    ),
    lambda key: maybe_make_key(
        key,
        ['UC_MODE_LINUX', 'UC_MODE_IBUS'],
        meta=UnicodeModeKeyMeta(UnicodeMode.IBUS),
        on_press=handlers.uc_mode_pressed,
    ),
    lambda key: maybe_make_key(
        key,
        ['UC_MODE_MACOS', 'UC_MODE_OSX', 'US_MODE_RALT'],
        meta=UnicodeModeKeyMeta(UnicodeMode.RALT),
        on_press=handlers.uc_mode_pressed,
    ),
    lambda key: maybe_make_key(
        key,
        ['UC_MODE_WINC'],
        meta=UnicodeModeKeyMeta(UnicodeMode.WINC),
        on_press=handlers.uc_mode_pressed,
    ),
    lambda key: maybe_make_argumented_key(
        key,
        ['UC_MODE'],
        validator=unicode_mode_key_validator,
        on_press=handlers.uc_mode_pressed,
    ),
    lambda key: maybe_make_key(
        key, ['HID_SWITCH', 'HID'], on_press=handlers.hid_switch
    ),
    lambda key: maybe_make_key(key, ['BLE_REFRESH'], on_press=handlers.ble_refresh),
    # Modifiers
    lambda key: maybe_make_mod_key(key, ['LEFT_CONTROL', 'LCTRL', 'LCTL'], 0x01),
    lambda key: maybe_make_mod_key(key, ['LEFT_SHIFT', 'LSHIFT', 'LSFT'], 0x02),
    lambda key: maybe_make_mod_key(key, ['LEFT_ALT', 'LALT', 'LOPT'], 0x04),
    lambda key: maybe_make_mod_key(key, ['LEFT_SUPER', 'LGUI', 'LCMD', 'LWIN'], 0x08),
    lambda key: maybe_make_mod_key(key, ['RIGHT_CONTROL', 'RCTRL', 'RCTL'], 0x10),
    lambda key: maybe_make_mod_key(key, ['RIGHT_SHIFT', 'RSHIFT', 'RSFT'], 0x20),
    lambda key: maybe_make_mod_key(key, ['RIGHT_ALT', 'RALT', 'ROPT'], 0x40),
    lambda key: maybe_make_mod_key(key, ['RIGHT_SUPER', 'RGUI', 'RCMD', 'RWIN'], 0x80),
    # MEH = LCTL | LALT | LSFT# MEH = LCTL |
    lambda key: maybe_make_mod_key(key, ['MEH'], 0x07),
    # HYPR = LCTL | LALT | LSFT | LGUI
    lambda key: maybe_make_mod_key(key, ['HYPER', 'HYPR'], 0x0F),
    # More ASCII standard keys
    lambda key: maybe_make_key(key, ['ENTER', 'ENT', '\n'], 40),
    lambda key: maybe_make_key(key, ['ESCAPE', 'ESC'], 41),
    lambda key: maybe_make_key(key, ['BACKSPACE', 'BSPC', 'BKSP'], 42),
    lambda key: maybe_make_key(key, ['TAB', '\t'], 43),
    lambda key: maybe_make_key(key, ['SPACE', 'SPC', ' '], 44),
    lambda key: maybe_make_key(key, ['MINUS', 'MINS', '-'], 45),
    lambda key: maybe_make_key(key, ['EQUAL', 'EQL', '='], 46),
    lambda key: maybe_make_key(key, ['LBRACKET', 'LBRC', '['], 47),
    lambda key: maybe_make_key(key, ['RBRACKET', 'RBRC', ']'], 48),
    lambda key: maybe_make_key(key, ['BACKSLASH', 'BSLASH', 'BSLS', '\\'], 49),
    lambda key: maybe_make_key(key, ['SEMICOLON', 'SCOLON', 'SCLN', ';'], 51),
    lambda key: maybe_make_key(key, ['QUOTE', 'QUOT', "'"], 52),
    lambda key: maybe_make_key(key, ['GRAVE', 'GRV', 'ZKHK', '`'], 53),
    lambda key: maybe_make_key(key, ['COMMA', 'COMM', ','], 54),
    lambda key: maybe_make_key(key, ['DOT', '.'], 55),
    lambda key: maybe_make_key(key, ['SLASH', 'SLSH', '/'], 56),
    # Function Keys
    lambda key: maybe_make_key(key, ['F1'], 58),
    lambda key: maybe_make_key(key, ['F2'], 59),
    lambda key: maybe_make_key(key, ['F3'], 60),
    lambda key: maybe_make_key(key, ['F4'], 61),
    lambda key: maybe_make_key(key, ['F5'], 62),
    lambda key: maybe_make_key(key, ['F6'], 63),
    lambda key: maybe_make_key(key, ['F7'], 64),
    lambda key: maybe_make_key(key, ['F8'], 65),
    lambda key: maybe_make_key(key, ['F9'], 66),
    lambda key: maybe_make_key(key, ['F10'], 67),
    lambda key: maybe_make_key(key, ['F11'], 68),
    lambda key: maybe_make_key(key, ['F12'], 69),
    lambda key: maybe_make_key(key, ['F13'], 104),
    lambda key: maybe_make_key(key, ['F14'], 105),
    lambda key: maybe_make_key(key, ['F15'], 106),
    lambda key: maybe_make_key(key, ['F16'], 107),
    lambda key: maybe_make_key(key, ['F17'], 108),
    lambda key: maybe_make_key(key, ['F18'], 109),
    lambda key: maybe_make_key(key, ['F19'], 110),
    lambda key: maybe_make_key(key, ['F20'], 111),
    lambda key: maybe_make_key(key, ['F21'], 112),
    lambda key: maybe_make_key(key, ['F22'], 113),
    lambda key: maybe_make_key(key, ['F23'], 114),
    lambda key: maybe_make_key(key, ['F24'], 115),
    # Lock Keys, Navigation, etc.
    lambda key: maybe_make_key(key, ['CAPS_LOCK', 'CAPSLOCK', 'CLCK', 'CAPS'], 57),
    # FIXME: Investigate whether this key actually works, and
    #        uncomment when/if it does.
    # lambda key: maybe_make_key(key, ['LOCKING_CAPS', 'LCAP'], 130),
    lambda key: maybe_make_key(key, ['PRINT_SCREEN', 'PSCREEN', 'PSCR'], 70),
    lambda key: maybe_make_key(key, ['SCROLL_LOCK', 'SCROLLLOCK', 'SLCK'], 1),
    # FIXME: Investigate whether this key actually works, and
    #        uncomment when/if it does.
    # lambda key: maybe_make_key(key, ['LOCKING_SCROLL', 'LSCRL'], 132),
    lambda key: maybe_make_key(key, ['PAUSE', 'PAUS', 'BRK'], 72),
    lambda key: maybe_make_key(key, ['INSERT', 'INS'], 73),
    lambda key: maybe_make_key(key, ['HOME'], 74),
    lambda key: maybe_make_key(key, ['PGUP'], 75),
    lambda key: maybe_make_key(key, ['DELETE', 'DEL'], 76),
    lambda key: maybe_make_key(key, ['END'], 77),
    lambda key: maybe_make_key(key, ['PGDOWN', 'PGDN'], 78),
    lambda key: maybe_make_key(key, ['RIGHT', 'RGHT'], 79),
    lambda key: maybe_make_key(key, ['LEFT'], 80),
    lambda key: maybe_make_key(key, ['DOWN'], 81),
    lambda key: maybe_make_key(key, ['UP'], 82),
    # Numpad
    lambda key: maybe_make_key(key, ['NUM_LOCK', 'NUMLOCK', 'NLCK'], 83),
    # FIXME: Investigate whether this key actually works, and
    #        uncomment when/if it does.
    # lambda key: maybe_make_key(key, ['LOCKING_NUM', 'LNUM'], 131),
    lambda key: maybe_make_key(key, ['KP_SLASH', 'NUMPAD_SLASH', 'PSLS'], 84),
    lambda key: maybe_make_key(key, ['KP_ASTERISK', 'NUMPAD_ASTERISK', 'PAST'], 85),
    lambda key: maybe_make_key(key, ['KP_MINUS', 'NUMPAD_MINUS', 'PMNS'], 86),
    lambda key: maybe_make_key(key, ['KP_PLUS', 'NUMPAD_PLUS', 'PPLS'], 87),
    lambda key: maybe_make_key(key, ['KP_ENTER', 'NUMPAD_ENTER', 'PENT'], 88),
    lambda key: maybe_make_key(key, ['KP_1', 'P1', 'NUMPAD_1'], 89),
    lambda key: maybe_make_key(key, ['KP_2', 'P2', 'NUMPAD_2'], 90),
    lambda key: maybe_make_key(key, ['KP_3', 'P3', 'NUMPAD_3'], 91),
    lambda key: maybe_make_key(key, ['KP_4', 'P4', 'NUMPAD_4'], 92),
    lambda key: maybe_make_key(key, ['KP_5', 'P5', 'NUMPAD_5'], 93),
    lambda key: maybe_make_key(key, ['KP_6', 'P6', 'NUMPAD_6'], 94),
    lambda key: maybe_make_key(key, ['KP_7', 'P7', 'NUMPAD_7'], 95),
    lambda key: maybe_make_key(key, ['KP_8', 'P8', 'NUMPAD_8'], 96),
    lambda key: maybe_make_key(key, ['KP_9', 'P9', 'NUMPAD_9'], 97),
    lambda key: maybe_make_key(key, ['KP_0', 'P0', 'NUMPAD_0'], 98),
    lambda key: maybe_make_key(key, ['KP_DOT', 'PDOT', 'NUMPAD_DOT'], 99),
    lambda key: maybe_make_key(key, ['KP_EQUAL', 'PEQL', 'NUMPAD_EQUAL'], 103),
    lambda key: maybe_make_key(key, ['KP_COMMA', 'PCMM', 'NUMPAD_COMMA'], 133),
    lambda key: maybe_make_key(key, ['KP_EQUAL_AS400', 'NUMPAD_EQUAL_AS400'], 134),
    # Making life better for folks on tiny keyboards especially: exposes
    # the 'shifted' keys as raw keys. Under the hood we're still
    # sending Shift+(whatever key is normally pressed) to get these, so
    # for example `KC_AT` will hold shift and press 2.
    lambda key: maybe_make_shifted_key(key, ['EXCLAIM', 'EXLM', '!'], 30),
    lambda key: maybe_make_shifted_key(key, ['AT', '@'], 31),
    lambda key: maybe_make_shifted_key(key, ['HASH', 'POUND', '#'], 32),
    lambda key: maybe_make_shifted_key(key, ['DOLLAR', 'DLR', '$'], 33),
    lambda key: maybe_make_shifted_key(key, ['PERCENT', 'PERC', '%'], 34),
    lambda key: maybe_make_shifted_key(key, ['CIRCUMFLEX', 'CIRC', '^'], 35),
    lambda key: maybe_make_shifted_key(key, ['AMPERSAND', 'AMPR', '&'], 36),
    lambda key: maybe_make_shifted_key(key, ['ASTERISK', 'ASTR', '*'], 37),
    lambda key: maybe_make_shifted_key(key, ['LEFT_PAREN', 'LPRN', '('], 38),
    lambda key: maybe_make_shifted_key(key, ['RIGHT_PAREN', 'RPRN', ')'], 39),
    lambda key: maybe_make_shifted_key(key, ['UNDERSCORE', 'UNDS', '_'], 45),
    lambda key: maybe_make_shifted_key(key, ['PLUS', '+'], 46),
    lambda key: maybe_make_shifted_key(key, ['LEFT_CURLY_BRACE', 'LCBR', '{'], 47),
    lambda key: maybe_make_shifted_key(key, ['RIGHT_CURLY_BRACE', 'RCBR', '}'], 48),
    lambda key: maybe_make_shifted_key(key, ['PIPE', '|'], 49),
    lambda key: maybe_make_shifted_key(key, ['COLON', 'COLN', ':'], 51),
    lambda key: maybe_make_shifted_key(key, ['DOUBLE_QUOTE', 'DQUO', 'DQT', '"'], 52),
    lambda key: maybe_make_shifted_key(key, ['TILDE', 'TILD', '~'], 53),
    lambda key: maybe_make_shifted_key(key, ['LEFT_ANGLE_BRACKET', 'LABK', '<'], 54),
    lambda key: maybe_make_shifted_key(key, ['RIGHT_ANGLE_BRACKET', 'RABK', '>'], 55),
    lambda key: maybe_make_shifted_key(key, ['QUESTION', 'QUES', '?'], 56),
    # International
    lambda key: maybe_make_key(key, ['NONUS_HASH', 'NUHS'], 50),
    lambda key: maybe_make_key(key, ['NONUS_BSLASH', 'NUBS'], 100),
    lambda key: maybe_make_key(key, ['APP', 'APPLICATION', 'SEL', 'WINMENU'], 101),
    lambda key: maybe_make_key(key, ['INT1', 'RO'], 135),
    lambda key: maybe_make_key(key, ['INT2', 'KANA'], 136),
    lambda key: maybe_make_key(key, ['INT3', 'JYEN'], 137),
    lambda key: maybe_make_key(key, ['INT4', 'HENK'], 138),
    lambda key: maybe_make_key(key, ['INT5', 'MHEN'], 139),
    lambda key: maybe_make_key(key, ['INT6'], 140),
    lambda key: maybe_make_key(key, ['INT7'], 141),
    lambda key: maybe_make_key(key, ['INT8'], 142),
    lambda key: maybe_make_key(key, ['INT9'], 143),
    lambda key: maybe_make_key(key, ['LANG1', 'HAEN'], 144),
    lambda key: maybe_make_key(key, ['LANG2', 'HAEJ'], 145),
    lambda key: maybe_make_key(key, ['LANG3'], 146),
    lambda key: maybe_make_key(key, ['LANG4'], 147),
    lambda key: maybe_make_key(key, ['LANG5'], 148),
    lambda key: maybe_make_key(key, ['LANG6'], 149),
    lambda key: maybe_make_key(key, ['LANG7'], 150),
    lambda key: maybe_make_key(key, ['LANG8'], 151),
    lambda key: maybe_make_key(key, ['LANG9'], 152),
    # Consumer ("media") keys. Most known keys aren't supported here. A much
    # longer list used to exist in this file, but the codes were almost
    # certainly incorrect, conflicting with each other, or otherwise
    # 'weird'. We'll add them back in piecemeal as needed. PRs welcome.
    #
    # A super useful reference for these is
    # http://www.freebsddiary.org/APC/usb_hid_usages.php
    # Note that currently we only have the PC codes. Recent MacOS versions
    # seem to support PC media keys, so I don't know how much value we
    # would get out of adding the old Apple-specific consumer codes, but
    # again, PRs welcome if the lack of them impacts you.
    lambda key: maybe_make_consumer_key(key, ['AUDIO_MUTE', 'MUTE'], 226),  # 0xE2
    lambda key: maybe_make_consumer_key(key, ['AUDIO_VOL_UP', 'VOLU'], 233),  # 0xE9
    lambda key: maybe_make_consumer_key(key, ['AUDIO_VOL_DOWN', 'VOLD'], 234),  # 0xEA
    lambda key: maybe_make_consumer_key(key, ['MEDIA_NEXT_TRACK', 'MNXT'], 181),  # 0xB5
    lambda key: maybe_make_consumer_key(key, ['MEDIA_PREV_TRACK', 'MPRV'], 182),  # 0xB6
    lambda key: maybe_make_consumer_key(key, ['MEDIA_STOP', 'MSTP'], 183),  # 0xB7
    lambda key: maybe_make_consumer_key(
        key, ['MEDIA_PLAY_PAUSE', 'MPLY'], 205
    ),  # 0xCD (this may not be right)
    lambda key: maybe_make_consumer_key(key, ['MEDIA_EJECT', 'EJCT'], 184),  # 0xB8
    lambda key: maybe_make_consumer_key(
        key, ['MEDIA_FAST_FORWARD', 'MFFD'], 179
    ),  # 0xB3
    lambda key: maybe_make_consumer_key(key, ['MEDIA_REWIND', 'MRWD'], 180),  # 0xB4
]


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

    def __getitem__(self, key):
        if DEBUG_OUTPUT:
            print(f'__getitem__ {key}')
        try:
            return self.__cache[key]
        except KeyError:
            if DEBUG_OUTPUT:
                print(f'{key} not found. Attempting to construct from known.')

            for func in KEY_FUNCTIONS:
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

        return Key(
            code=self.code,
            has_modifiers=self.has_modifiers,
            no_press=no_press,
            no_release=no_release,
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


def make_key(code=None, names=[], type=KEY_SIMPLE, **kwargs):
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
    names=[],
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
