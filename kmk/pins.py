from micropython import const

from kmk.consts import CIRCUITPYTHON, MICROPYTHON

PULL_UP = const(1)
PULL_DOWN = const(2)


try:
    import board
    import digitalio

    PLATFORM = CIRCUITPYTHON
    PIN_SOURCE = board
except ImportError:
    import machine

    PLATFORM = MICROPYTHON
    PIN_SOURCE = machine.Pin.board


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


class AbstractedDigitalPin:
    def __init__(self, pin):
        self.raw_pin = pin

        if PLATFORM == CIRCUITPYTHON:
            self.pin = digitalio.DigitalInOut(pin)
        elif PLATFORM == MICROPYTHON:
            self.pin = machine.Pin(pin)
        else:
            self.pin = pin

        self.call_value = callable(self.pin.value)

    def __repr__(self):
        return 'AbstractedPin({})'.format(repr(self.raw_pin))

    def switch_to_input(self, pull=None):
        if PLATFORM == CIRCUITPYTHON:
            if pull == PULL_UP:
                return self.pin.switch_to_input(pull=digitalio.Pull.UP)
            elif pull == PULL_DOWN:
                return self.pin.switch_to_input(pull=digitalio.Pull.DOWN)

            return self.pin.switch_to_input(pull=pull)

        elif PLATFORM == MICROPYTHON:
            if pull == PULL_UP:
                return self.pin.init(machine.Pin.IN, machine.Pin.PULL_UP)
            elif pull == PULL_DOWN:
                return self.pin.init(machine.Pin.IN, machine.Pin.PULL_DOWN)

            raise ValueError('only PULL_UP and PULL_DOWN supported on MicroPython')

        raise NotImplementedError('switch_to_input not supported on platform')

    def switch_to_output(self):
        if PLATFORM == CIRCUITPYTHON:
            return self.pin.switch_to_output()
        elif PLATFORM == MICROPYTHON:
            return self.pin.init(machine.Pin.OUT)

        raise NotImplementedError('switch_to_output not supported on platform')

    def value(self, value=None):
        if value is None:
            if self.call_value:
                return self.pin.value()
            return self.pin.value

        if self.call_value:
            return self.pin.value(value)
        self.pin.value = value
        return value


class PinLookup:
    def __getattr__(self, attr):
        return AbstractedDigitalPin(get_pin(attr))


Pin = PinLookup()
