from micropython import const

from kmk.keys import KC, make_argumented_key, make_key
from kmk.modules import Module
from kmk.scheduler import create_task
from kmk.utils import Debug

debug = Debug(__name__)

_IDLE = const(0)
_ON_PRESS = const(1)
_ON_HOLD = const(2)
_RELEASE = const(3)
_ON_RELEASE = const(4)


class MacroMeta:
    def __init__(
        self,
        *args,
        on_press=None,
        on_hold=None,
        on_release=None,
        blocking=True,
    ):
        if on_press is not None:
            self.on_press = on_press
        else:
            self.on_press = args
        self.on_hold = on_hold
        self.on_release = on_release
        self.blocking = blocking
        self.state = _IDLE
        self._task = None


def Delay(delay):
    return lambda keyboard: delay


def Press(key):
    return lambda keyboard: key.on_press(keyboard)


def Release(key):
    return lambda keyboard: key.on_release(keyboard)


def Tap(key):
    def _(keyboard):
        key.on_press(keyboard)
        yield
        key.on_release(keyboard)

    return _


class UnicodeModeIBus:
    @staticmethod
    def pre(keyboard):
        macro = (KC.LCTL, KC.LSFT, KC.U)
        for k in macro:
            k.on_press(keyboard)
        yield
        for k in macro:
            k.on_release(keyboard)

    @staticmethod
    def post(keyboard):
        KC.ENTER.on_press(keyboard)
        yield
        KC.ENTER.on_release(keyboard)


class UnicodeModeMacOS:
    @staticmethod
    def pre(keyboard):
        KC.LALT.on_press(keyboard)
        yield

    @staticmethod
    def post(keyboard):
        KC.LALT.on_release(keyboard)
        yield


class UnicodeModeWinC:
    @staticmethod
    def pre(keyboard):
        macro = (KC.RALT, KC.U)
        for k in macro:
            k.on_press(keyboard)
        yield
        for k in macro:
            k.on_release(keyboard)

    @staticmethod
    def post(keyboard):
        KC.ENTER.on_press(keyboard)
        yield
        KC.ENTER.on_release(keyboard)


def MacroIter(keyboard, macro, unicode_mode):
    for item in macro:
        if callable(item):
            ret = item(keyboard)
            if ret.__class__.__name__ == 'generator':
                for _ in ret:
                    yield _
                yield
            else:
                yield ret

        elif isinstance(item, str):
            for char in item:
                if ord(char) <= 127:
                    # ANSII key codes
                    key = KC[char]
                    if char.isupper():
                        KC.LSHIFT.on_press(keyboard)
                    key.on_press(keyboard)
                    yield

                    if char.isupper():
                        KC.LSHIFT.on_release(keyboard)
                    key.on_release(keyboard)
                    yield

                else:
                    # unicode code points
                    for _ in unicode_mode.pre(keyboard):
                        yield _
                    yield

                    for digit in hex(ord(char))[2:]:
                        key = KC[digit]
                        key.on_press(keyboard)
                        yield
                        key.on_release(keyboard)
                        yield

                    for _ in unicode_mode.post(keyboard):
                        yield _
                    yield

        elif debug.enabled:
            debug('unsupported macro type', item.__class__.__name__)


class Macros(Module):
    def __init__(self, unicode_mode=UnicodeModeIBus, delay=10):
        self._active = []
        self.key_buffer = []
        self.unicode_mode = unicode_mode
        self.delay = delay

        make_argumented_key(
            validator=MacroMeta,
            names=('MACRO',),
            on_press=self.on_press_macro,
            on_release=self.on_release_macro,
        )
        make_key(
            names=('UC_MODE_IBUS',),
            meta=UnicodeModeIBus,
            on_press=self.on_press_unicode_mode,
        )
        make_key(
            names=('UC_MODE_MACOS',),
            meta=UnicodeModeMacOS,
            on_press=self.on_press_unicode_mode,
        )
        make_key(
            names=('UC_MODE_WINC',),
            meta=UnicodeModeWinC,
            on_press=self.on_press_unicode_mode,
        )

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not self._active or key in self._active:
            return key

        self.key_buffer.append((int_coord, key, is_pressed))

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def on_press_unicode_mode(self, key, keyboard, *args, **kwargs):
        self.unicode_mode = key.meta

    def on_press_macro(self, key, keyboard, *args, **kwargs):
        key.meta.state = _ON_PRESS
        self.process_macro_async(keyboard, key)

    def on_release_macro(self, key, keyboard, *args, **kwargs):
        key.meta.state = _RELEASE
        if key.meta._task is None:
            self.process_macro_async(keyboard, key)

    def process_macro_async(self, keyboard, key, _iter=None):
        # There's no active macro iterator: select the next one.
        if _iter is None:
            key.meta._task = None

            if key.meta.state == _ON_PRESS:
                if key.meta.blocking:
                    self._active.append(key)
                if (macro := key.meta.on_press) is None:
                    key.meta.state = _ON_HOLD
                elif debug.enabled:
                    debug('on_press')

            if key.meta.state == _ON_HOLD:
                if (macro := key.meta.on_hold) is None:
                    return
                elif debug.enabled:
                    debug('on_hold')

            if key.meta.state == _RELEASE:
                key.meta.state = _ON_RELEASE

            if key.meta.state == _ON_RELEASE:
                if (macro := key.meta.on_release) is None:
                    macro = ()
                elif debug.enabled:
                    debug('on_release')

            _iter = MacroIter(keyboard, macro, self.unicode_mode)

        # Run one step in the macro sequence.
        delay = self.delay
        try:
            # any not None value the iterator yields is a delay value in ms.
            ret = next(_iter)
            if ret is not None:
                delay = ret
            keyboard._send_hid()

        # The sequence has reached its end: advance the macro state.
        except StopIteration:
            _iter = None
            delay = 0
            key.meta._task = None

            if key.meta.state == _ON_PRESS:
                key.meta.state = _ON_HOLD

            elif key.meta.state == _ON_RELEASE:
                if debug.enabled:
                    debug('deactivate')
                key.meta.state = _IDLE
                if key.meta.blocking:
                    self._active.remove(key)
                self.send_key_buffer(keyboard)
                return

        # Schedule the next step.
        # Reuse existing task objects and save a couple of bytes and cycles for the gc.
        if key.meta._task:
            task = key.meta._task
        else:

            def task():
                self.process_macro_async(keyboard, key, _iter)

        key.meta._task = create_task(task, after_ms=delay)

    def send_key_buffer(self, keyboard):
        if not self.key_buffer or self._active:
            return

        for int_coord, key, is_pressed in self.key_buffer:
            keyboard.resume_process_key(self, key, is_pressed, int_coord, False)

        self.key_buffer.clear()
