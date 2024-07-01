from micropython import const

from kmk.keys import AX, MouseKey, make_key
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


class MouseKeys(Module):
    def __init__(self, max_speed=10, acc_interval=20, move_step=1):
        self._movement = 0
        self.max_speed = max_speed
        self.acc_interval = acc_interval
        self.move_step = move_step

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
            (('MW_UP',), self._mw_up_press, self._mw_up_release),
            (('MW_DOWN', 'MW_DN'), self._mw_down_press, self._mw_down_release),
            (('MW_LEFT', 'MW_LT'), self._mw_left_press, self._mw_left_release),
            (('MW_RIGHT', 'MW_RT'), self._mw_right_press, self._mw_right_release),
            (('MS_UP',), self._ms_up_press, self._ms_up_release),
            (('MS_DOWN', 'MS_DN'), self._ms_down_press, self._ms_down_release),
            (('MS_LEFT', 'MS_LT'), self._ms_left_press, self._ms_left_release),
            (('MS_RIGHT', 'MS_RT'), self._ms_right_press, self._ms_right_release),
        )
        for names, on_press, on_release in keys:
            make_key(names=names, on_press=on_press, on_release=on_release)

    def during_bootup(self, keyboard):
        self._task = create_task(
            lambda: self._move(keyboard),
            period_ms=self.acc_interval,
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
        if self._movement & (_MR + _ML + _MD + _MU):
            if self.move_step < self.max_speed:
                self.move_step = self.move_step + 1
            if self._movement & _MU:
                AX.Y.move(keyboard, -self.move_step)
            if self._movement & _MD:
                AX.Y.move(keyboard, self.move_step)
            if self._movement & _ML:
                AX.X.move(keyboard, -self.move_step)
            if self._movement & _MR:
                AX.X.move(keyboard, self.move_step)

        if self._movement & _WU:
            AX.W.move(keyboard, 1)
        if self._movement & _WD:
            AX.W.move(keyboard, -1)
        if self._movement & _WL:
            AX.P.move(keyboard, -1)
        if self._movement & _WR:
            AX.P.move(keyboard, 1)

    def _maybe_start_move(self, mask):
        self._movement |= mask
        if self._movement == mask:
            self._task.restart()

    def _maybe_stop_move(self, mask):
        self._movement &= ~mask
        if not self._movement & (_MR + _ML + _MD + _MU):
            self.move_step = 1
        if not self._movement:
            cancel_task(self._task)

    def _mw_up_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_WU)

    def _mw_up_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_WU)

    def _mw_down_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_WD)

    def _mw_down_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_WD)

    def _mw_left_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_WL)

    def _mw_left_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_WL)

    def _mw_right_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_WR)

    def _mw_right_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_WR)

    def _ms_up_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_MU)

    def _ms_up_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_MU)

    def _ms_down_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_MD)

    def _ms_down_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_MD)

    def _ms_left_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_ML)

    def _ms_left_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_ML)

    def _ms_right_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_MR)

    def _ms_right_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_MR)
