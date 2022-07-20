from supervisor import ticks_ms


def clamp(x, bottom=0, top=100):
    return min(max(bottom, x), top)


_debug_enabled = False


class Debug:
    '''default usage:
    debug = Debug(__name__)
    '''

    def __init__(self, name=__name__):
        self.name = name

    def __call__(self, message):
        print(f'{ticks_ms()} {self.name}: {message}')

    @property
    def enabled(self):
        global _debug_enabled
        return _debug_enabled

    @enabled.setter
    def enabled(self, enabled):
        global _debug_enabled
        _debug_enabled = enabled
