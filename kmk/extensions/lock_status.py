import usb_hid

from kmk.extensions import Extension
from kmk.hid import HIDUsage


class LockCode:
    NUMLOCK = 0x01
    CAPSLOCK = 0x02
    SCROLLLOCK = 0x04
    COMPOSE = 0x08
    KANA = 0x10
    RESERVED = 0x20


class LockStatus(Extension):
    def __init__(self):
        self.report = None
        self.hid = None
        self._report_updated = False
        for device in usb_hid.devices:
            if device.usage == HIDUsage.KEYBOARD:
                self.hid = device

    def __repr__(self):
        return f'LockStatus(report={self.report})'

    def during_bootup(self, sandbox):
        return

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        if self.hid:
            report = self.hid.get_last_received_report()
            if report and report[0] != self.report:
                self.report = report[0]
                self._report_updated = True
            else:
                self._report_updated = False
        else:
            # _report_updated shouldn't ever be True if hid is
            # falsy, but I would rather be safe than sorry.
            self._report_updated = False
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return

    @property
    def report_updated(self):
        return self._report_updated

    def check_state(self, lock_code):
        # This is false if there's no valid report, or all report bits are zero
        if self.report:
            return bool(self.report & lock_code)
        else:
            # Just in case, default to False if we don't know anything
            return False

    def get_num_lock(self):
        return self.check_state(LockCode.NUMLOCK)

    def get_caps_lock(self):
        return self.check_state(LockCode.CAPSLOCK)

    def get_scroll_lock(self):
        return self.check_state(LockCode.SCROLLLOCK)

    def get_compose(self):
        return self.check_state(LockCode.COMPOSE)

    def get_kana(self):
        return self.check_state(LockCode.KANA)
