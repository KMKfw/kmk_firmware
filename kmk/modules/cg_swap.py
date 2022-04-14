from kmk.keys import KC, ModifierKey, make_key
from kmk.modules import Module


class CgSwap(Module):
    # default cg swap is disabled, can be eanbled too if needed
    def __init__(self, cg_swap_enable=False):
        self.cg_swap_enable = cg_swap_enable
        self._cg_mapping = {
            KC.LCTL: KC.LGUI,
            KC.RCTL: KC.RGUI,
            KC.LGUI: KC.LCTL,
            KC.RGUI: KC.RCTL,
        }
        make_key(
            names=('CG_SWAP',),
            on_press=self._cg_swap_pressed,
        )
        make_key(
            names=('CG_NORM',),
            on_press=self._cg_norm_pressed,
        )
        make_key(
            names=('CG_TOGG',),
            on_press=self._cg_togg_pressed,
        )

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if (
            is_pressed
            and self.cg_swap_enable
            and key not in (KC.CG_SWAP, KC.CG_NORM, KC.CG_TOGG)
            and isinstance(key, ModifierKey)
            and key in self._cg_mapping
        ):
            key = self._cg_mapping.get(key)

        return key

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def process_cg_swap(self, key):
        if self.cg_swap_enable and key in self._cg_mapping:
            return self._cg_mapping.get(key)
        else:
            return key

    def _cg_swap_pressed(self, key, keyboard, *args, **kwargs):
        self.cg_swap_enable = True

    def _cg_norm_pressed(self, key, keyboard, *args, **kwargs):
        self.cg_swap_enable = False

    def _cg_togg_pressed(self, key, keyboard, *args, **kwargs):
        if not self.cg_swap_enable:
            self.cg_swap_enable = True
        else:
            self.cg_swap_enable = False
