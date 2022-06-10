from micropython import const

from kmk.keys import make_argumented_key
from kmk.modules import Module
from kmk.types import HoldTapKeyMeta


class ActivationType:
    PRESSED = const(0)
    RELEASED = const(1)
    HOLD_TIMEOUT = const(2)
    INTERRUPTED = const(3)


class HoldTapKeyState:
    def __init__(self, timeout_key, *args, **kwargs):
        self.timeout_key = timeout_key
        self.args = args
        self.kwargs = kwargs
        self.activated = ActivationType.PRESSED


class HoldTap(Module):
    tap_time = 300

    def __init__(self):
        self.key_buffer = []
        self.key_states = {}
        make_argumented_key(
            validator=HoldTapKeyMeta,
            names=('HT',),
            on_press=self.ht_pressed,
            on_release=self.ht_released,
        )

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        '''Handle holdtap being interrupted by another key press/release.'''
        current_key = key
        send_buffer = False
        append_buffer = False

        for key, state in self.key_states.items():
            if key == current_key:
                continue
            if state.activated != ActivationType.PRESSED:
                continue

            # holdtap is interrupted by another key event.
            if (is_pressed and not key.meta.tap_interrupted) or (
                not is_pressed and key.meta.tap_interrupted and self.key_buffer
            ):

                keyboard.cancel_timeout(state.timeout_key)
                self.key_states[key].activated = ActivationType.INTERRUPTED
                self.ht_activate_on_interrupt(
                    key, keyboard, *state.args, **state.kwargs
                )
                keyboard._send_hid()
                send_buffer = True

            if state.activated == ActivationType.INTERRUPTED:
                current_key = keyboard._find_key_in_map(int_coord)

            # if interrupt on release: store interrupting keys until one of them
            # is released.
            if (
                key.meta.tap_interrupted
                and is_pressed
                and not isinstance(current_key.meta, HoldTapKeyMeta)
            ):
                append_buffer = True

        # apply changes with 'side-effects' on key_states or the loop behaviour
        # outside the loop.
        if append_buffer:
            self.key_buffer.append((int_coord, current_key))
            current_key = None
        elif send_buffer:
            self.send_key_buffer(keyboard)

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
        if key.meta.tap_time is None:
            tap_time = self.tap_time
        else:
            tap_time = key.meta.tap_time
        timeout_key = keyboard.set_timeout(
            tap_time,
            lambda: self.on_tap_time_expired(key, keyboard, *args, **kwargs),
        )
        self.key_states[key] = HoldTapKeyState(timeout_key, *args, **kwargs)
        return keyboard

    def ht_released(self, key, keyboard, *args, **kwargs):
        '''On keyup, release mod or tap key.'''
        if key not in self.key_states:
            return keyboard

        state = self.key_states[key]
        keyboard.cancel_timeout(state.timeout_key)

        if state.activated == ActivationType.HOLD_TIMEOUT:
            # release hold
            self.ht_deactivate_hold(key, keyboard, *args, **kwargs)
        elif state.activated == ActivationType.INTERRUPTED:
            # release tap
            self.ht_deactivate_on_interrupt(key, keyboard, *args, **kwargs)
        elif state.activated == ActivationType.PRESSED:
            # press and release tap because key released within tap time
            self.ht_activate_tap(key, keyboard, *args, **kwargs)
            keyboard.set_timeout(
                False,
                lambda: self.ht_deactivate_tap(key, keyboard, *args, **kwargs),
            )
            state.activated = ActivationType.RELEASED
            self.send_key_buffer(keyboard)
        del self.key_states[key]

        return keyboard

    def on_tap_time_expired(self, key, keyboard, *args, **kwargs):
        '''When tap time expires activate hold if key is still being pressed.
        Remove key if ActivationType is RELEASED.'''
        try:
            state = self.key_states[key]
        except KeyError:
            if keyboard.debug_enabled:
                print(f'HoldTap.on_tap_time_expired: no such key {key}')
            return

        if self.key_states[key].activated == ActivationType.PRESSED:
            # press hold because timer expired after tap time
            self.key_states[key].activated = ActivationType.HOLD_TIMEOUT
            self.ht_activate_hold(key, keyboard, *args, **kwargs)
            self.send_key_buffer(keyboard)
        elif state.activated == ActivationType.RELEASED:
            self.ht_deactivate_tap(key, keyboard, *args, **kwargs)
            del self.key_states[key]

    def send_key_buffer(self, keyboard):
        key_buffer = self.key_buffer
        self.key_buffer = []
        for (int_coord, key) in key_buffer:
            new_key = keyboard._find_key_in_map(int_coord)
            keyboard.pre_process_key(new_key, True, int_coord)
        keyboard._send_hid()
        self.key_buffer.clear()

    def ht_activate_hold(self, key, keyboard, *args, **kwargs):
        keyboard.process_key(key.meta.hold, True)

    def ht_deactivate_hold(self, key, keyboard, *args, **kwargs):
        keyboard.process_key(key.meta.hold, False)

    def ht_activate_tap(self, key, keyboard, *args, **kwargs):
        keyboard.process_key(key.meta.tap, True)

    def ht_deactivate_tap(self, key, keyboard, *args, **kwargs):
        keyboard.process_key(key.meta.tap, False)

    def ht_activate_on_interrupt(self, key, keyboard, *args, **kwargs):
        if key.meta.prefer_hold:
            self.ht_activate_hold(key, keyboard, *args, **kwargs)
        else:
            self.ht_activate_tap(key, keyboard, *args, **kwargs)

    def ht_deactivate_on_interrupt(self, key, keyboard, *args, **kwargs):
        if key.meta.prefer_hold:
            self.ht_deactivate_hold(key, keyboard, *args, **kwargs)
        else:
            self.ht_deactivate_tap(key, keyboard, *args, **kwargs)
