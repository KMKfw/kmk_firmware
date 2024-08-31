from kmk.keys import make_argumented_key
from kmk.modules.holdtap import ActivationType, HoldTap, HoldTapKey
from kmk.modules.layers import LayerKey
from kmk.utils import Debug

debug = Debug(__name__)


class OneShotKey(HoldTapKey):
    def __init__(self, kc, tap_time=None, **kwargs):
        super().__init__(
            tap=kc,
            hold=kc,
            prefer_hold=False,
            tap_interrupted=False,
            tap_time=tap_time,
            repeat=0,
            **kwargs,
        )


class OneShot(HoldTap):
    '''This module is deprecated; use sticky_keys instead.'''

    tap_time = 1000

    def __init__(self):
        super().__init__()
        debug(
            'Warning: OneShot module is deprecated and will be removed; use sticky_keys instead.'
        )
        make_argumented_key(
            names=('OS', 'ONESHOT'),
            constructor=OneShotKey,
            on_press=self.osk_pressed,
            on_release=self.osk_released,
        )

    def process_key(self, keyboard, current_key, is_pressed, int_coord):
        '''Release os key after interrupting non-os keyup, or reset timeout and
        stack multiple os keys.'''
        send_buffer = False

        for key, state in self.key_states.items():
            if key == current_key:
                continue

            if (isinstance(current_key, OneShotKey)) or (
                isinstance(current_key, LayerKey)
            ):
                keyboard.cancel_timeout(state.timeout_key)
                if key.tap_time is None:
                    tap_time = self.tap_time
                else:
                    tap_time = key.tap_time
                state.timeout_key = keyboard.set_timeout(
                    tap_time,
                    lambda k=key: self.on_tap_time_expired(k, keyboard),
                )
                continue

            if state.activated == ActivationType.PRESSED and is_pressed:
                state.activated = ActivationType.HOLD_TIMEOUT
            elif state.activated == ActivationType.RELEASED and is_pressed:
                state.activated = ActivationType.INTERRUPTED
            elif state.activated == ActivationType.INTERRUPTED:
                if is_pressed:
                    send_buffer = True
                self.key_buffer.insert(0, (None, key, False))

        if send_buffer:
            self.key_buffer.append((int_coord, current_key, is_pressed))
            current_key = None

        self.send_key_buffer(keyboard)

        return current_key

    def osk_pressed(self, key, keyboard, *args, **kwargs):
        '''Register HoldTap mechanism and activate os key.'''
        self.ht_pressed(key, keyboard, *args, **kwargs)
        self.ht_activate_tap(key, keyboard, *args, **kwargs)
        self.send_key_buffer(keyboard)
        return keyboard

    def osk_released(self, key, keyboard, *args, **kwargs):
        '''On keyup, mark os key as released or handle HoldTap.'''
        try:
            state = self.key_states[key]
        except KeyError:
            if debug.enabled:
                debug(f'OneShot.osk_released: no such key {key}')
            return keyboard

        if state.activated == ActivationType.PRESSED:
            state.activated = ActivationType.RELEASED
        else:
            self.ht_released(key, keyboard, *args, **kwargs)

        return keyboard
