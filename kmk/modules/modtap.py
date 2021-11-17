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

    def before_hid_send(self, keyboard):
        keyboard.hid_pending = True

    def ht_activate_hold(self, key, keyboard, *args, **kwargs):
        keyboard.keys_pressed.add(key.meta.mods)

    def ht_deactivate_hold(self, key, keyboard, *args, **kwargs):
        keyboard.keys_pressed.discard(key.meta.mods)

    def ht_activate_tap(self, key, keyboard, *args, **kwargs):
        keyboard.keys_pressed.add(key.meta.kc)

    def ht_deactivate_tap(self, key, keyboard, *args, **kwargs):
        keyboard.keys_pressed.discard(key.meta.kc)
