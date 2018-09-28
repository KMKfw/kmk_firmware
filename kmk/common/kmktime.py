
try:
    import utime
except ImportError:
    pass


def ticks_ms():
    return utime.ticks_ms()


def ticks_diff(new, old):
    return utime.ticks_diff(new, old)
