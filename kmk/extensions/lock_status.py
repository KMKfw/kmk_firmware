import usb_hid
from micropython import const

from kmk.extensions import Extension

_NUMLOCK = const(0x01)
_CAPSLOCK = const(0x02)
_SCROLLLOCK = const(0x04)
_COMPOSE = const(0x08)
_KANA = const(0x10)


class LockStatus(Extension):
    def __init__(self):
        self.report = 0
        self.hid = None
        self._report_updated = False

    def __repr__(self):
        return f'LockStatus(report={self.report})'

    def during_bootup(self, sandbox):
        for device in usb_hid.devices:
            if device.usage == usb_hid.Device.KEYBOARD.usage:
                self.hid = device
        if self.hid is None:
            raise RuntimeError

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        report = self.hid.get_last_received_report()
        if report is None:
            self._report_updated = False
        else:
            self.report = report[0]
            self._report_updated = True

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return

    @property
    def report_updated(self):
        return self._report_updated

    def get_num_lock(self):
        return bool(self.report & _NUMLOCK)

    def get_caps_lock(self):
        return bool(self.report & _CAPSLOCK)

    def get_scroll_lock(self):
        return bool(self.report & _SCROLLLOCK)

    def get_compose(self):
        return bool(self.report & _COMPOSE)

    def get_kana(self):
        return bool(self.report & _COMPOSE)
