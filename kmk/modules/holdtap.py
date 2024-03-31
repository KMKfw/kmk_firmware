from micropython import const

from kmk.keys import KC, make_argumented_key
from kmk.modules import Module
from kmk.utils import Debug

debug = Debug(__name__)


class HoldTapRepeat:
    NONE = const(0)
    TAP = const(1)
    HOLD = const(2)
    ALL = const(3)


class HoldTapKeyState:

    RELEASED = const(0)
    PRESSED = const(1)
    HOLD_TIMEOUT = const(2)
    INTERRUPTED = const(3)
    REPEAT = const(4)

    def __init__(self, timeout_key, *args, **kwargs):
        self.timeout_key = timeout_key
        self.args = args
        self.kwargs = kwargs
        self.key_state = HoldTapKeyState.PRESSED
        self.active_kc = None
        self.may_repeat = False


class HoldTapKeyMeta:
    def __init__(
        self,
        tap,
        hold,
        prefer_hold=True,
        tap_interrupted=False,
        tap_time=None,
        repeat=HoldTapRepeat.NONE,
    ):
        self.tap = tap
        self.hold = hold
        self.prefer_hold = prefer_hold
        self.tap_interrupted = tap_interrupted
        self.tap_time = tap_time
        self.repeat = repeat


class HoldTap(Module):
    tap_time = 300

    def __init__(self):
        self.key_buffer = []
        self.key_states = {}
        if KC.get('HT') == KC.NO:
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
            if state.key_state != HoldTapKeyState.PRESSED:
                continue

            # holdtap isn't interruptable, resolves on ht_release or timeout.
            if not key.meta.tap_interrupted and not key.meta.prefer_hold:
                append_buffer = True
                continue

            # holdtap is interrupted by another key event.
            if (is_pressed and not key.meta.tap_interrupted) or (
                not is_pressed and key.meta.tap_interrupted and self.key_buffer
            ):

                keyboard.cancel_timeout(state.timeout_key)
                self.key_states[key].key_state = HoldTapKeyState.INTERRUPTED
                self.ht_activate_on_interrupt(
                    state, key, keyboard, *state.args, **state.kwargs
                )
                append_buffer = True
                send_buffer = True

            # if interrupt on release: store interrupting keys until one of them
            # is released.
            if key.meta.tap_interrupted and is_pressed:
                append_buffer = True

        # apply changes with 'side-effects' on key_states or the loop behaviour
        # outside the loop.
        if append_buffer:
            self.key_buffer.append((int_coord, current_key, is_pressed))
            current_key = None

        if send_buffer:
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
        '''Unless in repeat mode, do nothing yet, action resolves when key is released, timer expires or other key is pressed.'''
        if key in self.key_states:
            state = self.key_states[key]
            keyboard.cancel_timeout(self.key_states[key].timeout_key)

            if state.may_repeat and state.active_kc != None:
                state.key_state = HoldTapKeyState.REPEAT
                self.ht_activate_repeat(state, key, keyboard, *args, **kwargs)
            return

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

        if state.key_state == HoldTapKeyState.HOLD_TIMEOUT:
            # release hold
            self.ht_deactivate(state, key, keyboard, *args, **kwargs)
        elif state.key_state == HoldTapKeyState.INTERRUPTED:
            # release tap
            self.ht_deactivate(state, key, keyboard, *args, **kwargs)
        elif state.key_state == HoldTapKeyState.PRESSED:
            # press and release tap because key released within tap time
            self.ht_activate_tap(state, key, keyboard, *args, **kwargs)
            self.send_key_buffer(keyboard)
            self.ht_deactivate(state, key, keyboard, *args, **kwargs)
            self.send_key_buffer(keyboard)
        elif state.key_state == HoldTapKeyState.REPEAT:
            self.ht_deactivate(state, key, keyboard, *args, **kwargs)

        state.key_state = HoldTapKeyState.RELEASED

        # don't delete the key state right now in this case
        if state.may_repeat:
            if key.meta.tap_time is None:
                tap_time = self.tap_time
            else:
                tap_time = key.meta.tap_time
            state.timeout_key = keyboard.set_timeout(
                tap_time, lambda: self.key_states.pop(key)
            )
        else:
            del self.key_states[key]

        return keyboard

    def on_tap_time_expired(self, key, keyboard, *args, **kwargs):
        '''When tap time expires activate hold if key is still being pressed.
        Remove key if key_state is RELEASED.'''
        try:
            state = self.key_states[key]
        except KeyError:
            if debug.enabled:
                debug(f'on_tap_time_expired: no such key {key}')
            return

        if self.key_states[key].key_state == HoldTapKeyState.PRESSED:
            # press hold because timer expired after tap time
            self.key_states[key].key_state = HoldTapKeyState.HOLD_TIMEOUT
            self.ht_activate_hold(state, key, keyboard, *args, **kwargs)
            self.send_key_buffer(keyboard)
        elif state.key_state == HoldTapKeyState.RELEASED:
            del self.key_states[key]

    def send_key_buffer(self, keyboard):
        if not self.key_buffer:
            return

        reprocess = False
        for int_coord, key, is_pressed in self.key_buffer:
            keyboard.resume_process_key(self, key, is_pressed, int_coord, reprocess)
            if isinstance(key.meta, HoldTapKeyMeta):
                reprocess = True

        self.key_buffer.clear()

    def ht_activate_hold(self, state, key, keyboard, *args, **kwargs):
        if debug.enabled:
            debug('ht_activate_hold')
        state.active_kc = key.meta.hold
        state.may_repeat = key.meta.repeat & HoldTapRepeat.HOLD
        keyboard.resume_process_key(self, state.active_kc, True)

    def ht_activate_tap(self, state, key, keyboard, *args, **kwargs):
        if debug.enabled:
            debug('ht_activate_tap')
        state.active_kc = key.meta.tap
        state.may_repeat = key.meta.repeat & HoldTapRepeat.TAP
        keyboard.resume_process_key(self, state.active_kc, True)

    def ht_activate_on_interrupt(self, state, key, keyboard, *args, **kwargs):
        if debug.enabled:
            debug('ht_activate_on_interrupt')
        if key.meta.prefer_hold:
            self.ht_activate_hold(state, key, keyboard, *args, **kwargs)
        else:
            self.ht_activate_tap(state, key, keyboard, *args, **kwargs)

    def ht_activate_repeat(self, state, key, keyboard, *args, **kwargs):
        if debug.enabled:
            debug('ht_activate_repeat')
        keyboard.resume_process_key(self, state.active_kc, True)

    def ht_deactivate(self, state, key, keyboard, *args, **kwargs):
        if state.active_kc is not None:
            if debug.enabled:
                debug('ht_deactivate')
            keyboard.resume_process_key(self, state.active_kc, False)
