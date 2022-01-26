import kmk.handlers.stock as handlers
from kmk.key_validators import mod_tap_validator
from kmk.keys import make_argumented_key
from kmk.modules.holdtap import HoldTap


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
        handlers.default_pressed(key.meta.mods, keyboard, None)

    def ht_deactivate_hold(self, key, keyboard, *args, **kwargs):
        handlers.default_released(key.meta.mods, keyboard, None)

    def ht_activate_tap(self, key, keyboard, *args, **kwargs):
        handlers.default_pressed(key.meta.kc, keyboard, None)

    def ht_deactivate_tap(self, key, keyboard, *args, **kwargs):
        handlers.default_released(key.meta.kc, keyboard, None)
