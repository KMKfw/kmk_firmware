from kmk.keys import FIRST_KMK_INTERNAL_KEY, KC, ModifierKey, make_key
from kmk.modules import Module


class CapsWord(Module):
    # default timeout is 8000
    # alphabets, numbers and few more keys will not disable capsword
    def __init__(self, timeout=8000):
        self._alphabets = range(KC.A.code, KC.Z.code)
        self._numbers = range(KC.N1.code, KC.N0.code)
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
            on_press=self._cw_pressed,
        )

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        self.process_capsword(key, keyboard, is_pressed)
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

    def _perform_timeout(self, keyboard, key):
        self._cw_active = False
        self._timeout_key = False

    def _request_timeout(self, keyboard, key):
        if self._cw_active:
            if self.timeout:
                self._timeout_key = keyboard.set_timeout(
                    self.timeout, lambda: self._perform_timeout(keyboard, key)
                )

    def _discard_timeout(self, keyboard):
        if self._timeout_key:
            if self.timeout:
                keyboard.cancel_timeout(self._timeout_key)
            self._timeout_key = False

    def _cw_pressed(self, key, keyboard, *args, **kwargs):
        if not self._cw_active:
            self._cw_active = True
            self._discard_timeout(keyboard)
            self._request_timeout(keyboard, key)
        else:
            self._discard_timeout(keyboard)
            self._perform_timeout(keyboard, key)

    def _is_alphabet_key(self, key):
        if key.code in self._alphabets:
            return True
        return False

    def _is_addl_ignored_key(self, key):
        if (
            key.code in self._numbers
            or isinstance(key, ModifierKey)
            or key in self.keys_ignored
            or key.code
            # user defined keys are also ignored
            >= FIRST_KMK_INTERNAL_KEY
        ):
            return True
        return False

    # requests and cancels existing timeouts
    def _orchestrate_timeout(self, key, keyboard, ignored):
        if ignored:
            self._discard_timeout(keyboard)
            self._request_timeout(keyboard, key)
        else:
            self._perform_timeout(keyboard, key)

    def get_tap_capsword(self, key, keyboard):
        if self._cw_active:
            ignored = False
            # capitalize alphabets
            if self._is_alphabet_key(key):
                ignored = True
                key = KC.LSFT(key)
            elif self._is_addl_ignored_key(key):
                ignored = True

            self._orchestrate_timeout(key, keyboard, ignored)
        return key

    def process_capsword(self, key, keyboard, is_pressed):
        if self._cw_active:
            ignored = False
            # capitalize alphabets
            if self._is_alphabet_key(key):
                ignored = True
                keyboard.process_key(KC.LSFT, is_pressed)
            elif self._is_addl_ignored_key(key):
                ignored = True

            if is_pressed:
                self._orchestrate_timeout(key, keyboard, ignored)
