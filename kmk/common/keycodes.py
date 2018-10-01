try:
    from collections import namedtuple
except ImportError:
    # This is handled by micropython-lib/collections, but on local runs of
    # MicroPython, it doesn't exist
    from ucollections import namedtuple

from kmk.common.consts import UnicodeModes
from kmk.common.types import AttrDict
from kmk.common.util import flatten_dict

FIRST_KMK_INTERNAL_KEYCODE = 1000


class RawKeycodes:
    '''
    These are raw keycode numbers for keys we'll use in generated "keys".
    For example, we want to be able to check against these numbers in
    the internal_keycodes reducer fragments, but due to a limitation in
    MicroPython, we can't simply assign the `.code` attribute to
    a function (which is what most internal KMK keys (including layer stuff)
    are implemented as). Thus, we have to keep an external lookup table.
    '''
    LCTRL = 0x01
    LSHIFT = 0x02
    LALT = 0x04
    LGUI = 0x08
    RCTRL = 0x10
    RSHIFT = 0x20
    RALT = 0x40
    RGUI = 0x80

    KC_DF = 1050
    KC_MO = 1051
    KC_LM = 1052
    KC_LT = 1053
    KC_TG = 1054
    KC_TO = 1055
    KC_TT = 1056

    KC_UC_MODE = 1109


# These shouldn't have all the fancy shenanigans Keycode allows
# such as no_press, because they modify KMK internal state in
# ways we need to tightly control. Thus, we can get away with
# a lighter-weight namedtuple implementation here
LayerKeycode = namedtuple('LayerKeycode', ('code', 'layer'))


class UnicodeModeKeycode(namedtuple('UnicodeModeKeycode', ('code', 'mode'))):
    @staticmethod
    def from_mode_const(mode):
        return UnicodeModeKeycode(RawKeycodes.KC_UC_MODE, mode)


class Keycode:
    def __init__(self, code, has_modifiers=None, no_press=False, no_release=False):
        self.code = code
        self.has_modifiers = has_modifiers
        # cast to bool() in case we get a None value
        self.no_press = bool(no_press)
        self.no_release = bool(no_press)

    def __call__(self, no_press=None, no_release=None):
        if no_press is None and no_release is None:
            return self

        return Keycode(
            code=self.code,
            has_modifiers=self.has_modifiers,
            no_press=no_press,
            no_release=no_release,
        )


class ModifierKeycode(Keycode):
    def __call__(self, modified_code=None, no_press=None, no_release=None):
        if modified_code is None and no_press is None and no_release is None:
            return self

        new_keycode = Keycode(
            modified_code.code,
            {self.code},
            no_press=no_press,
            no_release=no_release,
        )

        if modified_code.has_modifiers:
            new_keycode.has_modifiers |= modified_code.has_modifiers

        return new_keycode


class ConsumerKeycode(Keycode):
    pass


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


class Modifiers(KeycodeCategory):
    KC_LCTRL = KC_LCTL = ModifierKeycode(RawKeycodes.LCTRL)
    KC_LSHIFT = KC_LSFT = ModifierKeycode(RawKeycodes.LSHIFT)
    KC_LALT = ModifierKeycode(RawKeycodes.LALT)
    KC_LGUI = KC_LCMD = KC_LWIN = ModifierKeycode(RawKeycodes.LGUI)
    KC_RCTRL = KC_RCTL = ModifierKeycode(RawKeycodes.RCTRL)
    KC_RSHIFT = KC_RSFT = ModifierKeycode(RawKeycodes.RSHIFT)
    KC_RALT = ModifierKeycode(RawKeycodes.RALT)
    KC_RGUI = KC_RCMD = KC_RWIN = ModifierKeycode(RawKeycodes.RGUI)


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


class ShiftedKeycodes(KeycodeCategory):
    KC_TILDE = KC_TILD = Modifiers.KC_LSHIFT(Common.KC_GRAVE)
    KC_EXCLAIM = KC_EXLM = Modifiers.KC_LSHIFT(Common.KC_1)
    KC_AT = Modifiers.KC_LSHIFT(Common.KC_2)
    KC_HASH = Modifiers.KC_LSHIFT(Common.KC_3)
    KC_DOLLAR = KC_DLR = Modifiers.KC_LSHIFT(Common.KC_4)
    KC_PERCENT = KC_PERC = Modifiers.KC_LSHIFT(Common.KC_5)
    KC_CIRCUMFLEX = KC_CIRC = Modifiers.KC_LSHIFT(Common.KC_6)  # The ^ Symbol
    KC_AMPERSAND = KC_AMPR = Modifiers.KC_LSHIFT(Common.KC_7)
    KC_ASTERISK = KC_ASTR = Modifiers.KC_LSHIFT(Common.KC_8)
    KC_LEFT_PAREN = KC_LPRN = Modifiers.KC_LSHIFT(Common.KC_9)
    KC_RIGHT_PAREN = KC_RPRN = Modifiers.KC_LSHIFT(Common.KC_0)
    KC_UNDERSCORE = KC_UNDS = Modifiers.KC_LSHIFT(Common.KC_MINUS)
    KC_PLUS = Modifiers.KC_LSHIFT(Common.KC_EQUAL)
    KC_LEFT_CURLY_BRACE = KC_LCBR = Modifiers.KC_LSHIFT(Common.KC_LBRACKET)
    KC_RIGHT_CURLY_BRACE = KC_RCBR = Modifiers.KC_LSHIFT(Common.KC_RBRACKET)
    KC_PIPE = Modifiers.KC_LSHIFT(Common.KC_BACKSLASH)
    KC_COLON = KC_COLN = Modifiers.KC_LSHIFT(Common.KC_SEMICOLON)
    KC_DOUBLE_QUOTE = KC_DQUO = KC_DQT = Modifiers.KC_LSHIFT(Common.KC_QUOTE)
    KC_LEFT_ANGLE_BRACKET = KC_LABK = KC_LT = Modifiers.KC_LSHIFT(Common.KC_COMMA)
    KC_RIGHT_ANGLE_BRACKET = KC_RABK = KC_GT = Modifiers.KC_LSHIFT(Common.KC_DOT)
    KC_QUESTION = KC_QUES = Modifiers.KC_LSHIFT(Common.KC_DOT)


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
    KC_APPLICATION = KC_APP = ConsumerKeycode(101)
    KC_POWER = ConsumerKeycode(102)
    KC_EXECUTE = KC_EXEC = ConsumerKeycode(116)
    KC_SYSTEM_POWER = KC_PWR = ConsumerKeycode(165)
    KC_SYSTEM_SLEEP = KC_SLEP = ConsumerKeycode(166)
    KC_SYSTEM_WAKE = KC_WAKE = ConsumerKeycode(167)
    KC_HELP = ConsumerKeycode(117)
    KC_MENU = ConsumerKeycode(118)
    KC_SELECT = KC_SLCT = ConsumerKeycode(119)
    KC_STOP = ConsumerKeycode(120)
    KC_AGAIN = KC_AGIN = ConsumerKeycode(121)
    KC_UNDO = ConsumerKeycode(122)
    KC_CUT = ConsumerKeycode(123)
    KC_COPY = ConsumerKeycode(124)
    KC_PASTE = KC_PSTE = ConsumerKeycode(125)
    KC_FIND = ConsumerKeycode(126)
    KC_ALT_ERASE = KC_ERAS = ConsumerKeycode(153)
    KC_SYSREQ = ConsumerKeycode(154)
    KC_CANCEL = ConsumerKeycode(155)
    KC_CLEAR = KC_CLR = ConsumerKeycode(156)
    KC_PRIOR = ConsumerKeycode(157)
    KC_RETURN = ConsumerKeycode(158)
    KC_SEPERATOR = ConsumerKeycode(159)
    KC_OUT = ConsumerKeycode(160)
    KC_OPER = ConsumerKeycode(161)
    KC_CLEAR_AGAIN = ConsumerKeycode(162)
    KC_CRSEL = ConsumerKeycode(163)
    KC_EXSEL = ConsumerKeycode(164)
    KC_MAIL = ConsumerKeycode(177)
    KC_CALCULATOR = KC_CALC = ConsumerKeycode(178)
    KC_MY_COMPUTER = KC_MYCM = ConsumerKeycode(179)
    KC_WWW_SEARCH = KC_WSCH = ConsumerKeycode(180)
    KC_WWW_HOME = KC_WHOM = ConsumerKeycode(181)
    KC_WWW_BACK = KC_WBAK = ConsumerKeycode(182)
    KC_WWW_FORWARD = KC_WFWD = ConsumerKeycode(183)
    KC_WWW_STOP = KC_WSTP = ConsumerKeycode(184)
    KC_WWW_REFRESH = KC_WREF = ConsumerKeycode(185)
    KC_WWW_FAVORITES = KC_WFAV = ConsumerKeycode(186)


class Media(KeycodeCategory):
    # I believe QMK used these double-underscore codes for MacOS
    # support or something. I have no idea, but modern MacOS supports
    # PC volume keys so I really don't care that these codes are the
    # same as below. If bugs arise, these codes may need to change.
    KC__MUTE = ConsumerKeycode(226)
    KC__VOLUP = ConsumerKeycode(233)
    KC__VOLDOWN = ConsumerKeycode(234)

    KC_AUDIO_MUTE = KC_MUTE = ConsumerKeycode(226)  # 0xE2
    KC_AUDIO_VOL_UP = KC_VOLU = ConsumerKeycode(233)  # 0xE9
    KC_AUDIO_VOL_DOWN = KC_VOLD = ConsumerKeycode(234)  # 0xEA
    KC_MEDIA_NEXT_TRACK = KC_MNXT = ConsumerKeycode(181)  # 0xB5
    KC_MEDIA_PREV_TRACK = KC_MPRV = ConsumerKeycode(182)  # 0xB6
    KC_MEDIA_STOP = KC_MSTP = ConsumerKeycode(183)  # 0xB7
    KC_MEDIA_PLAY_PAUSE = KC_MPLY = ConsumerKeycode(205)  # 0xCD (this may not be right)
    KC_MEDIA_EJECT = KC_EJCT = ConsumerKeycode(184)  # 0xB8
    KC_MEDIA_FAST_FORWARD = KC_MFFD = ConsumerKeycode(179)  # 0xB3
    KC_MEDIA_REWIND = KC_MRWD = ConsumerKeycode(180)  # 0xB4


class KMK(KeycodeCategory):
    KC_RESET = Keycode(1000)
    KC_DEBUG = Keycode(1001)
    KC_GESC = Keycode(1002)
    KC_LSPO = Keycode(1003)
    KC_RSPC = Keycode(1004)
    KC_LEAD = Keycode(1005)
    KC_LOCK = Keycode(1006)
    KC_NO = Keycode(1107)
    KC_TRANSPARENT = KC_TRNS = Keycode(1108)

    @staticmethod
    def KC_UC_MODE(mode):
        '''
        Set any Unicode Mode at runtime (allows the same keymap's unicode
        sequences to work across all supported platforms)
        '''
        return UnicodeModeKeycode.from_mode_const(mode)

    KC_UC_MODE_NOOP = KC_UC_DISABLE = UnicodeModeKeycode.from_mode_const(UnicodeModes.NOOP)
    KC_UC_MODE_LINUX = KC_UC_MODE_IBUS = UnicodeModeKeycode.from_mode_const(UnicodeModes.IBUS)
    KC_UC_MODE_MACOS = KC_UC_MODE_OSX = KC_UC_MODE_RALT = UnicodeModeKeycode.from_mode_const(
        UnicodeModes.RALT,
    )


class Layers(KeycodeCategory):
    @staticmethod
    def KC_DF(layer):
        return LayerKeycode(RawKeycodes.KC_DF, layer)

    @staticmethod
    def KC_MO(layer):
        return LayerKeycode(RawKeycodes.KC_MO, layer)

    @staticmethod
    def KC_LM(layer):
        return LayerKeycode(RawKeycodes.KC_LM, layer)

    @staticmethod
    def KC_LT(layer):
        return LayerKeycode(RawKeycodes.KC_LT, layer)

    @staticmethod
    def KC_TG(layer):
        return LayerKeycode(RawKeycodes.KC_TG, layer)

    @staticmethod
    def KC_TO(layer):
        return LayerKeycode(RawKeycodes.KC_TO, layer)

    @staticmethod
    def KC_TT(layer):
        return LayerKeycode(RawKeycodes.KC_TT, layer)


class Keycodes(KeycodeCategory):
    '''
    A massive grouping of keycodes

    Some of these are from http://www.freebsddiary.org/APC/usb_hid_usages.php,
    one of the most useful pages on the interwebs for HID stuff, apparently.
    '''

    Modifiers = Modifiers
    Common = Common
    ShiftedKeycodes = ShiftedKeycodes
    FunctionKeys = FunctionKeys
    NavAndLocks = NavAndLocks
    Numpad = Numpad
    International = International
    Misc = Misc
    Media = Media
    KMK = KMK
    Layers = Layers


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
