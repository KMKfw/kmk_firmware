class DiodeOrientation:
    '''
    Orientation of diodes on handwired boards. You can think of:
    COLUMNS = vertical
    ROWS = horizontal
    '''

    COLUMNS = 0
    ROWS = 1


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
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith('_')
        }

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
        KC_CTRL = KC_LEFT_CTRL = 0x01
        KC_SHIFT = KC_LEFT_SHIFT = 0x02
        KC_ALT = KC_LALT = 0x04
        KC_GUI = KC_LGUI = 0x08
        KC_RCTRL = 0x10
        KC_RSHIFT = 0x20
        KC_RALT = 0x40
        KC_RGUI = 0x80

    class Common(KeycodeCategory):
        KC_A = 4
        KC_B = 5
        KC_C = 6
        KC_D = 7
        KC_E = 8
        KC_F = 9
        KC_G = 10
        KC_H = 11
        KC_I = 12
        KC_J = 13
        KC_K = 14
        KC_L = 15
        KC_M = 16
        KC_N = 17
        KC_O = 18
        KC_P = 19
        KC_Q = 20
        KC_R = 21
        KC_S = 22
        KC_T = 23
        KC_U = 24
        KC_V = 25
        KC_W = 26
        KC_X = 27
        KC_Y = 28
        KC_Z = 29
        KC_1 = 30
        KC_2 = 31
        KC_3 = 32
        KC_4 = 33
        KC_5 = 34
        KC_6 = 35
        KC_7 = 36
        KC_8 = 37
        KC_9 = 38
        KC_0 = 39

        KC_ENTER = 40
        KC_ESC = 41
        KC_BACKSPACE = 42
        KC_TAB = 43
        KC_SPACE = 44
        KC_MINUS = 45
        KC_EQUAL = 46
        KC_LBRC = 47
        KC_RBRC = 48
        KC_BACKSLASH = 49
        KC_NUMBER = 50
        KC_SEMICOLON = 51
        KC_QUOTE = 52
        KC_TILDE = 53
        KC_COMMA = 54
        KC_PERIOD = 55
        KC_SLASH = 56
        KC_CAPS_LOCK = 57

    class FunctionKeys(KeycodeCategory):
        KC_F1 = 58
        KC_F2 = 59
        KC_F3 = 60
        KC_F4 = 61
        KC_F5 = 62
        KC_F6 = 63
        KC_F7 = 64
        KC_F8 = 65
        KC_F9 = 66
        KC_F10 = 67
        KC_F11 = 68
        KC_F12 = 69

    class NavAndLocks(KeycodeCategory):
        KC_PRINTSCREEN = 70
        KC_SCROLL_LOCK = 71
        KC_PAUSE = 72
        KC_INSERT = 73
        KC_HOME = 74
        KC_PGUP = 75
        KC_DELETE = 76
        KC_END = 77
        KC_PGDN = 78
        KC_RIGHT = 79
        KC_LEFT = 80
        KC_DOWN = 81
        KC_UP = 82

    class Numpad(KeycodeCategory):
        KC_NUMLOCK = 83
        KC_KP_SLASH = 84
        KC_KP_ASTERIX = 85
        KC_KP_MINUS = 86
        KC_KP_PLUS = 87
        KC_KP_ENTER = 88
        KC_KP_1 = 89
        KC_KP_2 = 90
        KC_KP_3 = 91
        KC_KP_4 = 92
        KC_KP_5 = 93
        KC_KP_6 = 94
        KC_KP_7 = 95
        KC_KP_8 = 96
        KC_KP_9 = 97
        KC_KP_0 = 98
        KC_KP_PERIOD = 99


char_lookup = {
    "\n": (Keycodes.Common.KC_ENTER,),
    "\t": (Keycodes.Common.KC_TAB,),
    ' ': (Keycodes.Common.KC_SPACE,),
    '-': (Keycodes.Common.KC_MINUS,),
    '=': (Keycodes.Common.KC_EQUAL,),
    '+': (Keycodes.Common.KC_EQUAL, Keycodes.Modifiers.KC_SHIFT),
    '~': (Keycodes.Common.KC_TILDE,),
}
