from micropython import const

from kmk.keys import AX, Key, MouseKey, make_key
from kmk.modules import Module
from kmk.scheduler import cancel_task, create_task

_MU = const(0x01)
_MD = const(0x02)
_ML = const(0x04)
_MR = const(0x08)
_WU = const(0x10)
_WD = const(0x20)
_WL = const(0x40)
_WR = const(0x80)


class MouseDirectionKey(Key):
    def __init__(self, code, **kwargs):
        super().__init__(**kwargs)
        self.code = code

    def __repr__(self):
        return super().__repr__() + f'(code=0x{self.code:02X})'


class MouseKeys(Module):
    def __init__(
        self,
        max_speed=10,
        timestep_ms=(20, 200),
        # The below arguments are for backwards compatibility. They can be
        # removed at some point in the future(TM).
        acc_interval=None,
        move_step=None,
    ):
        self.max_speed = max_speed
        self.timestep_ms = [timestep_ms[0], timestep_ms[1]]
        if acc_interval:
            self.timestep_ms[:] = (acc_interval,) * 2

        self._mouse_movement = 0
        self._wheel_movement = 0
        self._move_step = 0

        codes = (
            (0x01, ('MB_LMB',)),
            (0x02, ('MB_RMB',)),
            (0x04, ('MB_MMB',)),
            (0x08, ('MB_BTN4',)),
            (0x10, ('MB_BTN5',)),
        )
        for code, names in codes:
            make_key(names=names, constructor=MouseKey, code=code)

        keys = (
            ('MS_UP',),
            ('MS_DOWN', 'MS_DN'),
            ('MS_LEFT', 'MS_LT'),
            ('MS_RIGHT', 'MS_RT'),
        )
        for n, names in enumerate(keys):
            make_key(
                names=names,
                constructor=MouseDirectionKey,
                on_press=self._mouse_press,
                on_release=self._mouse_release,
                code=1 << n,
            )

        keys = (
            ('MW_UP',),
            ('MW_DOWN', 'MW_DN'),
            ('MW_LEFT', 'MW_LT'),
            ('MW_RIGHT', 'MW_RT'),
        )
        for n, names in enumerate(keys):
            make_key(
                names=names,
                constructor=MouseDirectionKey,
                on_press=self._wheel_press,
                on_release=self._wheel_release,
                code=1 << (n + 4),
            )

    def during_bootup(self, keyboard):
        self._mouse_task = create_task(
            lambda: self._move_mouse(keyboard),
            period_ms=self.timestep_ms[0],
        )
        cancel_task(self._mouse_task)

        self._wheel_task = create_task(
            lambda: self._move_wheel(keyboard),
            period_ms=self.timestep_ms[1],
        )
        cancel_task(self._wheel_task)

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

    def _move_mouse(self, keyboard):
        if self._move_step < self.max_speed:
            self._move_step += 1
        if self._mouse_movement & _MU:
            AX.Y.move(keyboard, -self._move_step)
        if self._mouse_movement & _MD:
            AX.Y.move(keyboard, self._move_step)
        if self._mouse_movement & _ML:
            AX.X.move(keyboard, -self._move_step)
        if self._mouse_movement & _MR:
            AX.X.move(keyboard, self._move_step)

    def _maybe_start_move_mouse(self, mask):
        self._mouse_movement |= mask
        if self._mouse_movement == mask:
            self._mouse_task.restart()

    def _maybe_stop_move_mouse(self, mask):
        self._mouse_movement &= ~mask
        if not self._mouse_movement:
            self._move_step = 0
            cancel_task(self._mouse_task)

    def _move_wheel(self, keyboard):
        if self._wheel_movement & _WU:
            AX.W.move(keyboard, 1)
        if self._wheel_movement & _WD:
            AX.W.move(keyboard, -1)
        if self._wheel_movement & _WL:
            AX.P.move(keyboard, -1)
        if self._wheel_movement & _WR:
            AX.P.move(keyboard, 1)

    def _maybe_start_move_wheel(self, mask):
        self._wheel_movement |= mask
        if self._wheel_movement == mask:
            self._wheel_task.restart()

    def _maybe_stop_move_wheel(self, mask):
        self._wheel_movement &= ~mask
        if not self._wheel_movement:
            cancel_task(self._wheel_task)

    def _mouse_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move_mouse(key.code)

    def _mouse_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move_mouse(key.code)

    def _wheel_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move_wheel(key.code)

    def _wheel_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move_wheel(key.code)
