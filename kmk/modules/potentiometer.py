from analogio import AnalogIn
from supervisor import ticks_ms

from kmk.modules import Module


class PotentiometerState:
    def __init__(self, direction: int, position: int):
        self.direction = direction
        self.position = position


class Potentiometer:
    def __init__(self, pin, move_callback, is_inverted=False):
        self.is_inverted = is_inverted
        self.read_pin = AnalogIn(pin)
        self._direction = None
        self._pos = self.get_pos()
        self._timestamp = ticks_ms()
        self.cb = move_callback

        # callback function on events.
        self.on_move_do = lambda state: self.cb(state)

    def get_state(self) -> PotentiometerState:
        return PotentiometerState(
            direction=(self.is_inverted and -self._direction or self._direction),
            position=(self.is_inverted and -self._pos or self._pos),
        )

    def get_pos(self):
        '''
        Read from the analog pin assingned, truncate to 7 bits,
        average over 10 readings, and return a value 0-127
        '''
        return int(sum([(self.read_pin.value >> 9) for i in range(10)]) / 10)

    def update_state(self):
        self._direction = 0
        new_pos = self.get_pos()
        if abs(new_pos - self._pos) > 2:
            # movement detected!
            if new_pos > self._pos:
                self._direction = 1
            else:
                self._direction = -1
            self._pos = new_pos
            if self.on_move_do is not None:
                self.on_move_do(self.get_state())


class PotentiometerHandler(Module):
    def __init__(self):
        self.potentiometers = []
        self.pins = None

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        if self.pins:
            for args in self.pins:
                self.potentiometers.append(Potentiometer(*args))
        return

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        for potentiometer in self.potentiometers:
            potentiometer.update_state()

        return keyboard

    def after_matrix_scan(self, keyboard):
        '''
        Return value will be replace matrix update if supplied
        '''
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return
