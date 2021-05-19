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
KEY_SHIFTED = const(3)
KEY_ARGUMENTED = const(4)


class KeyAttrDict(AttrDict):
    def __getattr__(self, key):
        try:
            return super(KeyAttrDict, self).__getattr__(key)
        except:
            pass
        for names, args in key_map.items():
            maker = key_makers[args[1]]
            if len(args) > 2:
                kwargs = args[2]
            else:
                kwargs = {}

            if key in names:
                if isinstance(args[0], int):
                    maker(code=args[0], names=names, **kwargs)
                elif isinstance(args[0], str):
                    maker(args[0], names=names, **kwargs)
                else:
                    maker(names=names, **kwargs)
                return self.__getattr__(key)
        else:
            raise ValueError("Invalid key")


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


key_makers = {
    KEY_SIMPLE: make_key,
    KEY_MODIFIER: make_mod_key,
    KEY_CONSUMER: make_consumer_key,
    KEY_SHIFTED: make_shifted_key,
    KEY_ARGUMENTED: make_argumented_key,
}

key_map = {
    ('LEFT_CONTROL', 'LCTRL', 'LCTL'): (1, KEY_MODIFIER),
    ('LEFT_SHIFT', 'LSHIFT', 'LSFT'): (2, KEY_MODIFIER),
    ('LEFT_ALT', 'LALT'): (4, KEY_MODIFIER),
    ('LEFT_SUPER', 'LGUI', 'LCMD', 'LWIN'): (8, KEY_MODIFIER),
    ('RIGHT_CONTROL', 'RCTRL', 'RCTL'): (16, KEY_MODIFIER),
    ('RIGHT_SHIFT', 'RSHIFT', 'RSFT'): (32, KEY_MODIFIER),
    ('RIGHT_ALT', 'RALT'): (64, KEY_MODIFIER),
    ('RIGHT_SUPER', 'RGUI', 'RCMD', 'RWIN'): (128, KEY_MODIFIER),
    ('MEH',): (7, KEY_MODIFIER),
    ('HYPER', 'HYPR'): (15, KEY_MODIFIER),
    ('A',): (4, KEY_SIMPLE),
    ('B',): (5, KEY_SIMPLE),
    ('C',): (6, KEY_SIMPLE),
    ('D',): (7, KEY_SIMPLE),
    ('E',): (8, KEY_SIMPLE),
    ('F',): (9, KEY_SIMPLE),
    ('G',): (10, KEY_SIMPLE),
    ('H',): (11, KEY_SIMPLE),
    ('I',): (12, KEY_SIMPLE),
    ('J',): (13, KEY_SIMPLE),
    ('K',): (14, KEY_SIMPLE),
    ('L',): (15, KEY_SIMPLE),
    ('M',): (16, KEY_SIMPLE),
    ('N',): (17, KEY_SIMPLE),
    ('O',): (18, KEY_SIMPLE),
    ('P',): (19, KEY_SIMPLE),
    ('Q',): (20, KEY_SIMPLE),
    ('R',): (21, KEY_SIMPLE),
    ('S',): (22, KEY_SIMPLE),
    ('T',): (23, KEY_SIMPLE),
    ('U',): (24, KEY_SIMPLE),
    ('V',): (25, KEY_SIMPLE),
    ('W',): (26, KEY_SIMPLE),
    ('X',): (27, KEY_SIMPLE),
    ('Y',): (28, KEY_SIMPLE),
    ('Z',): (29, KEY_SIMPLE),
    ('1', 'N1'): (30, KEY_SIMPLE),
    ('2', 'N2'): (31, KEY_SIMPLE),
    ('3', 'N3'): (32, KEY_SIMPLE),
    ('4', 'N4'): (33, KEY_SIMPLE),
    ('5', 'N5'): (34, KEY_SIMPLE),
    ('6', 'N6'): (35, KEY_SIMPLE),
    ('7', 'N7'): (36, KEY_SIMPLE),
    ('8', 'N8'): (37, KEY_SIMPLE),
    ('9', 'N9'): (38, KEY_SIMPLE),
    ('0', 'N0'): (39, KEY_SIMPLE),
    ('ENTER', 'ENT', '\n'): (40, KEY_SIMPLE),
    ('ESCAPE', 'ESC'): (41, KEY_SIMPLE),
    ('BACKSPACE', 'BSPC', 'BKSP'): (42, KEY_SIMPLE),
    ('TAB', '\t'): (43, KEY_SIMPLE),
    ('SPACE', 'SPC', ' '): (44, KEY_SIMPLE),
    ('MINUS', 'MINS', '-'): (45, KEY_SIMPLE),
    ('EQUAL', 'EQL', '='): (46, KEY_SIMPLE),
    ('LBRACKET', 'LBRC', '['): (47, KEY_SIMPLE),
    ('RBRACKET', 'RBRC', ']'): (48, KEY_SIMPLE),
    ('BACKSLASH', 'BSLASH', 'BSLS', '\\'): (49, KEY_SIMPLE),
    ('SEMICOLON', 'SCOLON', 'SCLN', ';'): (51, KEY_SIMPLE),
    ('QUOTE', 'QUOT', "'"): (52, KEY_SIMPLE),
    ('GRAVE', 'GRV', 'ZKHK', '`'): (53, KEY_SIMPLE),
    ('COMMA', 'COMM', ','): (54, KEY_SIMPLE),
    ('DOT', '.'): (55, KEY_SIMPLE),
    ('SLASH', 'SLSH'): (56, KEY_SIMPLE),
    ('F1',): (58, KEY_SIMPLE),
    ('F2',): (59, KEY_SIMPLE),
    ('F3',): (60, KEY_SIMPLE),
    ('F4',): (61, KEY_SIMPLE),
    ('F5',): (62, KEY_SIMPLE),
    ('F6',): (63, KEY_SIMPLE),
    ('F7',): (64, KEY_SIMPLE),
    ('F8',): (65, KEY_SIMPLE),
    ('F9',): (66, KEY_SIMPLE),
    ('F10',): (67, KEY_SIMPLE),
    ('F11',): (68, KEY_SIMPLE),
    ('F12',): (69, KEY_SIMPLE),
    ('F13',): (104, KEY_SIMPLE),
    ('F14',): (105, KEY_SIMPLE),
    ('F15',): (106, KEY_SIMPLE),
    ('F16',): (107, KEY_SIMPLE),
    ('F17',): (108, KEY_SIMPLE),
    ('F18',): (109, KEY_SIMPLE),
    ('F19',): (110, KEY_SIMPLE),
    ('F20',): (111, KEY_SIMPLE),
    ('F21',): (112, KEY_SIMPLE),
    ('F22',): (113, KEY_SIMPLE),
    ('F23',): (114, KEY_SIMPLE),
    ('F24',): (115, KEY_SIMPLE),
    ('CAPS_LOCK', 'CAPSLOCK', 'CLCK', 'CAPS'): (57, KEY_SIMPLE),
    ('PRINT_SCREEN', 'PSCREEN', 'PSCR'): (70, KEY_SIMPLE),
    ('SCROLL_LOCK', 'SCROLLLOCK', 'SLCK'): (71, KEY_SIMPLE),
    ('PAUSE', 'PAUS', 'BRK'): (72, KEY_SIMPLE),
    ('INSERT', 'INS'): (73, KEY_SIMPLE),
    ('HOME',): (74, KEY_SIMPLE),
    ('PGUP',): (75, KEY_SIMPLE),
    ('DELETE', 'DEL'): (76, KEY_SIMPLE),
    ('END',): (77, KEY_SIMPLE),
    ('PGDOWN', 'PGDN'): (78, KEY_SIMPLE),
    ('RIGHT', 'RGHT'): (79, KEY_SIMPLE),
    ('LEFT',): (80, KEY_SIMPLE),
    ('DOWN',): (81, KEY_SIMPLE),
    ('UP',): (82, KEY_SIMPLE),
    ('NUM_LOCK', 'NUMLOCK', 'NLCK'): (83, KEY_SIMPLE),
    ('KP_SLASH', 'NUMPAD_SLASH', 'PSLS'): (84, KEY_SIMPLE),
    ('KP_ASTERISK', 'NUMPAD_ASTERISK', 'PAST'): (85, KEY_SIMPLE),
    ('KP_MINUS', 'NUMPAD_MINUS', 'PMNS'): (86, KEY_SIMPLE),
    ('KP_PLUS', 'NUMPAD_PLUS', 'PPLS'): (87, KEY_SIMPLE),
    ('KP_ENTER', 'NUMPAD_ENTER', 'PENT'): (88, KEY_SIMPLE),
    ('KP_1', 'P1', 'NUMPAD_1'): (89, KEY_SIMPLE),
    ('KP_2', 'P2', 'NUMPAD_2'): (90, KEY_SIMPLE),
    ('KP_3', 'P3', 'NUMPAD_3'): (91, KEY_SIMPLE),
    ('KP_4', 'P4', 'NUMPAD_4'): (92, KEY_SIMPLE),
    ('KP_5', 'P5', 'NUMPAD_5'): (93, KEY_SIMPLE),
    ('KP_6', 'P6', 'NUMPAD_6'): (94, KEY_SIMPLE),
    ('KP_7', 'P7', 'NUMPAD_7'): (95, KEY_SIMPLE),
    ('KP_8', 'P8', 'NUMPAD_8'): (96, KEY_SIMPLE),
    ('KP_9', 'P9', 'NUMPAD_9'): (97, KEY_SIMPLE),
    ('KP_0', 'P0', 'NUMPAD_0'): (98, KEY_SIMPLE),
    ('KP_DOT', 'PDOT', 'NUMPAD_DOT'): (99, KEY_SIMPLE),
    ('KP_EQUAL', 'PEQL', 'NUMPAD_EQUAL'): (103, KEY_SIMPLE),
    ('KP_COMMA', 'PCMM', 'NUMPAD_COMMA'): (133, KEY_SIMPLE),
    ('KP_EQUAL_AS400', 'NUMPAD_EQUAL_AS400'): (134, KEY_SIMPLE),
    ('TILDE', 'TILD', '~'): ('GRAVE', KEY_SHIFTED),
    ('EXCLAIM', 'EXLM', '!'): ('1', KEY_SHIFTED),
    ('AT', '@'): ('2', KEY_SHIFTED),
    ('HASH', 'POUND', '#'): ('3', KEY_SHIFTED),
    ('DOLLAR', 'DLR', '$'): ('4', KEY_SHIFTED),
    ('PERCENT', 'PERC', '%'): ('5', KEY_SHIFTED),
    ('CIRCUMFLEX', 'CIRC', '^'): ('6', KEY_SHIFTED),
    ('AMPERSAND', 'AMPR', '&'): ('7', KEY_SHIFTED),
    ('ASTERISK', 'ASTR', '*'): ('8', KEY_SHIFTED),
    ('LEFT_PAREN', 'LPRN', '('): ('9', KEY_SHIFTED),
    ('RIGHT_PAREN', 'RPRN', ')'): ('0', KEY_SHIFTED),
    ('UNDERSCORE', 'UNDS', '_'): ('MINUS', KEY_SHIFTED),
    ('PLUS', '+'): ('EQUAL', KEY_SHIFTED),
    ('LEFT_CURLY_BRACE', 'LCBR', '{'): ('LBRACKET', KEY_SHIFTED),
    ('RIGHT_CURLY_BRACE', 'RCBR', '}'): ('RBRACKET', KEY_SHIFTED),
    ('PIPE', '|'): ('BACKSLASH', KEY_SHIFTED),
    ('COLON', 'COLN', ':'): ('SEMICOLON', KEY_SHIFTED),
    ('DOUBLE_QUOTE', 'DQUO', 'DQT', '"'): ('QUOTE', KEY_SHIFTED),
    ('LEFT_ANGLE_BRACKET', 'LABK', '<'): ('COMMA', KEY_SHIFTED),
    ('RIGHT_ANGLE_BRACKET', 'RABK', '>'): ('DOT', KEY_SHIFTED),
    ('QUESTION', 'QUES', '?'): ('SLSH', KEY_SHIFTED),
    ('NONUS_HASH', 'NUHS'): (50, KEY_SIMPLE),
    ('NONUS_BSLASH', 'NUBS'): (100, KEY_SIMPLE),
    ('APP', 'APPLICATION', 'SEL', 'WINMENU'): (101, KEY_SIMPLE),
    ('INT1', 'RO'): (135, KEY_SIMPLE),
    ('INT2', 'KANA'): (136, KEY_SIMPLE),
    ('INT3', 'JYEN'): (137, KEY_SIMPLE),
    ('INT4', 'HENK'): (138, KEY_SIMPLE),
    ('INT5', 'MHEN'): (139, KEY_SIMPLE),
    ('INT6',): (140, KEY_SIMPLE),
    ('INT7',): (141, KEY_SIMPLE),
    ('INT8',): (142, KEY_SIMPLE),
    ('INT9',): (143, KEY_SIMPLE),
    ('LANG1', 'HAEN'): (144, KEY_SIMPLE),
    ('LANG2', 'HAEJ'): (145, KEY_SIMPLE),
    ('LANG3',): (146, KEY_SIMPLE),
    ('LANG4',): (147, KEY_SIMPLE),
    ('LANG5',): (148, KEY_SIMPLE),
    ('LANG6',): (149, KEY_SIMPLE),
    ('LANG7',): (150, KEY_SIMPLE),
    ('LANG8',): (151, KEY_SIMPLE),
    ('LANG9',): (152, KEY_SIMPLE),
    ('AUDIO_MUTE', 'MUTE'): (226, KEY_CONSUMER),
    ('AUDIO_VOL_UP', 'VOLU'): (233, KEY_CONSUMER),
    ('AUDIO_VOL_DOWN', 'VOLD'): (234, KEY_CONSUMER),
    ('MEDIA_NEXT_TRACK', 'MNXT'): (181, KEY_CONSUMER),
    ('MEDIA_PREV_TRACK', 'MPRV'): (182, KEY_CONSUMER),
    ('MEDIA_STOP', 'MSTP'): (183, KEY_CONSUMER),
    ('MEDIA_PLAY_PAUSE', 'MPLY'): (205, KEY_CONSUMER),
    ('MEDIA_EJECT', 'EJCT'): (184, KEY_CONSUMER),
    ('MEDIA_FAST_FORWARD', 'MFFD'): (179, KEY_CONSUMER),
    ('MEDIA_REWIND', 'MRWD'): (180, KEY_CONSUMER),
    ('NO',): (
        None,
        KEY_SIMPLE,
        {'on_press': handlers.passthrough, 'on_release': handlers.passthrough},
    ),
    ('TRANSPARENT', 'TRNS'): (
        None,
        KEY_SIMPLE,
        {'on_press': handlers.passthrough, 'on_release': handlers.passthrough},
    ),
    ('RESET',): (None, KEY_SIMPLE, {'on_press': handlers.reset}),
    ('BOOTLOADER',): (None, KEY_SIMPLE, {'on_press': handlers.bootloader}),
    ('DEBUG', 'DBG'): (
        None,
        KEY_SIMPLE,
        {'on_press': handlers.debug_pressed, 'on_release': handlers.passthrough},
    ),
    ('GESC',): (
        None,
        KEY_SIMPLE,
        {'on_press': handlers.gesc_pressed, 'on_release': handlers.gesc_released},
    ),
    ('BKDL',): (
        None,
        KEY_SIMPLE,
        {'on_press': handlers.bkdl_pressed, 'on_release': handlers.bkdl_released},
    ),
    ('GESC', 'GRAVE_ESC'): (
        None,
        KEY_SIMPLE,
        {'on_press': handlers.gesc_pressed, 'on_release': handlers.gesc_released},
    ),
    ('MACRO_SLEEP_MS', 'SLEEP_IN_SEQ'): (
        None,
        KEY_ARGUMENTED,
        {'validator': key_seq_sleep_validator, 'on_press': handlers.sleep_pressed},
    ),
    ('UC_MODE_NOOP', 'UC_DISABLE'): (
        None,
        KEY_SIMPLE,
        {
            'meta': UnicodeModeKeyMeta(UnicodeMode.NOOP),
            'on_press': handlers.uc_mode_pressed,
        },
    ),
    ('UC_MODE_LINUX', 'UC_MODE_IBUS'): (
        None,
        KEY_SIMPLE,
        {
            'meta': UnicodeModeKeyMeta(UnicodeMode.IBUS),
            'on_press': handlers.uc_mode_pressed,
        },
    ),
    ('UC_MODE_MACOS', 'UC_MODE_OSX', 'US_MODE_RALT'): (
        None,
        KEY_SIMPLE,
        {
            'meta': UnicodeModeKeyMeta(UnicodeMode.RALT),
            'on_press': handlers.uc_mode_pressed,
        },
    ),
    ('UC_MODE_WINC',): (
        None,
        KEY_SIMPLE,
        {
            'meta': UnicodeModeKeyMeta(UnicodeMode.WINC),
            'on_press': handlers.uc_mode_pressed,
        },
    ),
    ('UC_MODE',): (
        None,
        KEY_ARGUMENTED,
        {'validator': unicode_mode_key_validator, 'on_press': handlers.uc_mode_pressed},
    ),
    ('TAP_DANCE', 'TD'): (
        None,
        KEY_ARGUMENTED,
        {
            'validator': tap_dance_key_validator,
            'on_press': handlers.td_pressed,
            'on_release': handlers.td_released,
        },
    ),
    ('HID_SWITCH', 'HID'): (None, KEY_SIMPLE, {'on_press': handlers.hid_switch}),
}
