from micropython import const

from kmk.keys import make_argumented_key
from kmk.modules import Module
from kmk.utils import Debug

debug = Debug(__name__)


_SK_IDLE = const(0)
_SK_PRESSED = const(1)
_SK_RELEASED = const(2)
_SK_HOLD = const(3)
_SK_STICKY = const(4)


class StickyKeyMeta:
    def __init__(self, key, defer_release=False):
        self.key = key
        self.defer_release = defer_release
        self.timeout = None
        self.state = _SK_IDLE


class StickyKeys(Module):
    def __init__(self, release_after=1000):
        self.active_keys = []
        self.release_after = release_after

        make_argumented_key(
            validator=StickyKeyMeta,
            names=('SK', 'STICKY'),
            on_press=self.on_press,
            on_release=self.on_release,
        )

    def during_bootup(self, keyboard):
        return

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

    def process_key(self, keyboard, current_key, is_pressed, int_coord):
        delay_current = False

        for key in self.active_keys.copy():
            # Ignore keys that will resolve to and emit a different key
            # eventually, potentially triggering twice.
            # Handle interactions among sticky keys (stacking) in `on_press`
            # instead of `process_key` to avoid race conditions / causal
            # reordering when resetting timeouts.
            if (
                isinstance(current_key.meta, StickyKeyMeta)
                or current_key.meta.__class__.__name__ == 'TapDanceKeyMeta'
                or current_key.meta.__class__.__name__ == 'HoldTapKeyMeta'
            ):
                continue

            meta = key.meta

            if meta.state == _SK_PRESSED and is_pressed:
                meta.state = _SK_HOLD
            elif meta.state == _SK_RELEASED and is_pressed:
                meta.state = _SK_STICKY
            elif meta.state == _SK_STICKY:
                # Defer sticky release until last other key is released.
                if meta.defer_release:
                    if not is_pressed and len(keyboard._coordkeys_pressed) <= 1:
                        self.deactivate(keyboard, key)
                # Release sticky key; if it's a new key pressed: delay
                # propagation until after the sticky release.
                else:
                    self.deactivate(keyboard, key)
                    delay_current = is_pressed

        if delay_current:
            keyboard.resume_process_key(self, current_key, is_pressed, int_coord, False)
        else:
            return current_key

    def set_timeout(self, keyboard, key):
        key.meta.timeout = keyboard.set_timeout(
            self.release_after,
            lambda: self.on_release_after(keyboard, key),
        )

    def on_press(self, key, keyboard, *args, **kwargs):
        # Let sticky keys stack by renewing timeouts.
        for sk in self.active_keys:
            keyboard.cancel_timeout(sk.meta.timeout)

        # Reset on repeated taps.
        if key.meta.state != _SK_IDLE:
            key.meta.state = _SK_PRESSED
        else:
            self.activate(keyboard, key)

        for sk in self.active_keys:
            self.set_timeout(keyboard, sk)

    def on_release(self, key, keyboard, *args, **kwargs):
        # No interrupt or timeout happend, mark key as RELEASED, ready to get
        # STICKY.
        if key.meta.state == _SK_PRESSED:
            key.meta.state = _SK_RELEASED
        # Key in HOLD state is handled like a regular release.
        elif key.meta.state == _SK_HOLD:
            for sk in self.active_keys.copy():
                keyboard.cancel_timeout(sk.meta.timeout)
                self.deactivate(keyboard, sk)

    def on_release_after(self, keyboard, key):
        # Key is still pressed but nothing else happend: set to HOLD.
        if key.meta.state == _SK_PRESSED:
            for sk in self.active_keys:
                key.meta.state = _SK_HOLD
                keyboard.cancel_timeout(sk.meta.timeout)
        # Key got released but nothing else happend: deactivate.
        elif key.meta.state == _SK_RELEASED:
            for sk in self.active_keys.copy():
                self.deactivate(keyboard, sk)

    def activate(self, keyboard, key):
        if debug.enabled:
            debug('activate')
        key.meta.state = _SK_PRESSED
        self.active_keys.insert(0, key)
        keyboard.resume_process_key(self, key.meta.key, True)

    def deactivate(self, keyboard, key):
        if debug.enabled:
            debug('deactivate')
        key.meta.state = _SK_IDLE
        self.active_keys.remove(key)
        keyboard.resume_process_key(self, key.meta.key, False)
