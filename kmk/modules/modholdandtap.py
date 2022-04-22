from kmk.keys import make_argumented_key
from kmk.modules import Module


class ModHoldAndTapValidator:
    def __init__(self, kc, mod):
        self.kc = kc
        self.mod = mod


class ModHoldAndTap(Module):
    def __init__(self):
        self._timeout_key = False
        self._active = False
        self._prev_key = None
        make_argumented_key(
            names=('MHAT',),
            validator=ModHoldAndTapValidator,
        )

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if isinstance(key.meta, ModHoldAndTapValidator):

            layer_id = keyboard.active_layers[0]
            if layer_id > 0:
                if self._active and self._prev_key is not None and is_pressed:
                    # release previous key
                    self.release(keyboard, self._prev_key)
                self._prev_key = key
                if is_pressed:
                    keyboard.process_key(key.meta.mod, is_pressed)

                    self._active = True
                keyboard.process_key(key.meta.kc, is_pressed)

        elif self._active:
            # release previous key if any other key is pressed
            if self._prev_key is not None:
                self.release(keyboard, self._prev_key)

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

    def release(self, keyboard, key):
        keyboard.process_key(key.meta.mod, False)
        self._active = False
        self._prev_key = None
