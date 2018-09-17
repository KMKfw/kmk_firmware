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
        KC_CTRL = KC_LEFT_CTRL = Keycode(0x01, True)
        KC_SHIFT = KC_LEFT_SHIFT = Keycode(0x02, True)
        KC_ALT = KC_LALT = Keycode(0x04, True)
        KC_GUI = KC_LGUI = Keycode(0x08, True)
        KC_RCTRL = Keycode(0x10, True)
        KC_RSHIFT = Keycode(0x20, True)
        KC_RALT = Keycode(0x40, True)
        KC_RGUI = Keycode(0x80, True)

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

        KC_ENTER = Keycode(40, False)
        KC_ESC = Keycode(41, False)
        KC_BACKSPACE = Keycode(42, False)
        KC_TAB = Keycode(43, False)
        KC_SPACE = Keycode(44, False)
        KC_MINUS = Keycode(45, False)
        KC_EQUAL = Keycode(46, False)
        KC_LBRC = Keycode(47, False)
        KC_RBRC = Keycode(48, False)
        KC_BACKSLASH = Keycode(49, False)
        KC_NUMBER = Keycode(50, False)
        KC_SEMICOLON = Keycode(51, False)
        KC_QUOTE = Keycode(52, False)
        KC_TILDE = Keycode(53, False)
        KC_COMMA = Keycode(54, False)
        KC_PERIOD = Keycode(55, False)
        KC_SLASH = Keycode(56, False)
        KC_CAPS_LOCK = Keycode(57, False)

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

    class NavAndLocks(KeycodeCategory):
        KC_PRINTSCREEN = Keycode(70, False)
        KC_SCROLL_LOCK = Keycode(71, False)
        KC_PAUSE = Keycode(72, False)
        KC_INSERT = Keycode(73, False)
        KC_HOME = Keycode(74, False)
        KC_PGUP = Keycode(75, False)
        KC_DELETE = Keycode(76, False)
        KC_END = Keycode(77, False)
        KC_PGDN = Keycode(78, False)
        KC_RIGHT = Keycode(79, False)
        KC_LEFT = Keycode(80, False)
        KC_DOWN = Keycode(81, False)
        KC_UP = Keycode(82, False)

    class Numpad(KeycodeCategory):
        KC_NUMLOCK = Keycode(83, False)
        KC_KP_SLASH = Keycode(84, False)
        KC_KP_ASTERIX = Keycode(85, False)
        KC_KP_MINUS = Keycode(86, False)
        KC_KP_PLUS = Keycode(87, False)
        KC_KP_ENTER = Keycode(88, False)
        KC_KP_1 = Keycode(89, False)
        KC_KP_2 = Keycode(90, False)
        KC_KP_3 = Keycode(91, False)
        KC_KP_4 = Keycode(92, False)
        KC_KP_5 = Keycode(93, False)
        KC_KP_6 = Keycode(94, False)
        KC_KP_7 = Keycode(95, False)
        KC_KP_8 = Keycode(96, False)
        KC_KP_9 = Keycode(97, False)
        KC_KP_0 = Keycode(98, False)
        KC_KP_PERIOD = Keycode(99, False)


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
