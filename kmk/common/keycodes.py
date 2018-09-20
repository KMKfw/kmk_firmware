try:
    from collections import namedtuple
except ImportError:
    # This is handled by micropython-lib/collections, but on local runs of
    # MicroPython, it doesn't exist
    from ucollections import namedtuple

from kmk.common.types import AttrDict
from kmk.common.util import flatten_dict

Keycode = namedtuple('Keycode', ('code', 'is_modifier'))


class KeycodeCategory(type):
    @classmethod
    def to_dict(cls):
        '''
        MicroPython, for whatever reason (probably performance/memory) makes
        __dict__ optional for ports. Unfortunately, at least the STM32
        (Pyboard) port is one such port. This reimplements a subset of
        __dict__, limited to just keys we're likely to care about (though this
        could be opened up further later).
        '''

        hidden = ('to_dict', 'recursive_dict', 'contains')
        return AttrDict({
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith('_') and key not in hidden
        })

    @classmethod
    def recursive_dict(cls):
        '''
        to_dict() executed recursively all the way down a tree
        '''
        ret = cls.to_dict()

        for key, val in ret.items():
            try:
                nested_ret = val.recursive_dict()
            except (AttributeError, NameError):
                continue

            ret[key] = nested_ret

        return ret

    @classmethod
    def contains(cls, kc):
        '''
        Emulates the 'in' operator for keycode groupings, given MicroPython's
        lack of support for metaclasses (meaning implementing 'in' for
        uninstantiated classes, such as these, is largely not possible). Not
        super useful in most cases, but does allow for sanity checks like

        ```python
        assert Keycodes.Modifiers.contains(requested_key)
        ```

        This is not bulletproof due to how HID codes are defined (there is
        overlap). Keycodes.Common.KC_A, for example, is equal in value to
        Keycodes.Modifiers.KC_LALT, but it can still prevent silly mistakes
        like trying to use, say, Keycodes.Common.KC_Q as a modifier.

        This is recursive across subgroups, enabling stuff like:

        ```python
        assert Keycodes.contains(requested_key)
        ```

        To ensure that a valid keycode has been requested to begin with. Again,
        not bulletproof, but adds at least some cushion to stuff that would
        otherwise cause AttributeErrors and crash the keyboard.
        '''
        subcategories = (
            category for category in cls.to_dict().values()
            # Disgusting, but since `cls.__bases__` isn't implemented in MicroPython,
            # I resort to a less foolproof inheritance check that should still ignore
            # strings and other stupid stuff (we don't want to iterate over __doc__,
            # for example), but include nested classes.
            #
            # One huge lesson in this project is that uninstantiated classes are hard...
            # and four times harder when the implementation of Python is half-baked.
            if isinstance(category, type)
        )

        if any(
            kc == _kc
            for name, _kc in cls.to_dict().items()
            if name.startswith('KC_')
        ):
            return True

        return any(sc.contains(kc) for sc in subcategories)


class Keycodes(KeycodeCategory):
    '''
    A massive grouping of keycodes
    '''
    class Modifiers(KeycodeCategory):
        KC_LCTRL = KC_LCTL = Keycode(0x01, True)
        KC_LSHIFT = KC_LSFT = Keycode(0x02, True)
        KC_LALT = Keycode(0x04, True)
        KC_LGUI = KC_LCMD = KL_LWIN = Keycode(0x08, True)
        KC_RCTRL = KC_RCTL = Keycode(0x10, True)
        KC_RSHIFT = KC_RSFT = Keycode(0x20, True)
        KC_RALT = Keycode(0x40, True)
        KC_RGUI = KC_RCMD = KC_RWIN = Keycode(0x80, True)

    class Common(KeycodeCategory):
        KC_A = Keycode(4, False)
        KC_B = Keycode(5, False)
        KC_C = Keycode(6, False)
        KC_D = Keycode(7, False)
        KC_E = Keycode(8, False)
        KC_F = Keycode(9, False)
        KC_G = Keycode(10, False)
        KC_H = Keycode(11, False)
        KC_I = Keycode(12, False)
        KC_J = Keycode(13, False)
        KC_K = Keycode(14, False)
        KC_L = Keycode(15, False)
        KC_M = Keycode(16, False)
        KC_N = Keycode(17, False)
        KC_O = Keycode(18, False)
        KC_P = Keycode(19, False)
        KC_Q = Keycode(20, False)
        KC_R = Keycode(21, False)
        KC_S = Keycode(22, False)
        KC_T = Keycode(23, False)
        KC_U = Keycode(24, False)
        KC_V = Keycode(25, False)
        KC_W = Keycode(26, False)
        KC_X = Keycode(27, False)
        KC_Y = Keycode(28, False)
        KC_Z = Keycode(29, False)

        # Aliases to play nicely with AttrDict, since KC.1 isn't a valid
        # attribute key in Python, but KC.N1 is
        KC_1 = KC_N1 = Keycode(30, False)
        KC_2 = KC_N2 = Keycode(31, False)
        KC_3 = KC_N3 = Keycode(32, False)
        KC_4 = KC_N4 = Keycode(33, False)
        KC_5 = KC_N5 = Keycode(34, False)
        KC_6 = KC_N6 = Keycode(35, False)
        KC_7 = KC_N7 = Keycode(36, False)
        KC_8 = KC_N8 = Keycode(37, False)
        KC_9 = KC_N9 = Keycode(38, False)
        KC_0 = KC_N0 = Keycode(39, False)

        KC_ENTER = KC_ENT = Keycode(40, False)
        KC_ESCAPE = KC_ESC = Keycode(41, False)
        KC_BACKSPACE = KC_BKSP = Keycode(42, False)
        KC_TAB = Keycode(43, False)
        KC_SPACE = KC_SPC = Keycode(44, False)
        KC_MINUS = KC_MINS = Keycode(45, False)
        KC_EQUAL = KC_EQL = Keycode(46, False)
        KC_LBRACKET = KC_LBRC = Keycode(47, False)
        KC_RBRACKET = KC_RBRC = Keycode(48, False)
        KC_BACKSLASH = KC_BSLASH = KC_BSLS = Keycode(49, False)
        KC_NONUS_HASH = KC_NUHS = Keycode(50, False)
        KC_NONUS_BSLASH = KC_NUBS = Keycode(100, False)
        KC_SEMICOLON = KC_SCOLON = KC_SCLN = Keycode(51, False)
        KC_QUOTE = KC_QUOT = Keycode(52, False)
        KC_GRAVE = KC_GRV = KC_ZKHK = Keycode(53, False)
        KC_COMMA = KC_COMM = Keycode(54, False)
        KC_DOT = Keycode(55, False)
        KC_SLASH = KC_SLSH = Keycode(56, False)

    class FunctionKeys(KeycodeCategory):
        KC_F1 = Keycode(58, False)
        KC_F2 = Keycode(59, False)
        KC_F3 = Keycode(60, False)
        KC_F4 = Keycode(61, False)
        KC_F5 = Keycode(62, False)
        KC_F6 = Keycode(63, False)
        KC_F7 = Keycode(64, False)
        KC_F8 = Keycode(65, False)
        KC_F9 = Keycode(66, False)
        KC_F10 = Keycode(67, False)
        KC_F11 = Keycode(68, False)
        KC_F12 = Keycode(69, False)
        KC_F13 = Keycode(104, False)
        KC_F14 = Keycode(105, False)
        KC_F15 = Keycode(106, False)
        KC_F16 = Keycode(107, False)
        KC_F17 = Keycode(108, False)
        KC_F18 = Keycode(109, False)
        KC_F19 = Keycode(110, False)
        KC_F20 = Keycode(111, False)
        KC_F21 = Keycode(112, False)
        KC_F22 = Keycode(113, False)
        KC_F23 = Keycode(114, False)
        KC_F24 = Keycode(115, False)

    class NavAndLocks(KeycodeCategory):
        KC_CAPS_LOCK = KC_CLCK = KC_CAPS = Keycode(57, False)
        KC_LOCKING_CAPS = KC_LCAP = Keycode(130, False)
        KC_PSCREEN = KC_PSCR = Keycode(70, False)
        KC_SCROLLLOCK = KC_SLCK = Keycode(71, False)
        KC_LOCKING_SCROLL = KC_LSCRL = Keycode(132, False)
        KC_PAUSE = KC_PAUS = KC_BRK = Keycode(72, False)
        KC_INSERT = KC_INS = Keycode(73, False)
        KC_HOME = Keycode(74, False)
        KC_PGUP = Keycode(75, False)
        KC_DELETE = KC_DEL = Keycode(76, False)
        KC_END = Keycode(77, False)
        KC_PGDOWN = KC_PGDN = Keycode(78, False)
        KC_RIGHT = KC_RGHT = Keycode(79, False)
        KC_LEFT = Keycode(80, False)
        KC_DOWN = Keycode(81, False)
        KC_UP = Keycode(82, False)

    class Numpad(KeycodeCategory):
        KC_NUMLOCK = KC_NLCK = Keycode(83, False)
        KC_LOCKING_NUM = KC_LNUM = Keycode(131, False)
        KC_KP_SLASH = KC_PSLS = Keycode(84, False)
        KC_KP_ASTERIK = KC_PAST = Keycode(85, False)
        KC_KP_MINUS = KC_PMNS = Keycode(86, False)
        KC_KP_PLUS = KC_PPLS = Keycode(87, False)
        KC_KP_ENTER = KC_PENT = Keycode(88, False)
        KC_KP_1 = KC_P1 = Keycode(89, False)
        KC_KP_2 = KC_P2 = Keycode(90, False)
        KC_KP_3 = KC_P3 = Keycode(91, False)
        KC_KP_4 = KC_P4 = Keycode(92, False)
        KC_KP_5 = KC_P5 = Keycode(93, False)
        KC_KP_6 = KC_P6 = Keycode(94, False)
        KC_KP_7 = KC_P7 = Keycode(95, False)
        KC_KP_8 = KC_P8 = Keycode(96, False)
        KC_KP_9 = KC_P9 = Keycode(97, False)
        KC_KP_0 = KC_P0 = Keycode(98, False)
        KC_KP_DOT = KC_PDOT = Keycode(99, False)
        KC_KP_EQUAL = KC_PEQL = Keycode(103, False)
        KC_KP_COMMA = KC_PCMM = Keycode(133, False)
        KC_KP_EQUAL_AS400 = Keycode(134, False)

    class International(KeycodeCategory):
        KC_INT1 = KC_RO = Keycode(135, False)
        KC_INT2 = KC_KANA = Keycode(136, False)
        KC_INT3 = KC_JYEN = Keycode(137, False)
        KC_INT4 = KC_HENK = Keycode(138, False)
        KC_INT5 = KC_MHEN = Keycode(139, False)
        KC_INT6 = Keycode(140, False)
        KC_INT7 = Keycode(141, False)
        KC_INT8 = Keycode(142, False)
        KC_INT9 = Keycode(143, False)
        KC_LANG1 = KC_HAEN = Keycode(144, False)
        KC_LANG2 = KC_HAEJ = Keycode(145, False)
        KC_LANG3 = Keycode(146, False)
        KC_LANG4 = Keycode(147, False)
        KC_LANG5 = Keycode(148, False)
        KC_LANG6 = Keycode(149, False)
        KC_LANG7 = Keycode(150, False)
        KC_LANG8 = Keycode(151, False)
        KC_LANG9 = Keycode(152, False)

    class Misc(KeycodeCategory):
        KC_APPLICATION = KC_APP = Keycode(101, False)
        KC_POWER = Keycode(102, False)
        KC_EXECUTE = KC_EXEC = Keycode(116, False)
        KC_SYSTEM_POWER = KC_PWR = Keycode(165, False)
        KC_SYSTEM_SLEEP = KC_SLEP = Keycode(166, False)
        KC_SYSTEM_WAKE = KC_WAKE = Keycode(167, False)
        KC_HELP = Keycode(117, False)
        KC_MENU = Keycode(118, False)
        KC_SELECT = KC_SLCT = Keycode(119, False)
        KC_STOP = Keycode(120, False)
        KC_AGAIN = KC_AGIN = Keycode(121, False)
        KC_UNDO = Keycode(122, False)
        KC_CUT = Keycode(123, False)
        KC_COPY = Keycode(124, False)
        KC_PASTE = KC_PSTE = Keycode(125, False)
        KC_FIND = Keycode(126, False)
        KC_ALT_ERASE = KC_ERAS = Keycode(153, False)
        KC_SYSREQ = Keycode(154, False)
        KC_CANCEL = Keycode(155, False)
        KC_CLEAR = KC_CLR = Keycode(156, False)
        KC_PRIOR = Keycode(157, False)
        KC_RETURN = Keycode(158, False)
        KC_SEPERATOR = Keycode(159, False)
        KC_OUT = Keycode(160, False)
        KC_OPER = Keycode(161, False)
        KC_CLEAR_AGAIN = Keycode(162, False)
        KC_CRSEL = Keycode(163, False)
        KC_EXSEL = Keycode(164, False)
        KC_MAIL = Keycode(177, False)
        KC_CALCULATOR = KC_CALC = Keycode(178, False)
        KC_MY_COMPUTER = KC_MYCM = Keycode(179, False)
        KC_WWW_SEARCH = KC_WSCH = Keycode(180, False)
        KC_WWW_HOME = KC_WHOM = Keycode(181, False)
        KC_WWW_BACK = KC_WBAK = Keycode(182, False)
        KC_WWW_FORWARD = KC_WFWD = Keycode(183, False)
        KC_WWW_STOP = KC_WSTP = Keycode(184, False)
        KC_WWW_REFRESH = KC_WREF = Keycode(185, False)
        KC_WWW_FAVORITES = KC_WFAV = Keycode(186, False)

    class Media(KeycodeCategory):
        KC__MUTE = Keycode(127, False)
        KC__VOLUP = Keycode(128, False)
        KC__VOLDOWN = Keycode(129, False)
        KC_AUDIO_MUTE = KC_MUTE = Keycode(168, False)
        KC_AUDIO_VOL_UP = KC_VOLU = Keycode(169, False)
        KC_AUDIO_VOL_DOWN = KC_VOLD = Keycode(170, False)
        KC_MEDIA_NEXT_TRACK = KC_MNXT = Keycode(171, False)
        KC_MEDIA_PREV_TRACK = KC_MPRV = Keycode(172, False)
        KC_MEDIA_STOP = KC_MSTP = Keycode(173, False)
        KC_MEDIA_PLAY_PAUSE = KC_MPLY = Keycode(174, False)
        KC_MEDIA_SELECT = KC_MSEL = Keycode(175, False)
        KC_MEDIA_EJECT = KC_EJCT = Keycode(176, False)
        KC_MEDIA_FAST_FORWARD = KC_MFFD = Keycode(187, False)
        KC_MEDIA_REWIND = KC_MRWD = Keycode(189, False)


ALL_KEYS = KC = AttrDict({
    k.replace('KC_', ''): v
    for k, v in flatten_dict(Keycodes.recursive_dict()).items()
})

char_lookup = {
    "\n": (Keycodes.Common.KC_ENTER,),
    "\t": (Keycodes.Common.KC_TAB,),
    ' ': (Keycodes.Common.KC_SPACE,),
    '-': (Keycodes.Common.KC_MINUS,),
    '=': (Keycodes.Common.KC_EQUAL,),
    '+': (Keycodes.Common.KC_EQUAL, Keycodes.Modifiers.KC_SHIFT),
    '~': (Keycodes.Common.KC_TILDE,),
}
