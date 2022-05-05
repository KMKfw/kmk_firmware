from kmk.extensions import Extension
from kmk.keys import KC


class StringyKeymaps(Extension):
    #####
    # User-configurable
    debug_enabled = False

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        for _, layer in enumerate(keyboard.keymap):
            for key_idx, key in enumerate(layer):
                if isinstance(key, str):
                    replacement = KC.get(key)
                    if replacement is None:
                        replacement = KC.NO
                        if self.debug_enabled:
                            print(f"Failed replacing '{key}'. Using KC.NO")
                    elif self.debug_enabled:
                        print(f"Replacing '{key}' with {replacement}")
                    layer[key_idx] = replacement

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return
