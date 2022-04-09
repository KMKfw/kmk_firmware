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
        )
        make_key(
            names=('CG_NORM',),
        )
        make_key(
            names=('CG_TOGG',),
        )

    def during_bootup(self, keyboard):
        return

    def matrix_detected_press(self, keyboard):
        return keyboard.matrix_update is None

    def before_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if is_pressed:
            # enables or disables or toggles cg swap
            if key == KC.CG_SWAP:
                self.cg_swap_enable = True
            elif key == KC.CG_NORM:
                self.cg_swap_enable = False
            elif key == KC.CG_TOGG:
                if not self.cg_swap_enable:
                    self.cg_swap_enable = True
                else:
                    self.cg_swap_enable = False
            # performs cg swap
            if (
                self.cg_swap_enable
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
