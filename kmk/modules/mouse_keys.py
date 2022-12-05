from supervisor import ticks_ms

from kmk.hid import HID_REPORT_SIZES, HIDReportTypes
from kmk.keys import KC, make_key
from kmk.modules import Module


class PointingDevice:
    MB_LMB = 1
    MB_RMB = 2
    MB_MMB = 4
    _evt = bytearray(HID_REPORT_SIZES[HIDReportTypes.MOUSE] + 1)

    def __init__(self):
        self.key_states = {}
        self.hid_pending = False
        self.report_device = memoryview(self._evt)[0:1]
        self.report_device[0] = HIDReportTypes.MOUSE
        self.button_status = memoryview(self._evt)[1:2]
        self.report_x = memoryview(self._evt)[2:3]
        self.report_y = memoryview(self._evt)[3:4]
        self.report_w = memoryview(self._evt)[4:]


class MouseKeys(Module):
    def __init__(self):
        self.pointing_device = PointingDevice()
        self._nav_key_activated = 0
        self._up_activated = False
        self._down_activated = False
        self._left_activated = False
        self._right_activated = False
        self.max_speed = 10
        self.ac_interval = 100  # Delta ms to apply acceleration
        self._next_interval = 0  # Time for next tick interval
        self.move_step = 1
        KC._generators.append(self.maybe_make_mouse_key())

    def maybe_make_mouse_key(self):
        keys = (
            (('MB_LMB',), self._mb_lmb_press, self._mb_lmb_release),
            (('MB_MMB',), self._mb_mmb_press, self._mb_mmb_release),
            (('MB_RMB',), self._mb_rmb_press, self._mb_rmb_release),
            (('MW_UP',), self._mw_up_press, self._mw_up_release),
            (('MW_DOWN', 'MW_DN'), self._mw_down_press, self._mw_down_release),
            (('MS_UP',), self._ms_up_press, self._ms_up_release),
            (('MS_DOWN', 'MS_DN'), self._ms_down_press, self._ms_down_release),
            (('MS_LEFT', 'MS_LT'), self._ms_left_press, self._ms_left_release),
            (('MS_RIGHT', 'MS_RT'), self._ms_right_press, self._ms_right_release),
        )

        def closure(candidate):
            for names, on_press, on_release in keys:
                if candidate in names:
                    return make_key(
                        names=names, on_press=on_press, on_release=on_release
                    )

        return closure

    def during_bootup(self, keyboard):
        return

    def matrix_detected_press(self, keyboard):
        return keyboard.matrix_update is None

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        if self._nav_key_activated:
            if self._next_interval <= ticks_ms():
                # print("hello: ")
                # print(ticks_ms())
                self._next_interval = ticks_ms() + self.ac_interval
                # print(self._next_interval)
                if self.move_step < self.max_speed:
                    self.move_step = self.move_step + 1
            if self._right_activated:
                self.pointing_device.report_x[0] = self.move_step
            if self._left_activated:
                self.pointing_device.report_x[0] = 0xFF & (0 - self.move_step)
            if self._up_activated:
                self.pointing_device.report_y[0] = 0xFF & (0 - self.move_step)
            if self._down_activated:
                self.pointing_device.report_y[0] = self.move_step
            self.pointing_device.hid_pending = True
        return

    def before_hid_send(self, keyboard):
        if self.pointing_device.hid_pending and keyboard._hid_send_enabled:
            keyboard._hid_helper.hid_send(self.pointing_device._evt)
            self.pointing_device.hid_pending = False
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def _mb_lmb_press(self, key, keyboard, *args, **kwargs):
        self.pointing_device.button_status[0] |= self.pointing_device.MB_LMB
        self.pointing_device.hid_pending = True

    def _mb_lmb_release(self, key, keyboard, *args, **kwargs):
        self.pointing_device.button_status[0] &= ~self.pointing_device.MB_LMB
        self.pointing_device.hid_pending = True

    def _mb_mmb_press(self, key, keyboard, *args, **kwargs):
        self.pointing_device.button_status[0] |= self.pointing_device.MB_MMB
        self.pointing_device.hid_pending = True

    def _mb_mmb_release(self, key, keyboard, *args, **kwargs):
        self.pointing_device.button_status[0] &= ~self.pointing_device.MB_MMB
        self.pointing_device.hid_pending = True

    def _mb_rmb_press(self, key, keyboard, *args, **kwargs):
        self.pointing_device.button_status[0] |= self.pointing_device.MB_RMB
        self.pointing_device.hid_pending = True

    def _mb_rmb_release(self, key, keyboard, *args, **kwargs):
        self.pointing_device.button_status[0] &= ~self.pointing_device.MB_RMB
        self.pointing_device.hid_pending = True

    def _mw_up_press(self, key, keyboard, *args, **kwargs):
        self.pointing_device.report_w[0] = self.move_step
        self.pointing_device.hid_pending = True

    def _mw_up_release(self, key, keyboard, *args, **kwargs):
        self.pointing_device.report_w[0] = 0
        self.pointing_device.hid_pending = True

    def _mw_down_press(self, key, keyboard, *args, **kwargs):
        self.pointing_device.report_w[0] = 0xFF
        self.pointing_device.hid_pending = True

    def _mw_down_release(self, key, keyboard, *args, **kwargs):
        self.pointing_device.report_w[0] = 0
        self.pointing_device.hid_pending = True

    # Mouse movement
    def _reset_next_interval(self):
        if self._nav_key_activated == 1:
            self._next_interval = ticks_ms() + self.ac_interval
            self.move_step = 1

    def _check_last(self):
        if self._nav_key_activated == 0:
            self.move_step = 1

    def _ms_up_press(self, key, keyboard, *args, **kwargs):
        self._nav_key_activated += 1
        self._reset_next_interval()
        self._up_activated = True
        self.pointing_device.report_y[0] = 0xFF & (0 - self.move_step)
        self.pointing_device.hid_pending = True

    def _ms_up_release(self, key, keyboard, *args, **kwargs):
        self._up_activated = False
        self._nav_key_activated -= 1
        self._check_last()
        self.pointing_device.report_y[0] = 0
        self.pointing_device.hid_pending = False

    def _ms_down_press(self, key, keyboard, *args, **kwargs):
        self._nav_key_activated += 1
        self._reset_next_interval()
        self._down_activated = True
        # if not self.x_activated and not self.y_activated:
        #     self.next_interval = ticks_ms() + self.ac_intervalle
        self.pointing_device.report_y[0] = self.move_step
        self.pointing_device.hid_pending = True

    def _ms_down_release(self, key, keyboard, *args, **kwargs):
        self._down_activated = False
        self._nav_key_activated -= 1
        self._check_last()
        self.pointing_device.report_y[0] = 0
        self.pointing_device.hid_pending = False

    def _ms_left_press(self, key, keyboard, *args, **kwargs):
        self._nav_key_activated += 1
        self._reset_next_interval()
        self._left_activated = True
        self.pointing_device.report_x[0] = 0xFF & (0 - self.move_step)
        self.pointing_device.hid_pending = True

    def _ms_left_release(self, key, keyboard, *args, **kwargs):
        self._nav_key_activated -= 1
        self._left_activated = False
        self._check_last()
        self.pointing_device.report_x[0] = 0
        self.pointing_device.hid_pending = False

    def _ms_right_press(self, key, keyboard, *args, **kwargs):
        self._nav_key_activated += 1
        self._reset_next_interval()
        self._right_activated = True
        self.pointing_device.report_x[0] = self.move_step
        self.pointing_device.hid_pending = True

    def _ms_right_release(self, key, keyboard, *args, **kwargs):
        self._nav_key_activated -= 1
        self._right_activated = False
        self._check_last()
        self.pointing_device.report_x[0] = 0
        self.pointing_device.hid_pending = False
