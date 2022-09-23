try:
    from typing import Callable, Optional, Tuple
except ImportError:
    pass

from micropython import const

import kmk.handlers.stock as handlers
from kmk.consts import UnicodeMode
from kmk.key_validators import key_seq_sleep_validator, unicode_mode_key_validator
from kmk.types import UnicodeModeKeyMeta
from kmk.utils import Debug

# Type aliases / forward declaration; can't use the proper types because of circular imports.
Keyboard = object
Key = object


class KeyType:
    SIMPLE = const(0)
    MODIFIER = const(1)
    CONSUMER = const(2)


FIRST_KMK_INTERNAL_KEY = const(1000)
NEXT_AVAILABLE_KEY = 1000

ALL_ALPHAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALL_NUMBERS = '1234567890'
# since KC.1 isn't valid Python, alias to KC.N1
ALL_NUMBER_ALIASES = tuple(f'N{x}' for x in ALL_NUMBERS)

debug = Debug(__name__)


def maybe_make_key(
    code: Optional[int],
    names: Tuple[str, ...],
    *args,
    **kwargs,
) -> Callable[[str], Key]:
    def closure(candidate):
        if candidate in names:
            return make_key(code=code, names=names, *args, **kwargs)

    return closure


def maybe_make_argumented_key(
    validator=lambda *validator_args, **validator_kwargs: object(),
    names: Tuple[str, ...] = tuple(),  # NOQA
    *constructor_args,
    **constructor_kwargs,
) -> Callable[[str], Key]:
    def closure(candidate):
        if candidate in names:
            return make_argumented_key(
                validator, names, *constructor_args, **constructor_kwargs
            )

    return closure


def maybe_make_no_key(candidate: str) -> Optional[Key]:
    # NO and TRNS are functionally identical in how they (don't) mutate
    # the state, but are tracked semantically separately, so create
    # two keys with the exact same functionality
    keys = (
        ('NO', 'XXXXXXX'),
        ('TRANSPARENT', 'TRNS'),
    )

    for names in keys:
        if candidate in names:
            return make_key(
                names=names,
                on_press=handlers.passthrough,
                on_release=handlers.passthrough,
            )


def maybe_make_alpha_key(candidate: str) -> Optional[Key]:
    if len(candidate) != 1:
        return

    candidate_upper = candidate.upper()
    if candidate_upper in ALL_ALPHAS:
        return make_key(
            code=4 + ALL_ALPHAS.index(candidate_upper),
            names=(candidate_upper, candidate.lower()),
        )


def maybe_make_numeric_key(candidate: str) -> Optional[Key]:
    if candidate in ALL_NUMBERS or candidate in ALL_NUMBER_ALIASES:
        try:
            offset = ALL_NUMBERS.index(candidate)
        except ValueError:
            offset = ALL_NUMBER_ALIASES.index(candidate)

        return make_key(
            code=30 + offset,
            names=(ALL_NUMBERS[offset], ALL_NUMBER_ALIASES[offset]),
        )


def maybe_make_mod_key(candidate: str) -> Optional[Key]:
    # MEH = LCTL | LALT | LSFT
    # HYPR = LCTL | LALT | LSFT | LGUI
    mods = (
        (0x01, ('LEFT_CONTROL', 'LCTRL', 'LCTL')),
        (0x02, ('LEFT_SHIFT', 'LSHIFT', 'LSFT')),
        (0x04, ('LEFT_ALT', 'LALT', 'LOPT')),
        (0x08, ('LEFT_SUPER', 'LGUI', 'LCMD', 'LWIN')),
        (0x10, ('RIGHT_CONTROL', 'RCTRL', 'RCTL')),
        (0x20, ('RIGHT_SHIFT', 'RSHIFT', 'RSFT')),
        (0x40, ('RIGHT_ALT', 'RALT', 'ROPT')),
        (0x80, ('RIGHT_SUPER', 'RGUI', 'RCMD', 'RWIN')),
        (0x07, ('MEH',)),
        (0x0F, ('HYPER', 'HYPR')),
    )

    for code, names in mods:
        if candidate in names:
            return make_key(code=code, names=names, type=KeyType.MODIFIER)


def maybe_make_more_ascii(candidate: str) -> Optional[Key]:
    codes = (
        (40, ('ENTER', 'ENT', '\n')),
        (41, ('ESCAPE', 'ESC')),
        (42, ('BACKSPACE', 'BSPACE', 'BSPC', 'BKSP')),
        (43, ('TAB', '\t')),
        (44, ('SPACE', 'SPC', ' ')),
        (45, ('MINUS', 'MINS', '-')),
        (46, ('EQUAL', 'EQL', '=')),
        (47, ('LBRACKET', 'LBRC', '[')),
        (48, ('RBRACKET', 'RBRC', ']')),
        (49, ('BACKSLASH', 'BSLASH', 'BSLS', '\\')),
        (51, ('SEMICOLON', 'SCOLON', 'SCLN', ';')),
        (52, ('QUOTE', 'QUOT', "'")),
        (53, ('GRAVE', 'GRV', 'ZKHK', '`')),
        (54, ('COMMA', 'COMM', ',')),
        (55, ('DOT', '.')),
        (56, ('SLASH', 'SLSH', '/')),
    )

    for code, names in codes:
        if candidate in names:
            return make_key(code=code, names=names)


def maybe_make_fn_key(candidate: str) -> Optional[Key]:
    codes = (
        (58, ('F1',)),
        (59, ('F2',)),
        (60, ('F3',)),
        (61, ('F4',)),
        (62, ('F5',)),
        (63, ('F6',)),
        (64, ('F7',)),
        (65, ('F8',)),
        (66, ('F9',)),
        (67, ('F10',)),
        (68, ('F11',)),
        (69, ('F12',)),
        (104, ('F13',)),
        (105, ('F14',)),
        (106, ('F15',)),
        (107, ('F16',)),
        (108, ('F17',)),
        (109, ('F18',)),
        (110, ('F19',)),
        (111, ('F20',)),
        (112, ('F21',)),
        (113, ('F22',)),
        (114, ('F23',)),
        (115, ('F24',)),
    )

    for code, names in codes:
        if candidate in names:
            return make_key(code=code, names=names)


def maybe_make_navlock_key(candidate: str) -> Optional[Key]:
    codes = (
        (57, ('CAPS_LOCK', 'CAPSLOCK', 'CLCK', 'CAPS')),
        # FIXME: Investigate whether this key actually works, and
        #        uncomment when/if it does.
        # (130, ('LOCKING_CAPS', 'LCAP')),
        (70, ('PRINT_SCREEN', 'PSCREEN', 'PSCR')),
        (71, ('SCROLL_LOCK', 'SCROLLLOCK', 'SLCK')),
        # FIXME: Investigate whether this key actually works, and
        #        uncomment when/if it does.
        # (132, ('LOCKING_SCROLL', 'LSCRL')),
        (72, ('PAUSE', 'PAUS', 'BRK')),
        (73, ('INSERT', 'INS')),
        (74, ('HOME',)),
        (75, ('PGUP',)),
        (76, ('DELETE', 'DEL')),
        (77, ('END',)),
        (78, ('PGDOWN', 'PGDN')),
        (79, ('RIGHT', 'RGHT')),
        (80, ('LEFT',)),
        (81, ('DOWN',)),
        (82, ('UP',)),
    )

    for code, names in codes:
        if candidate in names:
            return make_key(code=code, names=names)


def maybe_make_numpad_key(candidate: str) -> Optional[Key]:
    codes = (
        (83, ('NUM_LOCK', 'NUMLOCK', 'NLCK')),
        (84, ('KP_SLASH', 'NUMPAD_SLASH', 'PSLS')),
        (85, ('KP_ASTERISK', 'NUMPAD_ASTERISK', 'PAST')),
        (86, ('KP_MINUS', 'NUMPAD_MINUS', 'PMNS')),
        (87, ('KP_PLUS', 'NUMPAD_PLUS', 'PPLS')),
        (88, ('KP_ENTER', 'NUMPAD_ENTER', 'PENT')),
        (89, ('KP_1', 'P1', 'NUMPAD_1')),
        (90, ('KP_2', 'P2', 'NUMPAD_2')),
        (91, ('KP_3', 'P3', 'NUMPAD_3')),
        (92, ('KP_4', 'P4', 'NUMPAD_4')),
        (93, ('KP_5', 'P5', 'NUMPAD_5')),
        (94, ('KP_6', 'P6', 'NUMPAD_6')),
        (95, ('KP_7', 'P7', 'NUMPAD_7')),
        (96, ('KP_8', 'P8', 'NUMPAD_8')),
        (97, ('KP_9', 'P9', 'NUMPAD_9')),
        (98, ('KP_0', 'P0', 'NUMPAD_0')),
        (99, ('KP_DOT', 'PDOT', 'NUMPAD_DOT')),
        (103, ('KP_EQUAL', 'PEQL', 'NUMPAD_EQUAL')),
        (133, ('KP_COMMA', 'PCMM', 'NUMPAD_COMMA')),
        (134, ('KP_EQUAL_AS400', 'NUMPAD_EQUAL_AS400')),
    )

    for code, names in codes:
        if candidate in names:
            return make_key(code=code, names=names)


def maybe_make_shifted_key(candidate: str) -> Optional[Key]:
    codes = (
        (30, ('EXCLAIM', 'EXLM', '!')),
        (31, ('AT', '@')),
        (32, ('HASH', 'POUND', '#')),
        (33, ('DOLLAR', 'DLR', '$')),
        (34, ('PERCENT', 'PERC', '%')),
        (35, ('CIRCUMFLEX', 'CIRC', '^')),
        (36, ('AMPERSAND', 'AMPR', '&')),
        (37, ('ASTERISK', 'ASTR', '*')),
        (38, ('LEFT_PAREN', 'LPRN', '(')),
        (39, ('RIGHT_PAREN', 'RPRN', ')')),
        (45, ('UNDERSCORE', 'UNDS', '_')),
        (46, ('PLUS', '+')),
        (47, ('LEFT_CURLY_BRACE', 'LCBR', '{')),
        (48, ('RIGHT_CURLY_BRACE', 'RCBR', '}')),
        (49, ('PIPE', '|')),
        (51, ('COLON', 'COLN', ':')),
        (52, ('DOUBLE_QUOTE', 'DQUO', 'DQT', '"')),
        (53, ('TILDE', 'TILD', '~')),
        (54, ('LEFT_ANGLE_BRACKET', 'LABK', '<')),
        (55, ('RIGHT_ANGLE_BRACKET', 'RABK', '>')),
        (56, ('QUESTION', 'QUES', '?')),
    )

    for code, names in codes:
        if candidate in names:
            return make_key(code=code, names=names, has_modifiers={KC.LSFT.code})


def maybe_make_international_key(candidate: str) -> Optional[Key]:
    codes = (
        (50, ('NONUS_HASH', 'NUHS')),
        (100, ('NONUS_BSLASH', 'NUBS')),
        (101, ('APP', 'APPLICATION', 'SEL', 'WINMENU')),
        (135, ('INT1', 'RO')),
        (136, ('INT2', 'KANA')),
        (137, ('INT3', 'JYEN')),
        (138, ('INT4', 'HENK')),
        (139, ('INT5', 'MHEN')),
        (140, ('INT6',)),
        (141, ('INT7',)),
        (142, ('INT8',)),
        (143, ('INT9',)),
        (144, ('LANG1', 'HAEN')),
        (145, ('LANG2', 'HAEJ')),
        (146, ('LANG3',)),
        (147, ('LANG4',)),
        (148, ('LANG5',)),
        (149, ('LANG6',)),
        (150, ('LANG7',)),
        (151, ('LANG8',)),
        (152, ('LANG9',)),
    )

    for code, names in codes:
        if candidate in names:
            return make_key(code=code, names=names)


def maybe_make_unicode_key(candidate: str) -> Optional[Key]:
    keys = (
        (
            ('UC_MODE_NOOP', 'UC_DISABLE'),
            handlers.uc_mode_pressed,
            UnicodeModeKeyMeta(UnicodeMode.NOOP),
        ),
        (
            ('UC_MODE_LINUX', 'UC_MODE_IBUS'),
            handlers.uc_mode_pressed,
            UnicodeModeKeyMeta(UnicodeMode.IBUS),
        ),
        (
            ('UC_MODE_MACOS', 'UC_MODE_OSX', 'US_MODE_RALT'),
            handlers.uc_mode_pressed,
            UnicodeModeKeyMeta(UnicodeMode.RALT),
        ),
        (
            ('UC_MODE_WINC',),
            handlers.uc_mode_pressed,
            UnicodeModeKeyMeta(UnicodeMode.WINC),
        ),
    )

    for names, handler, meta in keys:
        if candidate in names:
            return make_key(names=names, on_press=handler, meta=meta)

    if candidate in ('UC_MODE',):
        return make_argumented_key(
            names=('UC_MODE',),
            validator=unicode_mode_key_validator,
            on_press=handlers.uc_mode_pressed,
        )


def maybe_make_firmware_key(candidate: str) -> Optional[Key]:
    keys = (
        ((('BLE_REFRESH',), handlers.ble_refresh)),
        ((('BOOTLOADER',), handlers.bootloader)),
        ((('DEBUG', 'DBG'), handlers.debug_pressed)),
        ((('HID_SWITCH', 'HID'), handlers.hid_switch)),
        ((('RELOAD', 'RLD'), handlers.reload)),
        ((('RESET',), handlers.reset)),
    )

    for names, handler in keys:
        if candidate in names:
            return make_key(names=names, on_press=handler)


KEY_GENERATORS = (
    maybe_make_no_key,
    maybe_make_alpha_key,
    maybe_make_numeric_key,
    maybe_make_firmware_key,
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
    maybe_make_mod_key,
    # More ASCII standard keys
    maybe_make_more_ascii,
    # Function Keys
    maybe_make_fn_key,
    # Lock Keys, Navigation, etc.
    maybe_make_navlock_key,
    # Numpad
    # FIXME: Investigate whether this key actually works, and
    #        uncomment when/if it does.
    # maybe_make_key(131, ('LOCKING_NUM', 'LNUM')),
    maybe_make_numpad_key,
    # Making life better for folks on tiny keyboards especially: exposes
    # the 'shifted' keys as raw keys. Under the hood we're still
    # sending Shift+(whatever key is normally pressed) to get these, so
    # for example `KC_AT` will hold shift and press 2.
    maybe_make_shifted_key,
    # International
    maybe_make_international_key,
    maybe_make_unicode_key,
)


class KeyAttrDict:
    __cache = {}

    def __iter__(self):
        return self.__cache.__iter__()

    def __setitem__(self, key: str, value: Key):
        self.__cache.__setitem__(key, value)

    def __getattr__(self, key: Key):
        return self.__getitem__(key)

    def get(self, key: Key, default: Optional[Key] = None):
        try:
            return self.__getitem__(key)
        except Exception:
            return default

    def clear(self):
        self.__cache.clear()

    def __getitem__(self, key: Key):
        try:
            return self.__cache[key]
        except KeyError:
            pass

        for func in KEY_GENERATORS:
            maybe_key = func(key)
            if maybe_key:
                break
        else:
            raise ValueError(f'Invalid key: {key}')

        if debug.enabled:
            debug(f'{key}: {maybe_key}')

        return self.__cache[key]


# Global state, will be filled in throughout this file, and
# anywhere the user creates custom keys
KC = KeyAttrDict()


class Key:
    def __init__(
        self,
        code: int,
        has_modifiers: Optional[list[Key, ...]] = None,
        no_press: bool = False,
        no_release: bool = False,
        on_press: Callable[
            [object, Key, Keyboard, ...], None
        ] = handlers.default_pressed,
        on_release: Callable[
            [object, Key, Keyboard, ...], None
        ] = handlers.default_released,
        meta: object = object(),
    ):
        self.code = code
        self.has_modifiers = has_modifiers
        # cast to bool() in case we get a None value
        self.no_press = bool(no_press)
        self.no_release = bool(no_release)

        self._handle_press = on_press
        self._handle_release = on_release
        self.meta = meta

    def __call__(
        self, no_press: Optional[bool] = None, no_release: Optional[bool] = None
    ) -> Key:
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
        return f'Key(code={self.code}, has_modifiers={self.has_modifiers})'

    def on_press(self, keyboard: Keyboard, coord_int: Optional[int] = None) -> None:
        if hasattr(self, '_pre_press_handlers'):
            for fn in self._pre_press_handlers:
                if not fn(self, keyboard, KC, coord_int):
                    return

        self._handle_press(self, keyboard, KC, coord_int)

        if hasattr(self, '_post_press_handlers'):
            for fn in self._post_press_handlers:
                fn(self, keyboard, KC, coord_int)

    def on_release(self, keyboard: Keyboard, coord_int: Optional[int] = None) -> None:
        if hasattr(self, '_pre_release_handlers'):
            for fn in self._pre_release_handlers:
                if not fn(self, keyboard, KC, coord_int):
                    return

        self._handle_release(self, keyboard, KC, coord_int)

        if hasattr(self, '_post_release_handlers'):
            for fn in self._post_release_handlers:
                fn(self, keyboard, KC, coord_int)

    def clone(self) -> Key:
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

    def before_press_handler(self, fn: Callable[[Key, Keyboard, ...], bool]) -> None:
        '''
        Attach a callback to be run prior to the on_press handler for this key.
        Receives the following:

        - self (this Key instance)
        - state (the current InternalState)
        - KC (the global KC lookup table, for convenience)
        - coord_int (an internal integer representation of the matrix coordinate
          for the pressed key - this is likely not useful to end users, but is
          provided for consistency with the internal handlers)

        If return value of the provided callback is evaluated to False, press
        processing is cancelled. Exceptions are _not_ caught, and will likely
        crash KMK if not handled within your function.

        These handlers are run in attachment order: handlers provided by earlier
        calls of this method will be executed before those provided by later calls.
        '''

        if not hasattr(self, '_pre_press_handlers'):
            self._pre_press_handlers = []
        self._pre_press_handlers.append(fn)

    def after_press_handler(self, fn: Callable[[Key, Keyboard, ...], bool]) -> None:
        '''
        Attach a callback to be run after the on_release handler for this key.
        Receives the following:

        - self (this Key instance)
        - state (the current InternalState)
        - KC (the global KC lookup table, for convenience)
        - coord_int (an internal integer representation of the matrix coordinate
          for the pressed key - this is likely not useful to end users, but is
          provided for consistency with the internal handlers)

        The return value of the provided callback is discarded. Exceptions are _not_
        caught, and will likely crash KMK if not handled within your function.

        These handlers are run in attachment order: handlers provided by earlier
        calls of this method will be executed before those provided by later calls.
        '''

        if not hasattr(self, '_post_press_handlers'):
            self._post_press_handlers = []
        self._post_press_handlers.append(fn)

    def before_release_handler(self, fn: Callable[[Key, Keyboard, ...], bool]) -> None:
        '''
        Attach a callback to be run prior to the on_release handler for this
        key. Receives the following:

        - self (this Key instance)
        - state (the current InternalState)
        - KC (the global KC lookup table, for convenience)
        - coord_int (an internal integer representation of the matrix coordinate
          for the pressed key - this is likely not useful to end users, but is
          provided for consistency with the internal handlers)

        If return value of the provided callback evaluates to False, the release
        processing is cancelled. Exceptions are _not_ caught, and will likely crash
        KMK if not handled within your function.

        These handlers are run in attachment order: handlers provided by earlier
        calls of this method will be executed before those provided by later calls.
        '''

        if not hasattr(self, '_pre_release_handlers'):
            self._pre_release_handlers = []
        self._pre_release_handlers.append(fn)

    def after_release_handler(self, fn: Callable[[Key, Keyboard, ...], bool]) -> None:
        '''
        Attach a callback to be run after the on_release handler for this key.
        Receives the following:

        - self (this Key instance)
        - state (the current InternalState)
        - KC (the global KC lookup table, for convenience)
        - coord_int (an internal integer representation of the matrix coordinate
          for the pressed key - this is likely not useful to end users, but is
          provided for consistency with the internal handlers)

        The return value of the provided callback is discarded. Exceptions are _not_
        caught, and will likely crash KMK if not handled within your function.

        These handlers are run in attachment order: handlers provided by earlier
        calls of this method will be executed before those provided by later calls.
        '''

        if not hasattr(self, '_post_release_handlers'):
            self._post_release_handlers = []
        self._post_release_handlers.append(fn)


class ModifierKey(Key):
    FAKE_CODE = const(-1)

    def __call__(
        self,
        modified_key: Optional[Key] = None,
        no_press: Optional[bool] = None,
        no_release: Optional[bool] = None,
    ) -> Key:
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
        return f'ModifierKey(code={self.code}, has_modifiers={self.has_modifiers})'


class ConsumerKey(Key):
    pass


def make_key(
    code: Optional[int] = None,
    names: Tuple[str, ...] = tuple(),  # NOQA
    type: KeyType = KeyType.SIMPLE,
    **kwargs,
) -> Key:
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

    if type == KeyType.SIMPLE:
        constructor = Key
    elif type == KeyType.MODIFIER:
        constructor = ModifierKey
    elif type == KeyType.CONSUMER:
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

    return key


def make_mod_key(code: int, names: Tuple[str, ...], *args, **kwargs) -> Key:
    return make_key(code, names, *args, **kwargs, type=KeyType.MODIFIER)


def make_shifted_key(code: int, names: Tuple[str, ...]) -> Key:
    return make_key(code, names, has_modifiers={KC.LSFT.code})


def make_consumer_key(*args, **kwargs) -> Key:
    return make_key(*args, **kwargs, type=KeyType.CONSUMER)


# Argumented keys are implicitly internal, so auto-gen of code
# is almost certainly the best plan here
def make_argumented_key(
    validator: object = lambda *validator_args, **validator_kwargs: object(),
    names: Tuple[str, ...] = tuple(),  # NOQA
    *constructor_args,
    **constructor_kwargs,
) -> Key:
    global NEXT_AVAILABLE_KEY

    def _argumented_key(*user_args, **user_kwargs) -> Key:
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
