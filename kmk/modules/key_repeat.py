from kmk.keys import KC, make_key
from kmk.modules import Module


class KeyRepeat(Module):
    def __init__(self):
        make_key(
            names=('REP',),
            on_press=self.on_press,
            on_release=self.on_release,
        )
        self.repeat_key = KC.NO

    def on_press(self, key, keyboard, *args, **kwargs):
        self.repeat_key.on_press(keyboard)

    def on_release(self, key, keyboard, *args, **kwargs):
        self.repeat_key.on_release(keyboard)

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not key == KC.REP and is_pressed:
            self.repeat_key = key

        return key

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return
