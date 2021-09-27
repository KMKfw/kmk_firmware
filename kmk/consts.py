from micropython import const

try:
    from kmk.release_info import KMK_RELEASE
except Exception:
    KMK_RELEASE = 'copied-from-git'


class UnicodeMode:
    NOOP = const(0)
    LINUX = IBUS = const(1)
    MACOS = OSX = RALT = const(2)
    WINC = const(3)


TYPING_PLATFORMS = [
    'linux',
    'linux2',
    'win32',
    'cygwin',
    'msys',
    'darwin',
    'freebsd7',
    'freebsd8',
    'freebsdN',
    'openbsd6',
]
