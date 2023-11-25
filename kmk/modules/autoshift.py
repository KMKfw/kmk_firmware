from kmk.keys import KC, Key
from kmk.modules import Module
from kmk.scheduler import cancel_task, create_task
from kmk.utils import Debug

debug = Debug(__name__)


class Autoshift(Module):
    def __init__(self, tap_time=300):
        self.tap_time = tap_time

        self._active = False
        self._task = None
        self._key = None

    def during_bootup(self, keyboard):
        self._task = create_task(lambda: self._shift(keyboard), after_ms=-1)

    def before_matrix_scan(self, keyboard):
        pass

    def after_matrix_scan(self, keyboard):
        pass

    def process_key(self, keyboard, key, is_pressed, int_coord):
        # Unshift on any key event
        if self._active:
            self._unshift(keyboard)
            return key

        # Only shift from an unshifted state
        if keyboard._hid_helper.has_key(KC.LSHIFT):
            return key

        # Ignore rolls from tapped to hold
        if not is_pressed and key is not self._key:
            return key

        # Only shift alpha keys, iff there's no pending potential shift
        if (
            is_pressed
            and not self._key
            and isinstance(key, Key)
            and key.code
            and KC.A.code <= key.code <= KC.Z.code
        ):
            create_task(self._task, after_ms=self.tap_time)
            self._key = key
        else:
            cancel_task(self._task)
            keyboard.resume_process_key(self, self._key, True)
            if key is self._key:
                keyboard.resume_process_key(self, self._key, False)
            else:
                keyboard.resume_process_key(self, key, True)
            self._key = None

    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass

    def _shift(self, keyboard):
        if debug.enabled:
            debug('activate')
        self._active = True
        keyboard.keys_pressed.add(KC.LSFT)
        keyboard.resume_process_key(self, self._key, True)

    def _unshift(self, keyboard):
        if debug.enabled:
            debug('deactivate')
        self._active = False
        self._key = None
        keyboard.keys_pressed.remove(KC.LSFT)
