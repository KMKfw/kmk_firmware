from kmk.keys import KC
from kmk.modules import Module
from kmk.scheduler import create_task
from kmk.utils import Debug

debug = Debug(__name__)


def noop(*args):
    pass


class AnalogEvent:
    def __init__(self, on_change=noop, on_stop=noop):
        self._on_change = on_change
        self._on_stop = on_stop

    def on_change(self, event, keyboard):
        self._on_change(self, event, keyboard)

    def on_stop(self, event, keyboard):
        self._on_stop(self, event, keyboard)


class AnalogKey(AnalogEvent):
    def __init__(self, key, threshold=127):
        self.key = key
        self.threshold = threshold
        self.pressed = False

    def on_change(self, event, keyboard):
        if event.value >= self.threshold and not self.pressed:
            self.pressed = True
            keyboard.pre_process_key(self.key, True)

        elif event.value < self.threshold and self.pressed:
            self.pressed = False
            keyboard.pre_process_key(self.key, False)

    def on_stop(self, event, keyboard):
        pass


class AnalogInput:
    def __init__(self, input, filter=lambda input: input.value >> 8):
        self.input = input
        self.value = 0
        self.delta = 0
        self.filter = filter

    def update(self):
        '''
        Read a new value from an analogio compatible input, apply
        transformation, then return either the new value if it changed or `None`
        otherwise.
        '''
        value = self.filter(self.input)
        self.delta = value - self.value
        if self.delta != 0:
            self.value = value
            return value


class AnalogInputs(Module):
    def __init__(self, inputs, evtmap, update_interval=10):
        self._active = {}
        self.inputs = inputs
        self.evtmap = evtmap
        self.update_interval = update_interval

    def during_bootup(self, keyboard):
        self.task = create_task(
            lambda: self.update(keyboard),
            period_ms=self.update_interval,
        )

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

    def update(self, keyboard):
        for idx, input in enumerate(self.inputs):
            value = input.update()

            # No change in value: stop or pass
            if value is None:
                if idx in self._active:
                    if debug.enabled:
                        debug('on_stop', input, self._active[idx])
                    self._active[idx].on_stop(input, keyboard)
                    del self._active[idx]
                continue

            # Resolve event handler
            if idx in self._active:
                key = self._active[idx]
            else:
                key = None
                for layer in keyboard.active_layers:
                    try:
                        key = self.evtmap[layer][idx]
                    except IndexError:
                        if debug.enabled:
                            debug('evtmap IndexError: idx=', idx, ' layer=', layer)
                    if key and key != KC.TRNS:
                        break

            if key == KC.NO:
                continue

            # Forward change to event handler
            try:
                self._active[idx] = key
                if debug.enabled:
                    debug('on_change', input, key, value)
                key.on_change(input, keyboard)
            except Exception as e:
                if debug.enabled:
                    debug(type(e), ': ', e, ' in ', key.on_change)
