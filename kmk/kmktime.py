import time


def sleep_ms(ms):
    # type: (float) -> None
    return time.sleep(ms / 1000)


def ticks_ms():
    # type: () -> float
    '''Has .25s granularity, but is cheap'''
    return time.monotonic() * 1000


def ticks_diff(new, old):
    # type: (float, float) -> float
    return new - old


def accurate_ticks():
    # type: () -> int
    '''Is more expensive, but good for time critical things'''
    return time.monotonic_ns()


def accurate_ticks_diff(new, old, ms):
    # type: (float, float, float) -> bool
    return bool(new - old < ms * 1000000)
