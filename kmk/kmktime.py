import time


def sleep_ms(ms):
    return time.sleep(ms / 1000)


def ticks_ms():
    '''Has .25s granularity, but is cheap'''
    return time.monotonic() * 1000


def ticks_diff(new, old):
    return new - old


def accurate_ticks():
    '''Is more expensive, but good for time critical things'''
    return time.monotonic_ns()


def accurate_ticks_diff(new, old, ms):
    return bool(new - old < ms * 1000000)
