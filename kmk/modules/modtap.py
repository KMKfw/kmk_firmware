from kmk.key_validators import mod_tap_validator
from kmk.keys import make_argumented_key
from kmk.kmktime import accurate_ticks, accurate_ticks_diff
from kmk.modules import Module


class ModTap(Module):
    def __init__(self):
        self._mod_tap_timer = None
        make_argumented_key(
            validator=mod_tap_validator,
            names=('MT',),
            on_press=self.mt_pressed,
            on_release=self.mt_released,
        )

    def during_bootup(self, keyboard):
        return

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

    def mt_pressed(self, key, keyboard, *args, **kwargs):
        '''Sets the timer start and acts like a modifier otherwise'''
        keyboard.keys_pressed.add(key.meta.mods)

        self._mod_tap_timer = accurate_ticks()
        return keyboard

    def mt_released(self, key, keyboard, *args, **kwargs):
        '''On keyup, check timer, and press key if needed.'''
        keyboard.keys_pressed.discard(key.meta.mods)
        if self._mod_tap_timer and (
            accurate_ticks_diff(
                accurate_ticks(), self._mod_tap_timer, keyboard.tap_time
            )
        ):
            keyboard.hid_pending = True
            keyboard.tap_key(key.meta.kc)

        self._mod_tap_timer = None
        return keyboard
