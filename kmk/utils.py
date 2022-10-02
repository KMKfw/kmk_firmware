from supervisor import ticks_ms


def clamp(x: int, bottom: int = 0, top: int = 100) -> int:
    return min(max(bottom, x), top)


_debug_enabled = False


class Debug:
    '''default usage:
    debug = Debug(__name__)
    '''

    def __init__(self, name: str = __name__):
        self.name = name

    def __call__(self, message: str) -> None:
        print(f'{ticks_ms()} {self.name}: {message}')

    @property
    def enabled(self) -> bool:
        global _debug_enabled
        return _debug_enabled

    @enabled.setter
    def enabled(self, enabled: bool):
        global _debug_enabled
        _debug_enabled = enabled
