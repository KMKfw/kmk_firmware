try:
    from kmk.release_info import KMK_RELEASE
except Exception:
    KMK_RELEASE = 'copied-from-git'


class UnicodeMode:
    NOOP = 0
    LINUX = IBUS = 1
    MACOS = OSX = RALT = 2
    WINC = 3


class LeaderMode:
    TIMEOUT = 0
    TIMEOUT_ACTIVE = 1
    ENTER = 2
    ENTER_ACTIVE = 3
