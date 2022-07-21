import kmk.handlers.stock as handlers
from kmk.keys import make_argumented_key
from kmk.modules.holdtap import HoldTap, HoldTapKeyMeta


def mod_tap_validator(
    kc, mods=None, prefer_hold=True, tap_interrupted=False, tap_time=None
):
    '''
    Validates that mod tap keys are correctly used
    '''
    return ModTapKeyMeta(
        kc=kc,
        mods=mods,
        prefer_hold=prefer_hold,
        tap_interrupted=tap_interrupted,
        tap_time=tap_time,
    )


class ModTapKeyMeta(HoldTapKeyMeta):
    def __init__(self, kc=None, mods=None, **kwargs):
        super().__init__(tap=kc, hold=mods, **kwargs)


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
        handlers.default_pressed(key.meta.hold, keyboard, None)

    def ht_deactivate_hold(self, key, keyboard, *args, **kwargs):
        handlers.default_released(key.meta.hold, keyboard, None)

    def ht_activate_tap(self, key, keyboard, *args, **kwargs):
        handlers.default_pressed(key.meta.tap, keyboard, None)

    def ht_deactivate_tap(self, key, keyboard, *args, **kwargs):
        handlers.default_released(key.meta.tap, keyboard, None)
