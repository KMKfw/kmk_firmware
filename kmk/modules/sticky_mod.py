from kmk.keys import make_argumented_key
from kmk.modules import Module


class StickyModMeta:
    def __init__(self, kc, mod):
        self.kc = kc
        self.mod = mod


class StickyMod(Module):
    def __init__(self):
        self._active = False
        self._active_key = None
        make_argumented_key(
            names=('SM',),
            validator=StickyModMeta,
            on_press=self.sm_pressed,
            on_release=self.sm_released,
        )

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        # release previous key if any other key is pressed
        if self._active and self._active_key is not None:
            self.release_key(keyboard, self._active_key)

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

    def release_key(self, keyboard, key):
        keyboard.process_key(key.meta.mod, False)
        self._active = False
        self._active_key = None

    def sm_pressed(self, key, keyboard, *args, **kwargs):
        keyboard.process_key(key.meta.mod, True)
        keyboard.process_key(key.meta.kc, True)
        self._active_key = key

    def sm_released(self, key, keyboard, *args, **kwargs):
        keyboard.process_key(key.meta.kc, False)
        self._active_key = key
        self._active = True
