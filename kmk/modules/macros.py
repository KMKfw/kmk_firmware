from micropython import const

from kmk.keys import KC, Key, make_argumented_key, make_key
from kmk.modules import Module
from kmk.scheduler import create_task
from kmk.utils import Debug

debug = Debug(__name__)

_IDLE = const(0)
_ON_PRESS = const(1)
_ON_HOLD = const(2)
_RELEASE = const(3)
_ON_RELEASE = const(4)


class MacroKey(Key):
    def __init__(
        self,
        *args,
        on_press=None,
        on_hold=None,
        on_release=None,
        blocking=True,
        _on_press=None,
        _on_release=None,
    ):
        super().__init__(on_press=_on_press, on_release=_on_release)

        if on_press is not None:
            self.on_press_macro = on_press
        else:
            self.on_press_macro = args
        self.on_hold_macro = on_hold
        self.on_release_macro = on_release
        self.blocking = blocking
        self.state = _IDLE
        self._task = None


class UnicodeModeKey(Key):
    def __init__(self, mode, **kwargs):
        super().__init__(**kwargs)
        self.mode = mode


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
            item = item(keyboard)

        if item is None:
            yield

        elif isinstance(item, int):
            yield item

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
                    yield from unicode_mode.pre(keyboard)
                    yield

                    for digit in hex(ord(char))[2:]:
                        key = KC[digit]
                        key.on_press(keyboard)
                        yield
                        key.on_release(keyboard)
                        yield

                    yield from unicode_mode.post(keyboard)
                    yield

        elif item.__class__.__name__ == 'generator':
            yield from MacroIter(keyboard, item, unicode_mode)
            yield

        elif debug.enabled:
            debug('unsupported macro type ', item.__class__.__name__)


class Macros(Module):
    def __init__(self, unicode_mode=UnicodeModeIBus, delay=10):
        self._active = []
        self.key_buffer = []
        self.unicode_mode = unicode_mode
        self.delay = delay

        make_argumented_key(
            names=('MACRO',),
            constructor=MacroKey,
            _on_press=self.on_press_macro,
            _on_release=self.on_release_macro,
        )
        make_key(
            names=('UC_MODE_IBUS',),
            constructor=UnicodeModeKey,
            mode=UnicodeModeIBus,
            on_press=self.on_press_unicode_mode,
        )
        make_key(
            names=('UC_MODE_MACOS',),
            constructor=UnicodeModeKey,
            mode=UnicodeModeMacOS,
            on_press=self.on_press_unicode_mode,
        )
        make_key(
            names=('UC_MODE_WINC',),
            constructor=UnicodeModeKey,
            mode=UnicodeModeWinC,
            on_press=self.on_press_unicode_mode,
        )

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        # Passthrough if there are no active macros, or the key belongs to an
        # active macro, or all active macros or non-blocking.
        if not self._active or key in self._active or not self._active[-1].blocking:
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
        self.unicode_mode = key.mode

    def on_press_macro(self, key, keyboard, *args, **kwargs):
        if key.state == _IDLE:
            key.state = _ON_PRESS
            self.process_macro_async(keyboard, key)
        else:
            self.key_buffer.append((args[1], key, True))

    def on_release_macro(self, key, keyboard, *args, **kwargs):
        if key.state == _ON_PRESS or key.state == _ON_HOLD:
            key.state = _RELEASE
            if key._task is None:
                self.process_macro_async(keyboard, key)
        else:
            self.key_buffer.append((args[1], key, False))

    def process_macro_async(self, keyboard, key, _iter=None):
        # There's no active macro iterator: select the next one.
        if _iter is None:
            key._task = None

            if key.state == _ON_PRESS:
                self._active.append(key)
                if (macro := key.on_press_macro) is None:
                    key.state = _ON_HOLD
                elif debug.enabled:
                    debug('on_press')

            if key.state == _ON_HOLD:
                if (macro := key.on_hold_macro) is None:
                    return
                elif debug.enabled:
                    debug('on_hold')

            if key.state == _RELEASE:
                key.state = _ON_RELEASE

            if key.state == _ON_RELEASE:
                if (macro := key.on_release_macro) is None:
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
            key._task = None

            if key.state == _ON_PRESS:
                key.state = _ON_HOLD

            elif key.state == _ON_RELEASE:
                if debug.enabled:
                    debug('deactivate')
                key.state = _IDLE
                self._active.remove(key)
                self.send_key_buffer(keyboard)
                return

        # Schedule the next step.
        # Reuse existing task objects and save a couple of bytes and cycles for the gc.
        if key._task:
            task = key._task
        else:

            def task():
                self.process_macro_async(keyboard, key, _iter)

        key._task = create_task(task, after_ms=delay)

    def send_key_buffer(self, keyboard):
        if not self.key_buffer or self._active:
            return

        for int_coord, key, is_pressed in self.key_buffer:
            keyboard.resume_process_key(self, key, is_pressed, int_coord, False)

        self.key_buffer.clear()
