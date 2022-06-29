from random import randint

from kmk.keys import make_argumented_key
from kmk.modules import Module


class RapidFireMeta:
    def __init__(
        self,
        kc,
        interval=100,
        timeout=200,
        enable_interval_randomization=False,
        randomization_magnitude=15,
        toggle=False,
    ):
        self.kc = kc
        self.interval = interval
        self.timeout = timeout
        self.enable_interval_randomization = enable_interval_randomization
        self.randomization_magnitude = randomization_magnitude
        self.toggle = toggle


class RapidFire(Module):
    _active_keys = {}
    _toggled_keys = []
    _waiting_keys = []

    def __init__(self):
        make_argumented_key(
            validator=RapidFireMeta,
            names=('RF',),
            on_press=self._rf_pressed,
            on_release=self._rf_released,
        )

    def _get_repeat(self, key):
        if key.meta.enable_interval_randomization:
            return key.meta.interval + randint(
                -key.meta.randomization_magnitude, key.meta.randomization_magnitude
            )
        return key.meta.interval

    def _on_timer_timeout(self, key, keyboard):
        keyboard.tap_key(key.meta.kc)
        if key in self._waiting_keys:
            self._waiting_keys.remove(key)
        if key.meta.toggle and key not in self._toggled_keys:
            self._toggled_keys.append(key)
        self._active_keys[key] = keyboard.set_timeout(
            self._get_repeat(key), lambda: self._on_timer_timeout(key, keyboard)
        )

    def _rf_pressed(self, key, keyboard, *args, **kwargs):
        if key in self._toggled_keys:
            self._toggled_keys.remove(key)
            self._deactivate_key(key, keyboard)
            return
        if key.meta.timeout > 0:
            keyboard.tap_key(key.meta.kc)
            self._waiting_keys.append(key)
            self._active_keys[key] = keyboard.set_timeout(
                key.meta.timeout, lambda: self._on_timer_timeout(key, keyboard)
            )
        else:
            self._on_timer_timeout(key, keyboard)

    def _rf_released(self, key, keyboard, *args, **kwargs):
        if key not in self._active_keys:
            return
        if key in self._toggled_keys:
            if key not in self._waiting_keys:
                return
            self._toggled_keys.remove(key)
        if key in self._waiting_keys:
            self._waiting_keys.remove(key)
        self._deactivate_key(key, keyboard)

    def _deactivate_key(self, key, keyboard):
        keyboard.cancel_timeout(self._active_keys[key])
        self._active_keys.pop(key)

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

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
