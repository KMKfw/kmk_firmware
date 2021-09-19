from kmk.key_validators import mod_tap_validator
from kmk.keys import make_argumented_key
from kmk.modules import Module


class HoldTapKeyState:
    def __init__(self, timeout_key, *args, **kwargs):
        self.timeout_key = timeout_key
        self.args = args
        self.kwargs = kwargs
        self.activated = False


class HoldTap(Module):
    def __init__(self):
        self.key_states = {}

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        '''Before other key down decide to send tap kc down.'''
        if self.matrix_detected_press(keyboard):
            for key, state in self.key_states.items():
                if not state.activated:
                    # press tap because interrupted by other key
                    self.key_states[key].activated = 'interrupt'
                    self.ht_activate_on_interrupt(
                        key, keyboard, *state.args, **state.kwargs
                    )
                    if keyboard.hid_pending:
                        keyboard._send_hid()
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def matrix_detected_press(self, keyboard):
        return (keyboard.matrix_update is not None and keyboard.matrix_update[2]) or (
            keyboard.secondary_matrix_update is not None
            and keyboard.secondary_matrix_update[2]
        )

    def ht_pressed(self, key, keyboard, *args, **kwargs):
        '''Do nothing yet, action resolves when key is released, timer expires or other key is pressed.'''
        timeout_key = keyboard.set_timeout(
            keyboard.tap_time,
            lambda: self.on_tap_time_expired(key, keyboard, *args, **kwargs),
        )
        self.key_states[key] = HoldTapKeyState(timeout_key, *args, **kwargs)
        return keyboard

    def ht_released(self, key, keyboard, *args, **kwargs):
        '''On keyup, release mod or tap key.'''
        if key in self.key_states:
            state = self.key_states[key]
            keyboard.cancel_timeout(state.timeout_key)
            if state.activated == 'hold':
                # release hold
                self.ht_deactivate_hold(key, keyboard, *args, **kwargs)
            elif state.activated == 'interrupt':
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
        if key in self.key_states and not self.key_states[key].activated:
            # press hold because timer expired after tap time
            self.key_states[key].activated = 'hold'
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


class ModTap(HoldTap):
    def __init__(self):
        super().__init__()
        make_argumented_key(
            validator=mod_tap_validator,
            names=('MT',),
            on_press=self.ht_pressed,
            on_release=self.ht_released,
        )

    def ht_activate_hold(self, key, keyboard, *args, **kwargs):
        keyboard.hid_pending = True
        keyboard.keys_pressed.add(key.meta.mods)

    def ht_deactivate_hold(self, key, keyboard, *args, **kwargs):
        keyboard.hid_pending = True
        keyboard.keys_pressed.discard(key.meta.mods)

    def ht_activate_tap(self, key, keyboard, *args, **kwargs):
        keyboard.hid_pending = True
        keyboard.keys_pressed.add(key.meta.kc)

    def ht_deactivate_tap(self, key, keyboard, *args, **kwargs):
        keyboard.hid_pending = True
        keyboard.keys_pressed.discard(key.meta.kc)
