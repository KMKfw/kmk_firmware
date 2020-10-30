from kmk.extensions import Extension
from kmk.key_validators import mod_tap_validator
from kmk.keys import make_argumented_key
from kmk.kmktime import accurate_ticks, accurate_ticks_diff


class ModTap(Extension):
    def __init__(self):
        self._mod_tap_timer = None
        make_argumented_key(
            validator=mod_tap_validator,
            names=('MT',),
            on_press=self.mt_pressed,
            on_release=self.mt_released,
        )

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard, matrix_update):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def mt_pressed(self, key, state, *args, **kwargs):
        '''Sets the timer start and acts like a modifier otherwise'''
        state.keys_pressed.add(key.meta.mods)

        self._mod_tap_timer = accurate_ticks()
        return state

    def mt_released(self, key, state, *args, **kwargs):
        ''' On keyup, check timer, and press key if needed.'''
        state.keys_pressed.discard(key.meta.mods)
        if self._mod_tap_timer and (
            accurate_ticks_diff(accurate_ticks(), self._mod_tap_timer, state.tap_time)
        ):
            state.hid_pending = True
            state.tap_key(key.meta.kc)

        self._mod_tap_timer = None
        return state
