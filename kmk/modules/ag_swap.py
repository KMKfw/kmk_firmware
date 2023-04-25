from kmk.keys import KC, ModifierKey, make_key
from kmk.modules import Module


class AgSwap(Module):
    # default ag swap is disabled, can be eanbled too if needed
    def __init__(self, ag_swap_enable=False):
        self.ag_swap_enable = ag_swap_enable
        self._ag_mapping = {
            KC.LALT: KC.LGUI,
            KC.RALT: KC.RGUI,
            KC.LGUI: KC.LALT,
            KC.RGUI: KC.RALT,
        }
        make_key(
            names=('AG_SWAP',),
        )
        make_key(
            names=('AG_NORM',),
        )
        make_key(
            names=('AG_TOGG',),
        )

    def during_bootup(self, keyboard):
        return

    def matrix_detected_press(self, keyboard):
        return keyboard.matrix_update is None

    def before_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if is_pressed:
            # enables or disables or toggles ag swap
            if key == KC.AG_SWAP:
                self.ag_swap_enable = True
            elif key == KC.AG_NORM:
                self.ag_swap_enable = False
            elif key == KC.AG_TOGG:
                if not self.ag_swap_enable:
                    self.ag_swap_enable = True
                else:
                    self.ag_swap_enable = False
            # performs cg swap
            if (
                self.ag_swap_enable
                and key not in (KC.AG_SWAP, KC.AG_NORM, KC.AG_TOGG)
                and isinstance(key, ModifierKey)
                and key in self._ag_mapping
            ):
                key = self._ag_mapping.get(key)

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
