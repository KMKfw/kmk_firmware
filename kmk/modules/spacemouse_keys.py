from micropython import const

from kmk.keys import SM, Key, SpacemouseKey, make_key
from kmk.modules import Module
from kmk.scheduler import cancel_task, create_task

_XI = const(0x001)
_YI = const(0x002)
_ZI = const(0x004)
_AI = const(0x008)
_BI = const(0x010)
_CI = const(0x020)
_XD = const(0x040)
_YD = const(0x080)
_ZD = const(0x100)
_AD = const(0x200)
_BD = const(0x400)
_CD = const(0x800)


class SpacemouseDirectionKey(Key):
    def __init__(self, code, **kwargs):
        super().__init__(**kwargs)
        self.code = code

    def __repr__(self):
        return super().__repr__() + f'(code=0x{self.code:03X})'


class SpacemouseKeys(Module):
    def __init__(self, max_speed=450, accel=10, timestep_ms=15):
        self.max_speed = max_speed
        self.accel = accel
        self.timestep_ms = timestep_ms
        self._movement = 0
        self._move_step = 0

        codes = (
            (0x01, ('SM_LB', 'SM_LEFT')),
            (0x02, ('SM_RB', 'SM_RIGHT')),
        )
        for code, names in codes:
            make_key(names=names, constructor=SpacemouseKey, code=code)

        keys = (
            ('SM_XI', 'SM_X_INCREASE'),
            ('SM_YI', 'SM_Y_INCREASE'),
            ('SM_ZI', 'SM_Z_INCREASE'),
            ('SM_AI', 'SM_A_INCREASE'),
            ('SM_BI', 'SM_B_INCREASE'),
            ('SM_CI', 'SM_C_INCREASE'),
            ('SM_XD', 'SM_X_DECREASE'),
            ('SM_YD', 'SM_Y_DECREASE'),
            ('SM_ZD', 'SM_Z_DECREASE'),
            ('SM_AD', 'SM_A_DECREASE'),
            ('SM_BD', 'SM_B_DECREASE'),
            ('SM_CD', 'SM_C_DECREASE'),
        )
        for n, names in enumerate(keys):
            make_key(
                names=names,
                constructor=SpacemouseDirectionKey,
                on_press=self._on_press,
                on_release=self._on_release,
                code=1 << n,
            )

    def during_bootup(self, keyboard):
        self._task = create_task(
            lambda: self._move(keyboard),
            period_ms=self.timestep_ms,
        )
        cancel_task(self._task)

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

    def _move(self, keyboard):
        if self._movement:
            if self._move_step < self.max_speed:
                self._move_step = min(self._move_step + self.accel, self.max_speed)
            if self._movement & _XI:
                SM.X.move(keyboard, self._move_step)
            if self._movement & _YI:
                SM.Y.move(keyboard, self._move_step)
            if self._movement & _ZI:
                SM.Z.move(keyboard, self._move_step)
            if self._movement & _AI:
                SM.A.move(keyboard, self._move_step)
            if self._movement & _BI:
                SM.B.move(keyboard, self._move_step)
            if self._movement & _CI:
                SM.C.move(keyboard, self._move_step)
            if self._movement & _XD:
                SM.X.move(keyboard, -self._move_step)
            if self._movement & _YD:
                SM.Y.move(keyboard, -self._move_step)
            if self._movement & _ZD:
                SM.Z.move(keyboard, -self._move_step)
            if self._movement & _AD:
                SM.A.move(keyboard, -self._move_step)
            if self._movement & _BD:
                SM.B.move(keyboard, -self._move_step)
            if self._movement & _CD:
                SM.C.move(keyboard, -self._move_step)

    def _on_press(self, key, keyboard, *args, **kwargs):
        self._movement |= key.code
        if self._movement == key.code:
            self._task.restart()

    def _on_release(self, key, keyboard, *args, **kwargs):
        self._movement &= ~key.mask
        if not self._movement:
            cancel_task(self._task)
            self._move_step = 0
