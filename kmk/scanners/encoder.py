import keypad
import rotaryio

from kmk.scanners import Scanner


class RotaryioEncoder(Scanner):
    def __init__(self, pin_a, pin_b, divisor=4):
        self.encoder = rotaryio.IncrementalEncoder(pin_a, pin_b, divisor)
        self.position = 0
        self._pressed = False
        self._queue = []

    @property
    def key_count(self):
        return 2

    def scan_for_changes(self):
        position = self.encoder.position

        if position != self.position:
            self._queue.append(position - self.position)
            self.position = position

        if not self._queue:
            return

        key_number = self.offset
        if self._queue[0] > 0:
            key_number += 1

        if self._pressed:
            self._queue[0] -= 1 if self._queue[0] > 0 else -1

            if self._queue[0] == 0:
                self._queue.pop(0)

            self._pressed = False

        else:
            self._pressed = True

        return keypad.Event(key_number, self._pressed)
