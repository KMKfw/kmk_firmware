import time


def sleep_ms(ms: float) -> None:
    return time.sleep(ms / 1000)


def ticks_ms() -> float:
    '''Has .25s granularity, but is cheap'''
    return time.monotonic() * 1000


def ticks_diff(new: float, old: float) -> float:
    return new - old


def accurate_ticks() -> int:
    '''Is more expensive, but good for time critical things'''
    return time.monotonic_ns()


def accurate_ticks_diff(new: float, old: float, ms: float) -> bool:
    return bool(new - old < ms * 1000000)
