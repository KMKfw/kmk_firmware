from micropython import const

from kmk.keys import SM, SpacemouseKey, make_key
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


class SpacemouseKeys(Module):
    def __init__(self, max_speed=450, accel=5, timestep_ms=10):
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
            (('SM_XI', 'SM_X_INCREASE'), self._xi_press, self._xi_release),
            (('SM_YI', 'SM_Y_INCREASE'), self._yi_press, self._yi_release),
            (('SM_ZI', 'SM_Z_INCREASE'), self._zi_press, self._zi_release),
            (('SM_AI', 'SM_A_INCREASE'), self._ai_press, self._ai_release),
            (('SM_BI', 'SM_B_INCREASE'), self._bi_press, self._bi_release),
            (('SM_CI', 'SM_C_INCREASE'), self._ci_press, self._ci_release),
            (('SM_XD', 'SM_X_DECREASE'), self._xd_press, self._xd_release),
            (('SM_YD', 'SM_Y_DECREASE'), self._yd_press, self._yd_release),
            (('SM_ZD', 'SM_Z_DECREASE'), self._zd_press, self._zd_release),
            (('SM_AD', 'SM_A_DECREASE'), self._ad_press, self._ad_release),
            (('SM_BD', 'SM_B_DECREASE'), self._bd_press, self._bd_release),
            (('SM_CD', 'SM_C_DECREASE'), self._cd_press, self._cd_release),
        )
        for names, on_press, on_release in keys:
            make_key(names=names, on_press=on_press, on_release=on_release)

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
        if self._movement & (
            _XI + _YI + _ZI + _AI + _BI + _CI + _XD + _YD + _ZD + _AD + _BD + _CD
        ):
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

    def _maybe_start_move(self, mask):
        self._movement |= mask
        if self._movement == mask:
            self._task.restart()

    def _maybe_stop_move(self, mask):
        self._movement &= ~mask
        if not self._movement & (
            _XI + _YI + _ZI + _AI + _BI + _CI + _XD + _YD + _ZD + _AD + _BD + _CD
        ):
            self._move_step = 0
        if not self._movement:
            cancel_task(self._task)

    def _xi_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_XI)

    def _xi_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_XI)

    def _yi_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_YI)

    def _yi_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_YI)

    def _zi_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_ZI)

    def _zi_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_ZI)

    def _ai_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_AI)

    def _ai_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_AI)

    def _bi_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_BI)

    def _bi_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_BI)

    def _ci_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_CI)

    def _ci_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_CI)

    def _xd_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_XD)

    def _xd_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_XD)

    def _yd_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_YD)

    def _yd_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_YD)

    def _zd_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_ZD)

    def _zd_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_ZD)

    def _ad_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_AD)

    def _ad_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_AD)

    def _bd_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_BD)

    def _bd_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_BD)

    def _cd_press(self, key, keyboard, *args, **kwargs):
        self._maybe_start_move(_CD)

    def _cd_release(self, key, keyboard, *args, **kwargs):
        self._maybe_stop_move(_CD)
