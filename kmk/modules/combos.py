import kmk.handlers.stock as handlers
from kmk.keys import make_key
from kmk.modules import Module


class Combo:
    timeout = 50
    per_key_timeout = False
    _timeout = None
    _remaining = []

    def __init__(self, match, result, timeout=None, per_key_timeout=None):
        '''
        match: tuple of keys (KC.A, KC.B)
        result: key KC.C
        '''
        self.match = match
        self.result = result
        if timeout:
            self.timeout = timeout
        if per_key_timeout:
            self.per_key_timeout = per_key_timeout

    def matches(self, key):
        raise NotImplementedError

    def reset(self):
        self._remaining = list(self.match)


class Chord(Combo):
    def matches(self, key):
        try:
            self._remaining.remove(key)
            return True
        except ValueError:
            return False


class Sequence(Combo):
    timeout = 1000
    per_key_timeout = True

    def matches(self, key):
        try:
            return key == self._remaining.pop(0)
        except IndexError:
            return False


class Combos(Module):
    def __init__(self, combos=[]):
        self.combos = combos
        self._active = []
        self._matching = []
        self._reset = set()
        self._key_buffer = []

        make_key(
            names=('LEADER',),
            on_press=handlers.passthrough,
            on_release=handlers.passthrough,
        )

    def during_bootup(self, keyboard):
        self.reset(keyboard)

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if is_pressed:
            return self.on_press(keyboard, key)
        else:
            return self.on_release(keyboard, key)

    def on_press(self, keyboard, key):
        # refill potential matches from timed-out matches
        if not self._matching:
            self._matching = list(self._reset)
            self._reset = set()

        # filter potential matches
        for combo in self._matching.copy():
            if combo.matches(key):
                continue
            self._matching.remove(combo)
            if combo._timeout:
                keyboard.cancel_timeout(combo._timeout)
            combo._timeout = keyboard.set_timeout(
                combo.timeout, lambda c=combo: self.reset_combo(keyboard, c)
            )

        if self._matching:
            # At least one combo matches current key: append key to buffer.
            self._key_buffer.append((key, True))
            key = None

            # Start or reset individual combo timeouts.
            for combo in self._matching:
                if combo._timeout:
                    if combo.per_key_timeout:
                        keyboard.cancel_timeout(combo._timeout)
                    else:
                        continue
                combo._timeout = keyboard.set_timeout(
                    combo.timeout, lambda c=combo: self.on_timeout(keyboard, c)
                )
        else:
            # There's no matching combo: send and reset key buffer
            self.send_key_buffer(keyboard)
            self._key_buffer = []

        return key

    def on_release(self, keyboard, key):
        for combo in self._active:
            if key in combo.match:
                # Deactivate combo if it matches current key.
                self.deactivate(keyboard, combo)
                self.reset_combo(keyboard, combo)
                key = combo.result
                break

        # Don't propagate key-release events for keys that have been buffered.
        # Append release events only if corresponding press is in buffer.
        else:
            pressed = self._key_buffer.count((key, True))
            released = self._key_buffer.count((key, False))
            if (pressed - released) > 0:
                self._key_buffer.append((key, False))
                key = None

        return key

    def on_timeout(self, keyboard, combo):
        # If combo reaches timeout and has no remaining keys, activate it;
        # else, drop it from the match list.
        combo._timeout = None
        self._matching.remove(combo)

        if not combo._remaining:
            self.activate(keyboard, combo)
            if any([not pressed for (key, pressed) in self._key_buffer]):
                # At least one of the combo keys has already been released:
                # "tap" the combo result.
                keyboard._send_hid()
                self.deactivate(keyboard, combo)
            self.reset(keyboard)
            self._key_buffer = []
        else:
            if not self._matching:
                # This was the last pending combo: flush key buffer.
                self.send_key_buffer(keyboard)
                self._key_buffer = []
            self.reset_combo(keyboard, combo)

    def send_key_buffer(self, keyboard):
        for (key, is_pressed) in self._key_buffer:
            keyboard.process_key(key, is_pressed)
            keyboard._send_hid()

    def activate(self, keyboard, combo):
        combo.result.on_press(keyboard)
        self._active.append(combo)

    def deactivate(self, keyboard, combo):
        combo.result.on_release(keyboard)
        self._active.remove(combo)

    def reset_combo(self, keyboard, combo):
        combo.reset()
        if combo._timeout is not None:
            keyboard.cancel_timeout(combo._timeout)
            combo._timeout = None
        self._reset.add(combo)

    def reset(self, keyboard):
        self._matching = []
        for combo in self.combos:
            self.reset_combo(keyboard, combo)
