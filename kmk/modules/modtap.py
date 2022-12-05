from kmk.keys import KC, maybe_make_argumented_key
from kmk.modules.holdtap import HoldTap, HoldTapKeyMeta


class ModTap(HoldTap):
    def __init__(self):
        super().__init__()
        KC._generators.append(
            maybe_make_argumented_key(
                validator=HoldTapKeyMeta,
                names=('MT',),
                on_press=self.ht_pressed,
                on_release=self.ht_released,
            )
        )
