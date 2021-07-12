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


class InfiniteLoopDetected(Exception):
    pass


# this is a bit of an FP style thing - combining a pipe operator a-la F# with
# a bootleg Maybe monad to clean up these make_key sequences
def left_pipe_until_some(candidate, functor, *args_iter):
    for args in args_iter:
        result = functor(candidate, *args)
        if result is not None:
            return result


def first_truthy(candidate, *funcs):
    for func in funcs:
        result = func(candidate)
        if result is not None:
            return result


def maybe_make_mod_key(candidate, code, names):
    if candidate in names:
        return make_mod_key(code=code, names=names)


def maybe_make_key(candidate, code, names):
    if candidate in names:
        return make_key(code=code, names=names)


def maybe_make_shifted_key(candidate, target_name, names):
    if candidate in names:
        return make_shifted_key(target_name=target_name, names=names)


def maybe_make_consumer_key(candidate, code, names):
    if candidate in names:
        return make_consumer_key(code=code, names=names)


class KeyAttrDict(AttrDict):
    def __getattr__(self, key, depth=0):
        if depth > 1:
            raise InfiniteLoopDetected()

        try:
            return super(KeyAttrDict, self).__getattr__(key)
        except Exception:
            pass

        # Basic ASCII letters/numbers don't need anything fancy, so check those
        # in the laziest way
        if key in ALL_ALPHAS:
            make_key(code=4 + ALL_ALPHAS.index(key), names=(key,))
        elif key in ALL_NUMBERS or key in ALL_NUMBER_ALIASES:
            try:
                offset = ALL_NUMBERS.index(key)
            except ValueError:
                offset = ALL_NUMBER_ALIASES.index(key)

            names = (ALL_NUMBERS[offset], ALL_NUMBER_ALIASES[offset])
            make_key(code=30 + offset, names=names)

        # Now try all the other weird special cases to get them out of our way:

        # Internal, diagnostic, or auxiliary/enhanced keys

        # NO and TRNS are functionally identical in how they (don't) mutate
        # the state, but are tracked semantically separately, so create
        # two keys with the exact same functionality
        elif key in ('NO', 'XXXXXXX'):
            make_key(
                names=('NO', 'XXXXXXX'),
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
            maybe_key = first_truthy(
                key,
                # Modifiers
                lambda key: left_pipe_until_some(
                    key,
                    maybe_make_mod_key,
                    (0x01, ('LEFT_CONTROL', 'LCTRL', 'LCTL')),
                    (0x02, ('LEFT_SHIFT', 'LSHIFT', 'LSFT')),
                    (0x04, ('LEFT_ALT', 'LALT')),
                    (0x08, ('LEFT_SUPER', 'LGUI', 'LCMD', 'LWIN')),
                    (0x10, ('RIGHT_CONTROL', 'RCTRL', 'RCTL')),
                    (0x20, ('RIGHT_SHIFT', 'RSHIFT', 'RSFT')),
                    (0x40, ('RIGHT_ALT', 'RALT')),
                    (0x80, ('RIGHT_SUPER', 'RGUI', 'RCMD', 'RWIN')),
                    # MEH = LCTL | LALT | LSFT# MEH = LCTL |
                    (0x07, ('MEH',)),
                    # HYPR = LCTL | LALT | LSFT | LGUI
                    (0x0F, ('HYPER', 'HYPR')),
                ),
                lambda key: left_pipe_until_some(
                    key,
                    maybe_make_key,
                    # More ASCII standard keys
                    (40, ('ENTER', 'ENT', '\n')),
                    (41, ('ESCAPE', 'ESC')),
                    (42, ('BACKSPACE', 'BSPC', 'BKSP')),
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
                    (56, ('SLASH', 'SLSH')),
                    # Function Keys
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
                    # Lock Keys, Navigation, etc.
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
                    # Numpad
                    (83, ('NUM_LOCK', 'NUMLOCK', 'NLCK')),
                    # FIXME: Investigate whether this key actually works, and
                    #        uncomment when/if it does.
                    # (131, names=('LOCKING_NUM', 'LNUM')),
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
                ),
                # Making life better for folks on tiny keyboards especially: exposes
                # the 'shifted' keys as raw keys. Under the hood we're still
                # sending Shift+(whatever key is normally pressed) to get these, so
                # for example `KC_AT` will hold shift and press 2.
                lambda key: left_pipe_until_some(
                    key,
                    maybe_make_shifted_key,
                    ('GRAVE', ('TILDE', 'TILD', '~')),
                    ('1', ('EXCLAIM', 'EXLM', '!')),
                    ('2', ('AT', '@')),
                    ('3', ('HASH', 'POUND', '#')),
                    ('4', ('DOLLAR', 'DLR', '$')),
                    ('5', ('PERCENT', 'PERC', '%')),
                    ('6', ('CIRCUMFLEX', 'CIRC', '^')),
                    ('7', ('AMPERSAND', 'AMPR', '&')),
                    ('8', ('ASTERISK', 'ASTR', '*')),
                    ('9', ('LEFT_PAREN', 'LPRN', '(')),
                    ('0', ('RIGHT_PAREN', 'RPRN', ')')),
                    ('MINUS', ('UNDERSCORE', 'UNDS', '_')),
                    ('EQUAL', ('PLUS', '+')),
                    ('LBRACKET', ('LEFT_CURLY_BRACE', 'LCBR', '{')),
                    ('RBRACKET', ('RIGHT_CURLY_BRACE', 'RCBR', '}')),
                    ('BACKSLASH', ('PIPE', '|')),
                    ('SEMICOLON', ('COLON', 'COLN', ':')),
                    ('QUOTE', ('DOUBLE_QUOTE', 'DQUO', 'DQT', '"')),
                    ('COMMA', ('LEFT_ANGLE_BRACKET', 'LABK', '<')),
                    ('DOT', ('RIGHT_ANGLE_BRACKET', 'RABK', '>')),
                    ('SLSH', ('QUESTION', 'QUES', '?')),
                ),
                # International
                lambda key: left_pipe_until_some(
                    key,
                    maybe_make_key,
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
                ),
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
                lambda key: left_pipe_until_some(
                    key,
                    maybe_make_consumer_key,
                    (226, ('AUDIO_MUTE', 'MUTE')),  # 0xE2
                    (233, ('AUDIO_VOL_UP', 'VOLU')),  # 0xE9
                    (234, ('AUDIO_VOL_DOWN', 'VOLD')),  # 0xEA
                    (181, ('MEDIA_NEXT_TRACK', 'MNXT')),  # 0xB5
                    (182, ('MEDIA_PREV_TRACK', 'MPRV')),  # 0xB6
                    (183, ('MEDIA_STOP', 'MSTP')),  # 0xB7
                    (205, ('MEDIA_PLAY_PAUSE', 'MPLY')),  # 0xCD (this may not be right)
                    (184, ('MEDIA_EJECT', 'EJCT')),  # 0xB8
                    (179, ('MEDIA_FAST_FORWARD', 'MFFD')),  # 0xB3
                    (180, ('MEDIA_REWIND', 'MRWD')),  # 0xB4
                ),
            )

            if DEBUG_OUTPUT:
                print(f'{key}: {maybe_key}')

            if not maybe_key:
                raise ValueError('Invalid key')

        return self.__getattr__(key, depth=depth + 1)


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


def make_mod_key(code, names, *args, **kwargs):
    return make_key(code, names, *args, **kwargs, type=KEY_MODIFIER)


def make_shifted_key(target_name, names=tuple()):  # NOQA
    # For... probably a few years, a bug existed here where keys were looked
    # up by `KC[...]`, but that's incorrect: an AttrDit exposes a dictionary
    # with attributes, but key-based dictionary access with brackets does
    # *not* implicitly call __getattr__. We got away with this when key defs
    # were not lazily created, but now that they are, shifted keys would
    # sometimes break, complaining that they couldn't find their underlying
    # key to shift. Fixed!
    key = KC.LSFT(getattr(KC, target_name))

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
