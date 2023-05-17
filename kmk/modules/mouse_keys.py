from micropython import const

from kmk.keys import AX, make_key, make_mouse_key
from kmk.modules import Module
from kmk.scheduler import cancel_task, create_task

_MU = const(1)
_MD = const(2)
_ML = const(4)
_MR = const(8)
_WU = const(16)
_WD = const(32)
_WL = const(64)
_WR = const(128)


class MouseKeys(Module):
    def __init__(self):
        self._movement = 0
        self.max_speed = 10
        self.acc_interval = 20  # Delta ms to apply acceleration
        self.move_step = 1

        make_mouse_key(
            names=('MB_LMB',),
            code=1,
        )
        make_mouse_key(
            names=('MB_MMB',),
            code=4,
        )
        make_mouse_key(
            names=('MB_RMB',),
            code=2,
        )
        make_mouse_key(
            names=('MB_BTN4',),
            code=8,
        )
        make_mouse_key(
            names=('MB_BTN5',),
            code=16,
        )
        make_key(
            names=('MW_UP',),
            on_press=self._mw_up_press,
            on_release=self._mw_up_release,
        )
        make_key(
            names=(
                'MW_DOWN',
                'MW_DN',
            ),
            on_press=self._mw_down_press,
            on_release=self._mw_down_release,
        )
        make_key(
            names=('MW_LEFT', 'MW_LT'),
            on_press=self._mw_left_press,
            on_release=self._mw_left_release,
        )
        make_key(
            names=('MW_RIGHT', 'MW_RT'),
            on_press=self._mw_right_press,
            on_release=self._mw_right_release,
        )
        make_key(
            names=('MS_UP',),
            on_press=self._ms_up_press,
            on_release=self._ms_up_release,
        )
        make_key(
            names=(
                'MS_DOWN',
                'MS_DN',
            ),
            on_press=self._ms_down_press,
            on_release=self._ms_down_release,
        )
        make_key(
            names=(
                'MS_LEFT',
                'MS_LT',
            ),
            on_press=self._ms_left_press,
            on_release=self._ms_left_release,
        )
        make_key(
            names=(
                'MS_RIGHT',
                'MS_RT',
            ),
            on_press=self._ms_right_press,
            on_release=self._ms_right_release,
        )

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
