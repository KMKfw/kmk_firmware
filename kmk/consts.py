try:
    from kmk.release_info import KMK_RELEASE
except Exception:
    KMK_RELEASE = 'copied-from-git'


class UnicodeMode:
    NOOP = 0
    LINUX = IBUS = 1
    MACOS = OSX = RALT = 2
    WINC = 3
