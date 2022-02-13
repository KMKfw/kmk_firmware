from kmk.keys import make_argumented_key
from kmk.modules.holdtap import ActivationType, HoldTap
from kmk.types import HoldTapKeyMeta


def oneshot_validator(kc, tap_time=None):
    return HoldTapKeyMeta(kc=kc, prefer_hold=False, tap_time=tap_time)


class OneShot(HoldTap):
    tap_time = 1000

    def __init__(self):
        super().__init__()
        make_argumented_key(
            validator=oneshot_validator,
            names=('OS', 'ONESHOT'),
            on_press=self.osk_pressed,
            on_release=self.osk_released,
        )

    def process_key(self, keyboard, current_key, is_pressed, int_coord):
        '''Release os key after interrupting keyup.'''
        for key, state in self.key_states.items():
            if key == current_key:
                continue

            if state.activated == ActivationType.PRESSED and is_pressed:
                state.activated = ActivationType.HOLD_TIMEOUT
            elif state.activated == ActivationType.RELEASED and is_pressed:
                state.activated = ActivationType.INTERRUPTED
            elif state.activated == ActivationType.INTERRUPTED and not is_pressed:
                self.ht_released(key, keyboard)

        return current_key

    def osk_pressed(self, key, keyboard, *args, **kwargs):
        '''Register HoldTap mechanism and activate os key.'''
        self.ht_pressed(key, keyboard, *args, **kwargs)
        self.ht_activate_tap(key, keyboard, *args, **kwargs)
        return keyboard

    def osk_released(self, key, keyboard, *args, **kwargs):
        '''On keyup, mark os key as released or handle HoldTap.'''
        try:
            state = self.key_states[key]
        except KeyError:
            if keyboard.debug_enabled:
                print(f'OneShot.osk_released: no such key {key}')
            return keyboard

        if state.activated == ActivationType.PRESSED:
            state.activated = ActivationType.RELEASED
        else:
            self.ht_released(key, keyboard, *args, **kwargs)

        return keyboard

    def ht_activate_tap(self, key, keyboard, *args, **kwargs):
        keyboard.process_key(key.meta.kc, True)

    def ht_deactivate_tap(self, key, keyboard, *args, **kwargs):
        keyboard.process_key(key.meta.kc, False)

    def ht_deactivate_hold(self, key, keyboard, *args, **kwargs):
        keyboard.process_key(key.meta.kc, False)
