try:
    from typing import Callable, Optional, Tuple
except ImportError:
    pass

from micropython import const

import kmk.handlers.stock as handlers
from kmk.utils import Debug

# Type aliases / forward declaration; can't use the proper types because of circular imports.
Keyboard = object
Key = object


FIRST_KMK_INTERNAL_KEY = const(1000)
NEXT_AVAILABLE_KEY = 1000

ALL_ALPHAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALL_NUMBERS = '1234567890'
# since KC.1 isn't valid Python, alias to KC.N1
ALL_NUMBER_ALIASES = tuple(f'N{x}' for x in ALL_NUMBERS)

debug = Debug(__name__)


class Axis:
    def __init__(self, code: int) -> None:
        self.code = code
        self.delta = 0

    def __repr__(self) -> str:
        return f'Axis(code={self.code}, delta={self.delta})'

    def move(self, keyboard: Keyboard, delta: int):
        self.delta += delta
        if self.delta:
            keyboard.axes.add(self)
            keyboard.hid_pending = True
        else:
            keyboard.axes.discard(self)


class AX:
    P = Axis(3)
    W = Axis(2)
    X = Axis(0)
    Y = Axis(1)


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
                validator,
                names,
                *constructor_args,
                **constructor_kwargs,
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
            return make_key(code=code, names=names, key_type=ModifierKey)


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
            return make_key(
                code=code, names=names, key_type=ModifiedKey, modifier=KC.LSFT
            )


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


def maybe_make_firmware_key(candidate: str) -> Optional[Key]:
    keys = (
        ((('BLE_REFRESH',), handlers.ble_refresh)),
        ((('BLE_DISCONNECT',), handlers.ble_disconnect)),
        ((('BOOTLOADER',), handlers.bootloader)),
        ((('DEBUG', 'DBG'), handlers.debug_pressed)),
        ((('HID_SWITCH', 'HID'), handlers.hid_switch)),
        ((('RELOAD', 'RLD'), handlers.reload)),
        ((('RESET',), handlers.reset)),
        ((('ANY',), handlers.any_pressed)),
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
)


class KeyAttrDict:
    # Instead of relying on the uncontrollable availability of a big chunk of
    # contiguous memory for key caching, we can manually fragment the cache into
    # reasonably small partitions. The partition size is chosen from the magic
    # values of CPs hash allocation sizes.
    # (https://github.com/adafruit/circuitpython/blob/main/py/map.c, 2023-02)
    __partition_size = 37
    __cache = [{}]

    def __iter__(self):
        for partition in self.__cache:
            for name in partition:
                yield name

    def __setitem__(self, name: str, key: Key):
        # Overwrite existing reference.
        for partition in self.__cache:
            if name in partition:
                partition[name] = key
                return key

        # Insert new reference.
        if len(self.__cache[-1]) >= self.__partition_size:
            self.__cache.append({})
        self.__cache[-1][name] = key
        return key

    def __getattr__(self, name: str):
        return self.__getitem__(name)

    def get(self, name: str, default: Optional[Key] = None):
        try:
            return self.__getitem__(name)
        except Exception:
            return default

    def clear(self):
        self.__cache.clear()
        self.__cache.append({})

    def __getitem__(self, name: str):
        for partition in self.__cache:
            if name in partition:
                return partition[name]

        for func in KEY_GENERATORS:
            maybe_key = func(name)
            if maybe_key:
                break

        if not maybe_key:
            if debug.enabled:
                debug(f'Invalid key: {name}')
            return KC.NO

        if debug.enabled:
            debug(f'{name}: {maybe_key}')

        return maybe_key


# Global state, will be filled in throughout this file, and
# anywhere the user creates custom keys
KC = KeyAttrDict()


class Key:
    def __init__(
        self,
        code: int,
        on_press: Callable[
            [object, Key, Keyboard, ...], None
        ] = handlers.default_pressed,
        on_release: Callable[
            [object, Key, Keyboard, ...], None
        ] = handlers.default_released,
        meta: object = object(),
    ):
        self.code = code

        self._on_press = on_press
        self._on_release = on_release
        self.meta = meta

    def __call__(self) -> Key:
        return self

    def __repr__(self):
        return f'Key(code={self.code})'

    def on_press(self, keyboard: Keyboard, coord_int: Optional[int] = None) -> None:
        self._on_press(self, keyboard, KC, coord_int)

    def on_release(self, keyboard: Keyboard, coord_int: Optional[int] = None) -> None:
        self._on_release(self, keyboard, KC, coord_int)


class ModifierKey(Key):
    def __call__(self, key: Key) -> Key:
        # don't duplicate when applying the same modifier twice
        if (
            isinstance(key, ModifiedKey)
            and key.modifier.code & self.code == key.modifier.code
        ):
            return key
        elif isinstance(key, ModifierKey) and key.code & self.code == key.code:
            return key

        return ModifiedKey(key, self)

    def __repr__(self):
        return f'ModifierKey(code={self.code})'


class ModifiedKey(Key):
    meta = None
    code = -1

    def __init__(self, code: [Key, int], modifier: [ModifierKey]):
        # generate from code by maybe_make_shifted_key
        if isinstance(code, int):
            key = Key(code=code)
        else:
            key = code

        # stack modified keys
        if isinstance(key, ModifiedKey):
            modifier = ModifierKey(key.modifier.code | modifier.code)
            key = key.key

        self.key = key
        self.modifier = modifier

    def on_press(self, keyboard: Keyboard, coord_int: Optional[int] = None) -> None:
        self.modifier.on_press(keyboard, coord_int)
        self.key.on_press(keyboard, coord_int)

    def on_release(self, keyboard: Keyboard, coord_int: Optional[int] = None) -> None:
        self.key.on_release(keyboard, coord_int)
        self.modifier.on_release(keyboard, coord_int)

    def __repr__(self):
        return (
            'ModifiedKey(key='
            + str(self.key)
            + ', modifier='
            + str(self.modifier)
            + ')'
        )


class ConsumerKey(Key):
    pass


class MouseKey(Key):
    pass


def make_key(
    code: Optional[int] = None,
    names: Tuple[str, ...] = tuple(),  # NOQA
    key_type: Key = Key,
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

    if code is None:
        code = NEXT_AVAILABLE_KEY
        NEXT_AVAILABLE_KEY += 1
    elif code >= FIRST_KMK_INTERNAL_KEY:
        # Try to ensure future auto-generated internal keycodes won't
        # be overridden by continuing to +1 the sequence from the provided
        # code
        NEXT_AVAILABLE_KEY = max(NEXT_AVAILABLE_KEY, code + 1)

    key = key_type(code=code, **kwargs)

    for name in names:
        KC[name] = key

    return key


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
                NEXT_AVAILABLE_KEY,
                *constructor_args,
                meta=meta,
                **constructor_kwargs,
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
