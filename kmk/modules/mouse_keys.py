from kmk.keys import AX, make_key, make_mouse_key
from kmk.kmktime import PeriodicTimer
from kmk.modules import Module


class MouseKeys(Module):
    def __init__(self):
        self._nav_key_activated = 0
        self._up_activated = False
        self._down_activated = False
        self._left_activated = False
        self._right_activated = False
        self._mw_up_activated = False
        self._mw_down_activated = False
        self.max_speed = 10
        self.acc_interval = 10  # Delta ms to apply acceleration
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
        self._timer = PeriodicTimer(self.acc_interval)

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        if not self._timer.tick():
            return

        if self._nav_key_activated:
            if self.move_step < self.max_speed:
                self.move_step = self.move_step + 1
            if self._right_activated:
                AX.X.move(keyboard, self.move_step)
            if self._left_activated:
                AX.X.move(keyboard, -self.move_step)
            if self._up_activated:
                AX.Y.move(keyboard, -self.move_step)
            if self._down_activated:
                AX.Y.move(keyboard, self.move_step)

        if self._mw_up_activated:
            AX.W.move(keyboard, 1)
        if self._mw_down_activated:
            AX.W.move(keyboard, -1)

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def _mw_up_press(self, key, keyboard, *args, **kwargs):
        self._mw_up_activated = True

    def _mw_up_release(self, key, keyboard, *args, **kwargs):
        self._mw_up_activated = False

    def _mw_down_press(self, key, keyboard, *args, **kwargs):
        self._mw_down_activated = True

    def _mw_down_release(self, key, keyboard, *args, **kwargs):
        self._mw_down_activated = False

    # Mouse movement
    def _reset_next_interval(self):
        if self._nav_key_activated == 1:
            self.move_step = 1

    def _check_last(self):
        if self._nav_key_activated == 0:
            self.move_step = 1

    def _ms_up_press(self, key, keyboard, *args, **kwargs):
        self._nav_key_activated += 1
        self._reset_next_interval()
        self._up_activated = True

    def _ms_up_release(self, key, keyboard, *args, **kwargs):
        self._up_activated = False
        self._nav_key_activated -= 1
        self._check_last()

    def _ms_down_press(self, key, keyboard, *args, **kwargs):
        self._nav_key_activated += 1
        self._reset_next_interval()
        self._down_activated = True

    def _ms_down_release(self, key, keyboard, *args, **kwargs):
        self._down_activated = False
        self._nav_key_activated -= 1
        self._check_last()

    def _ms_left_press(self, key, keyboard, *args, **kwargs):
        self._nav_key_activated += 1
        self._reset_next_interval()
        self._left_activated = True

    def _ms_left_release(self, key, keyboard, *args, **kwargs):
        self._nav_key_activated -= 1
        self._left_activated = False
        self._check_last()

    def _ms_right_press(self, key, keyboard, *args, **kwargs):
        self._nav_key_activated += 1
        self._reset_next_interval()
        self._right_activated = True

    def _ms_right_release(self, key, keyboard, *args, **kwargs):
        self._nav_key_activated -= 1
        self._right_activated = False
        self._check_last()
