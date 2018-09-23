try:
    from collections import namedtuple
except ImportError:
    # This is handled by micropython-lib/collections, but on local runs of
    # MicroPython, it doesn't exist
    from ucollections import namedtuple

from kmk.common.types import AttrDict
from kmk.common.util import flatten_dict

FIRST_KMK_INTERNAL_KEYCODE = 1000

LayerKeycode = namedtuple('LayerKeycode', ('code', 'layer'))


class Keycode:
    def __init__(self, code, has_modifiers=None):
        self.code = code
        self.has_modifiers = has_modifiers


class ModifierKeycode:
    def __init__(self, code):
        self.code = code


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


CODE_LCTRL = CODE_LCTL = 0x01
CODE_LSHIFT = CODE_LSFT = 0x02
CODE_LALT = 0x04
CODE_LGUI = CODE_LCMD = CODE_LWIN = 0x08
CODE_RCTRL = CODE_RCTL = 0x10
CODE_RSHIFT = CODE_RSFT = 0x20
CODE_RALT = 0x40
CODE_RGUI = CODE_RCMD = CODE_RWIN = 0x80


class Keycodes(KeycodeCategory):
    '''
    A massive grouping of keycodes
    '''
    class Modifiers(KeycodeCategory):
        KC_LCTRL = KC_LCTL = ModifierKeycode(CODE_LCTRL)
        KC_LSHIFT = KC_LSFT = ModifierKeycode(CODE_LSHIFT)
        KC_LALT = ModifierKeycode(CODE_LALT)
        KC_LGUI = KC_LCMD = KC_LWIN = ModifierKeycode(CODE_LGUI)
        KC_RCTRL = KC_RCTL = ModifierKeycode(CODE_RCTRL)
        KC_RSHIFT = KC_RSFT = ModifierKeycode(CODE_RSHIFT)
        KC_RALT = ModifierKeycode(CODE_RALT)
        KC_RGUI = KC_RCMD = KC_RWIN = ModifierKeycode(CODE_RGUI)

    class Common(KeycodeCategory):
        KC_A = Keycode(4)
        KC_B = Keycode(5)
        KC_C = Keycode(6)
        KC_D = Keycode(7)
        KC_E = Keycode(8)
        KC_F = Keycode(9)
        KC_G = Keycode(10)
        KC_H = Keycode(11)
        KC_I = Keycode(12)
        KC_J = Keycode(13)
        KC_K = Keycode(14)
        KC_L = Keycode(15)
        KC_M = Keycode(16)
        KC_N = Keycode(17)
        KC_O = Keycode(18)
        KC_P = Keycode(19)
        KC_Q = Keycode(20)
        KC_R = Keycode(21)
        KC_S = Keycode(22)
        KC_T = Keycode(23)
        KC_U = Keycode(24)
        KC_V = Keycode(25)
        KC_W = Keycode(26)
        KC_X = Keycode(27)
        KC_Y = Keycode(28)
        KC_Z = Keycode(29)

        # Aliases to play nicely with AttrDict, since KC.1 isn't a valid
        # attribute key in Python, but KC.N1 is
        KC_1 = KC_N1 = Keycode(30)
        KC_2 = KC_N2 = Keycode(31)
        KC_3 = KC_N3 = Keycode(32)
        KC_4 = KC_N4 = Keycode(33)
        KC_5 = KC_N5 = Keycode(34)
        KC_6 = KC_N6 = Keycode(35)
        KC_7 = KC_N7 = Keycode(36)
        KC_8 = KC_N8 = Keycode(37)
        KC_9 = KC_N9 = Keycode(38)
        KC_0 = KC_N0 = Keycode(39)

        KC_ENTER = KC_ENT = Keycode(40)
        KC_ESCAPE = KC_ESC = Keycode(41)
        KC_BACKSPACE = KC_BKSP = Keycode(42)
        KC_TAB = Keycode(43)
        KC_SPACE = KC_SPC = Keycode(44)
        KC_MINUS = KC_MINS = Keycode(45)
        KC_EQUAL = KC_EQL = Keycode(46)
        KC_LBRACKET = KC_LBRC = Keycode(47)
        KC_RBRACKET = KC_RBRC = Keycode(48)
        KC_BACKSLASH = KC_BSLASH = KC_BSLS = Keycode(49)
        KC_NONUS_HASH = KC_NUHS = Keycode(50)
        KC_NONUS_BSLASH = KC_NUBS = Keycode(100)
        KC_SEMICOLON = KC_SCOLON = KC_SCLN = Keycode(51)
        KC_QUOTE = KC_QUOT = Keycode(52)
        KC_GRAVE = KC_GRV = KC_ZKHK = Keycode(53)
        KC_COMMA = KC_COMM = Keycode(54)
        KC_DOT = Keycode(55)
        KC_SLASH = KC_SLSH = Keycode(56)

    class FunctionKeys(KeycodeCategory):
        KC_F1 = Keycode(58)
        KC_F2 = Keycode(59)
        KC_F3 = Keycode(60)
        KC_F4 = Keycode(61)
        KC_F5 = Keycode(62)
        KC_F6 = Keycode(63)
        KC_F7 = Keycode(64)
        KC_F8 = Keycode(65)
        KC_F9 = Keycode(66)
        KC_F10 = Keycode(67)
        KC_F11 = Keycode(68)
        KC_F12 = Keycode(69)
        KC_F13 = Keycode(104)
        KC_F14 = Keycode(105)
        KC_F15 = Keycode(106)
        KC_F16 = Keycode(107)
        KC_F17 = Keycode(108)
        KC_F18 = Keycode(109)
        KC_F19 = Keycode(110)
        KC_F20 = Keycode(111)
        KC_F21 = Keycode(112)
        KC_F22 = Keycode(113)
        KC_F23 = Keycode(114)
        KC_F24 = Keycode(115)

    class NavAndLocks(KeycodeCategory):
        KC_CAPS_LOCK = KC_CLCK = KC_CAPS = Keycode(57)
        KC_LOCKING_CAPS = KC_LCAP = Keycode(130)
        KC_PSCREEN = KC_PSCR = Keycode(70)
        KC_SCROLLLOCK = KC_SLCK = Keycode(71)
        KC_LOCKING_SCROLL = KC_LSCRL = Keycode(132)
        KC_PAUSE = KC_PAUS = KC_BRK = Keycode(72)
        KC_INSERT = KC_INS = Keycode(73)
        KC_HOME = Keycode(74)
        KC_PGUP = Keycode(75)
        KC_DELETE = KC_DEL = Keycode(76)
        KC_END = Keycode(77)
        KC_PGDOWN = KC_PGDN = Keycode(78)
        KC_RIGHT = KC_RGHT = Keycode(79)
        KC_LEFT = Keycode(80)
        KC_DOWN = Keycode(81)
        KC_UP = Keycode(82)

    class Numpad(KeycodeCategory):
        KC_NUMLOCK = KC_NLCK = Keycode(83)
        KC_LOCKING_NUM = KC_LNUM = Keycode(131)
        KC_KP_SLASH = KC_PSLS = Keycode(84)
        KC_KP_ASTERIK = KC_PAST = Keycode(85)
        KC_KP_MINUS = KC_PMNS = Keycode(86)
        KC_KP_PLUS = KC_PPLS = Keycode(87)
        KC_KP_ENTER = KC_PENT = Keycode(88)
        KC_KP_1 = KC_P1 = Keycode(89)
        KC_KP_2 = KC_P2 = Keycode(90)
        KC_KP_3 = KC_P3 = Keycode(91)
        KC_KP_4 = KC_P4 = Keycode(92)
        KC_KP_5 = KC_P5 = Keycode(93)
        KC_KP_6 = KC_P6 = Keycode(94)
        KC_KP_7 = KC_P7 = Keycode(95)
        KC_KP_8 = KC_P8 = Keycode(96)
        KC_KP_9 = KC_P9 = Keycode(97)
        KC_KP_0 = KC_P0 = Keycode(98)
        KC_KP_DOT = KC_PDOT = Keycode(99)
        KC_KP_EQUAL = KC_PEQL = Keycode(103)
        KC_KP_COMMA = KC_PCMM = Keycode(133)
        KC_KP_EQUAL_AS400 = Keycode(134)

    class International(KeycodeCategory):
        KC_INT1 = KC_RO = Keycode(135)
        KC_INT2 = KC_KANA = Keycode(136)
        KC_INT3 = KC_JYEN = Keycode(137)
        KC_INT4 = KC_HENK = Keycode(138)
        KC_INT5 = KC_MHEN = Keycode(139)
        KC_INT6 = Keycode(140)
        KC_INT7 = Keycode(141)
        KC_INT8 = Keycode(142)
        KC_INT9 = Keycode(143)
        KC_LANG1 = KC_HAEN = Keycode(144)
        KC_LANG2 = KC_HAEJ = Keycode(145)
        KC_LANG3 = Keycode(146)
        KC_LANG4 = Keycode(147)
        KC_LANG5 = Keycode(148)
        KC_LANG6 = Keycode(149)
        KC_LANG7 = Keycode(150)
        KC_LANG8 = Keycode(151)
        KC_LANG9 = Keycode(152)

    class Misc(KeycodeCategory):
        KC_APPLICATION = KC_APP = Keycode(101)
        KC_POWER = Keycode(102)
        KC_EXECUTE = KC_EXEC = Keycode(116)
        KC_SYSTEM_POWER = KC_PWR = Keycode(165)
        KC_SYSTEM_SLEEP = KC_SLEP = Keycode(166)
        KC_SYSTEM_WAKE = KC_WAKE = Keycode(167)
        KC_HELP = Keycode(117)
        KC_MENU = Keycode(118)
        KC_SELECT = KC_SLCT = Keycode(119)
        KC_STOP = Keycode(120)
        KC_AGAIN = KC_AGIN = Keycode(121)
        KC_UNDO = Keycode(122)
        KC_CUT = Keycode(123)
        KC_COPY = Keycode(124)
        KC_PASTE = KC_PSTE = Keycode(125)
        KC_FIND = Keycode(126)
        KC_ALT_ERASE = KC_ERAS = Keycode(153)
        KC_SYSREQ = Keycode(154)
        KC_CANCEL = Keycode(155)
        KC_CLEAR = KC_CLR = Keycode(156)
        KC_PRIOR = Keycode(157)
        KC_RETURN = Keycode(158)
        KC_SEPERATOR = Keycode(159)
        KC_OUT = Keycode(160)
        KC_OPER = Keycode(161)
        KC_CLEAR_AGAIN = Keycode(162)
        KC_CRSEL = Keycode(163)
        KC_EXSEL = Keycode(164)
        KC_MAIL = Keycode(177)
        KC_CALCULATOR = KC_CALC = Keycode(178)
        KC_MY_COMPUTER = KC_MYCM = Keycode(179)
        KC_WWW_SEARCH = KC_WSCH = Keycode(180)
        KC_WWW_HOME = KC_WHOM = Keycode(181)
        KC_WWW_BACK = KC_WBAK = Keycode(182)
        KC_WWW_FORWARD = KC_WFWD = Keycode(183)
        KC_WWW_STOP = KC_WSTP = Keycode(184)
        KC_WWW_REFRESH = KC_WREF = Keycode(185)
        KC_WWW_FAVORITES = KC_WFAV = Keycode(186)

    class Media(KeycodeCategory):
        KC__MUTE = Keycode(127)
        KC__VOLUP = Keycode(128)
        KC__VOLDOWN = Keycode(129)
        KC_AUDIO_MUTE = KC_MUTE = Keycode(168)
        KC_AUDIO_VOL_UP = KC_VOLU = Keycode(169)
        KC_AUDIO_VOL_DOWN = KC_VOLD = Keycode(170)
        KC_MEDIA_NEXT_TRACK = KC_MNXT = Keycode(171)
        KC_MEDIA_PREV_TRACK = KC_MPRV = Keycode(172)
        KC_MEDIA_STOP = KC_MSTP = Keycode(173)
        KC_MEDIA_PLAY_PAUSE = KC_MPLY = Keycode(174)
        KC_MEDIA_SELECT = KC_MSEL = Keycode(175)
        KC_MEDIA_EJECT = KC_EJCT = Keycode(176)
        KC_MEDIA_FAST_FORWARD = KC_MFFD = Keycode(187)
        KC_MEDIA_REWIND = KC_MRWD = Keycode(189)

    class KMK(KeycodeCategory):
        KC_RESET = Keycode(1000)
        KC_DEBUG = Keycode(1001)
        KC_GESC = Keycode(1002)
        KC_LSPO = Keycode(1003)
        KC_RSPC = Keycode(1004)
        KC_LEAD = Keycode(1005)
        KC_LOCK = Keycode(1006)
        KC_NO = Keycode(1100)
        KC_TRNS = Keycode(1101)

    class Layers(KeycodeCategory):
        _KC_DF = 1050
        _KC_MO = 1051
        _KC_LM = 1052
        _KC_LT = 1053
        _KC_TG = 1054
        _KC_TO = 1055
        _KC_TT = 1056

        @staticmethod
        def KC_DF(layer):
            return LayerKeycode(Keycodes.Layers._KC_DF, layer)

        @staticmethod
        def KC_MO(layer):
            return LayerKeycode(Keycodes.Layers._KC_MO, layer)

        @staticmethod
        def KC_LM(layer):
            return LayerKeycode(Keycodes.Layers._KC_LM, layer)

        @staticmethod
        def KC_LT(layer):
            return LayerKeycode(Keycodes.Layers._KC_LT, layer)

        @staticmethod
        def KC_TG(layer):
            return LayerKeycode(Keycodes.Layers._KC_TG, layer)

        @staticmethod
        def KC_TO(layer):
            return LayerKeycode(Keycodes.Layers._KC_TO, layer)

        @staticmethod
        def KC_TT(layer):
            return LayerKeycode(Keycodes.Layers._KC_TT, layer)

    class ShiftedKeycodes(KeycodeCategory):
        KC_TILDE = KC_TILD = Keycode(53, (CODE_LSHIFT,))
        KC_EXCLAIM = KC_EXLM = Keycode(30, (CODE_LSHIFT,))
        KC_AT = Keycode(31, (CODE_LSHIFT,))
        KC_HASH = Keycode(32, (CODE_LSHIFT,))
        KC_DOLLAR = KC_DLR = Keycode(33, (CODE_LSHIFT,))
        KC_PERCENT = KC_PERC = Keycode(34, (CODE_LSHIFT,))
        KC_CIRCUMFLEX = KC_CIRC = Keycode(35, (CODE_LSHIFT,))  # The ^ Symbol
        KC_AMPERSAND = KC_AMPR = Keycode(36, (CODE_LSHIFT,))
        KC_ASTERISK = KC_ASTR = Keycode(37, (CODE_LSHIFT,))
        KC_LEFT_PAREN = KC_LPRN = Keycode(38, (CODE_LSHIFT,))
        KC_RIGHT_PAREN = KC_RPRN = Keycode(39, (CODE_LSHIFT,))
        KC_UNDERSCORE = KC_UNDS = Keycode(45, (CODE_LSHIFT,))
        KC_PLUS = Keycode(46, (CODE_LSHIFT,))
        KC_LEFT_CURLY_BRACE = KC_LCBR = Keycode(47, (CODE_LSHIFT,))
        KC_RIGHT_CURLY_BRACE = KC_RCBR = Keycode(48, (CODE_LSHIFT,))
        KC_PIPE = Keycode(49, (CODE_LSHIFT,))
        KC_COLON = KC_COLN = Keycode(51, (CODE_LSHIFT,))
        KC_DOUBLE_QUOTE = KC_DQUO = KC_DQT = Keycode(52, (CODE_LSHIFT,))
        KC_LEFT_ANGLE_BRACKET = KC_LABK = KC_LT = Keycode(54, (CODE_LSHIFT,))
        KC_RIGHT_ANGLE_BRACKET = KC_RABK = KC_GT = Keycode(55, (CODE_LSHIFT,))
        KC_QUESTION = KC_QUES = Keycode(56, (CODE_LSHIFT,))


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
    '+': (Keycodes.Common.KC_EQUAL, Keycodes.Modifiers.KC_LSHIFT),
    '~': (Keycodes.Common.KC_GRAVE,),
}
