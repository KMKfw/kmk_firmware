import random

from kmk.keys import AX, make_key
from kmk.modules import Module
from kmk.scheduler import cancel_task, create_task
from kmk.utils import Debug

debug = Debug(__name__)


class MouseJiggler(Module):
    def __init__(self, period_ms=5000, move_step=1):
        self.move_step = move_step
        self.period_ms = period_ms
        self._is_jiggling = False

        make_key(names=('MJ_TOGGLE',), on_press=self.toggle)
        make_key(names=('MJ_START',), on_press=self.start)
        make_key(names=('MJ_STOP',), on_press=self.stop)

    def during_bootup(self, keyboard):
        self._task = create_task(
            lambda: self._jiggle(keyboard),
            after_ms=-1,  # Don't start jiggling yet.
            period_ms=self.period_ms,
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

    def start(self, *args, **kwargs):
        if not self._is_jiggling:
            self._task.restart()
            self._is_jiggling = True
            if debug.enabled:
                debug('MouseJiggler started.')

    def stop(self, *args, **kwargs):
        if self._is_jiggling:
            cancel_task(self._task)
            self._is_jiggling = False
            if debug.enabled:
                debug('MouseJiggler stopped.')

    def toggle(self, *args, **kwargs):
        if self._is_jiggling:
            self.stop(*args, **kwargs)
        else:
            self.start(*args, **kwargs)

    @property
    def is_jiggling(self):
        return self._is_jiggling

    def _jiggle(self, keyboard):
        if debug.enabled:
            debug('MouseJiggler jiggling.')
        AX.X.move(keyboard, random.choice([-1, 1]) * self.move_step)
        AX.Y.move(keyboard, random.choice([-1, 1]) * self.move_step)
