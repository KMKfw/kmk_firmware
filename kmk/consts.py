from micropython import const


class UnicodeMode:
    NOOP = const(0)
    LINUX = IBUS = const(1)
    MACOS = OSX = RALT = const(2)
    WINC = const(3)
