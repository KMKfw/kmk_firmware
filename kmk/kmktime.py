from micropython import const
from supervisor import ticks_ms

_TICKS_PERIOD = const(1 << 29)
_TICKS_MAX = const(_TICKS_PERIOD - 1)
_TICKS_HALFPERIOD = const(_TICKS_PERIOD // 2)


def ticks_diff(new, start):
    diff = (new - start) & _TICKS_MAX
    diff = ((diff + _TICKS_HALFPERIOD) & _TICKS_MAX) - _TICKS_HALFPERIOD
    return diff


def check_deadline(new, start, ms):
    return ticks_diff(new, start) < ms


class PeriodicTimer:
    def __init__(self, period):
        self.period = period
        self.last_tick = ticks_ms()

    def tick(self):
        now = ticks_ms()
        if ticks_diff(now, self.last_tick) >= self.period:
            self.last_tick = now
            return True
        else:
            return False
