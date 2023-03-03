from kmk.keys import make_argumented_key
from kmk.modules.holdtap import HoldTap, HoldTapKeyMeta


# Deprecation Notice: The `ModTap` class serves as an alias for `HoldTap` and will be removed in a future update. Please use `HoldTap` instead.
class ModTap(HoldTap):
    def __init__(self):
        super().__init__()
        make_argumented_key(
            validator=HoldTapKeyMeta,
            names=('MT',),
            on_press=self.ht_pressed,
            on_release=self.ht_released,
        )
