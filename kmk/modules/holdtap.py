from micropython import const

from kmk.modules import Module
from kmk.types import ModTapKeyMeta


class ActivationType:
    NOT_ACTIVATED = const(0)
    HOLD_TIMEOUT = const(1)
    INTERRUPTED = const(2)


class HoldTapKeyState:
    def __init__(self, timeout_key, *args, **kwargs):
        self.timeout_key = timeout_key
        self.args = args
        self.kwargs = kwargs
        self.activated = ActivationType.NOT_ACTIVATED


class HoldTap(Module):
    tap_time = 300

    def __init__(self):
        self.key_states = {}

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed):
        '''Before other key down decide to send tap kc down.'''
        current_key = key
        if is_pressed and not isinstance(key.meta, ModTapKeyMeta):
            for key, state in self.key_states.items():
                if state.activated == ActivationType.NOT_ACTIVATED:
                    # press tap because interrupted by other key
                    self.key_states[key].activated = ActivationType.INTERRUPTED
                    self.ht_activate_on_interrupt(
                        key, keyboard, *state.args, **state.kwargs
                    )
                    if keyboard.hid_pending:
                        keyboard._send_hid()
        return current_key

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def ht_pressed(self, key, keyboard, *args, **kwargs):
        '''Do nothing yet, action resolves when key is released, timer expires or other key is pressed.'''
        timeout_key = keyboard.set_timeout(
            self.tap_time,
            lambda: self.on_tap_time_expired(key, keyboard, *args, **kwargs),
        )
        self.key_states[key] = HoldTapKeyState(timeout_key, *args, **kwargs)
        return keyboard

    def ht_released(self, key, keyboard, *args, **kwargs):
        '''On keyup, release mod or tap key.'''
        if key in self.key_states:
            state = self.key_states[key]
            keyboard.cancel_timeout(state.timeout_key)
            if state.activated == ActivationType.HOLD_TIMEOUT:
                # release hold
                self.ht_deactivate_hold(key, keyboard, *args, **kwargs)
            elif state.activated == ActivationType.INTERRUPTED:
                # release tap
                self.ht_deactivate_on_interrupt(key, keyboard, *args, **kwargs)
            else:
                # press and release tap because key released within tap time
                self.ht_activate_tap(key, keyboard, *args, **kwargs)
                keyboard.set_timeout(
                    False,
                    lambda: self.ht_deactivate_tap(key, keyboard, *args, **kwargs),
                )
            del self.key_states[key]
        return keyboard

    def on_tap_time_expired(self, key, keyboard, *args, **kwargs):
        '''When tap time expires activate mod if key is still being pressed.'''
        if (
            key in self.key_states
            and self.key_states[key].activated == ActivationType.NOT_ACTIVATED
        ):
            # press hold because timer expired after tap time
            self.key_states[key].activated = ActivationType.HOLD_TIMEOUT
            self.ht_activate_hold(key, keyboard, *args, **kwargs)

    def ht_activate_hold(self, key, keyboard, *args, **kwargs):
        pass

    def ht_deactivate_hold(self, key, keyboard, *args, **kwargs):
        pass

    def ht_activate_tap(self, key, keyboard, *args, **kwargs):
        pass

    def ht_deactivate_tap(self, key, keyboard, *args, **kwargs):
        pass

    def ht_activate_on_interrupt(self, key, keyboard, *args, **kwargs):
        self.ht_activate_tap(key, keyboard, *args, **kwargs)

    def ht_deactivate_on_interrupt(self, key, keyboard, *args, **kwargs):
        self.ht_deactivate_tap(key, keyboard, *args, **kwargs)
