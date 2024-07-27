from kmk.keys import KC, KeyboardKey, ModifierKey, make_key
from kmk.modules import Module


class CapsWord(Module):
    # default timeout is 8000
    # alphabets, numbers and few more keys will not disable capsword
    def __init__(self, timeout=8000):
        self._alphabets = range(KC.A.code, KC.Z.code + 1)
        self._numbers = range(KC.N1.code, KC.N0.code + 1)
        self.keys_ignored = [
            KC.MINS,
            KC.BSPC,
            KC.UNDS,
        ]
        self._timeout_key = False
        self._cw_active = False
        self.timeout = timeout
        make_key(
            names=(
                'CAPSWORD',
                'CW',
            ),
            on_press=self.cw_pressed,
        )

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not self._cw_active or key == KC.CW:
            return key

        continue_cw = False

        # capitalize alphabets
        if isinstance(key, KeyboardKey) and key.code in self._alphabets:
            keyboard.process_key(KC.LSFT, is_pressed)
            continue_cw = True
        elif (
            not isinstance(key, KeyboardKey)
            or isinstance(key, ModifierKey)
            or key.code in self._numbers
            or key in self.keys_ignored
        ):
            continue_cw = True

        # requests and cancels existing timeouts
        if is_pressed:
            if continue_cw:
                self.discard_timeout(keyboard)
                self.request_timeout(keyboard)
            else:
                self.process_timeout()

        return key

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def process_timeout(self):
        self._cw_active = False
        self._timeout_key = False

    def request_timeout(self, keyboard):
        if self._cw_active:
            if self.timeout:
                self._timeout_key = keyboard.set_timeout(
                    self.timeout, lambda: self.process_timeout()
                )

    def discard_timeout(self, keyboard):
        if self._timeout_key:
            if self.timeout:
                keyboard.cancel_timeout(self._timeout_key)
            self._timeout_key = False

    def cw_pressed(self, key, keyboard, *args, **kwargs):
        # enables/disables capsword
        if key == KC.CW:
            if not self._cw_active:
                self._cw_active = True
                self.discard_timeout(keyboard)
                self.request_timeout(keyboard)
            else:
                self.discard_timeout(keyboard)
                self.process_timeout()
