import math
import time

USE_UTIME = False


def sleep_ms(ms):
    '''
    Tries to sleep for a number of milliseconds in a cross-implementation
    way. Will raise an ImportError if time is not available on the platform.
    '''
    if USE_UTIME:
        return time.sleep_ms(ms)
    else:
        return time.sleep(ms / 1000)


def ticks_ms():
    if USE_UTIME:
        return time.ticks_ms()
    else:
        return math.floor(time.monotonic() * 1000)


def ticks_diff(new, old):
    if USE_UTIME:
        return time.ticks_diff(new, old)
    else:
        return new - old
