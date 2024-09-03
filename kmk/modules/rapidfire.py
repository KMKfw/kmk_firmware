from micropython import const

from random import randint

from kmk.keys import Key, make_argumented_key
from kmk.modules import Module
from kmk.utils import Debug

debug = Debug(__name__)

_INACTIVE = const(0)
_HOLD = const(1)
_ACTIVE = const(2)


class RapidFireKey(Key):
    def __init__(
        self,
        key,
        interval=100,
        timeout=200,
        enable_interval_randomization=False,
        randomization_magnitude=15,
        toggle=False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.key = key
        self.interval = interval
        self.timeout = timeout
        self.enable_interval_randomization = enable_interval_randomization
        self.randomization_magnitude = randomization_magnitude
        self.toggle = toggle
        self._state = _INACTIVE
        self._timeout = None


class RapidFire(Module):
    def __init__(self):
        make_argumented_key(
            names=('RF',),
            constructor=RapidFireKey,
            on_press=self._rf_pressed,
            on_release=self._rf_released,
        )

    def _on_timer_timeout(self, key, keyboard):
        if key._state == _HOLD:
            key._state = _ACTIVE
            keyboard.remove_key(key.key)
            key._timeout = keyboard.set_timeout(
                1, lambda: self._on_timer_timeout(key, keyboard)
            )
            return

        keyboard.add_key(key.key)
        keyboard.set_timeout(1, lambda: keyboard.remove_key(key.key))

        interval = key.interval
        if key.enable_interval_randomization:
            interval += randint(
                -key.randomization_magnitude, key.randomization_magnitude
            )
        key._timeout = keyboard.set_timeout(
            interval, lambda: self._on_timer_timeout(key, keyboard)
        )

        if debug.enabled:
            debug(key.key, ' @', interval, 'ms')

    def _rf_pressed(self, key, keyboard, *args, **kwargs):
        if key._state == _ACTIVE:
            self._deactivate_key(key, keyboard)
            return

        keyboard.add_key(key.key)
        key._state = _HOLD
        key._timeout = keyboard.set_timeout(
            key.timeout, lambda: self._on_timer_timeout(key, keyboard)
        )

    def _rf_released(self, key, keyboard, *args, **kwargs):
        if key._state == _ACTIVE:
            if key.toggle:
                return
            key._state = _INACTIVE
        elif key._state == _INACTIVE:
            return
        else:
            keyboard.remove_key(key.key)

        self._deactivate_key(key, keyboard)

    def _deactivate_key(self, key, keyboard):
        keyboard.cancel_timeout(key._timeout)
        key._state = _INACTIVE
        key._timeout = None

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
