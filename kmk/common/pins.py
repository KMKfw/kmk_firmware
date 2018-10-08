try:
    import board

    PLATFORM = 'CircuitPython'
    PIN_SOURCE = board
except ImportError:
    import machine

    PLATFORM = 'MicroPython'
    PIN_SOURCE = machine.Pin.board
except ImportError:
    from kmk.common.types import Passthrough

    PLATFORM = 'Unit Testing'
    PIN_SOURCE = Passthrough()


def get_pin(pin):
    '''
    Cross-platform method to find a pin by string.

    The pin definitions are platform-dependent, but this provides
    a way to say "I'm using pin D20" without rolling a D20 and
    having to actually learn MicroPython/CircuitPython and the
    differences in how they handle pinouts.

    This also makes the keymap sanity checker actually work for
    CircuitPython boards, since it's not possible in CPY to
    define a module stub for `board` that uses Passthrough
    natively (which is how the MicroPython stub worked originally)
    '''
    return getattr(PIN_SOURCE, pin)


class PinLookup:
    def __getattr__(self, attr):
        return get_pin(attr)


Pin = PinLookup()
