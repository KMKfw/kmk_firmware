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
        self.report = 0x00
        self.hid = None
        for device in usb_hid.devices:
            if device.usage == HIDUsage.KEYBOARD:
                self.hid = device

    def __repr__(self):
        return ('LockStatus(report={})').format(self.report)

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
            if report[0] != self.report:
                self.report = report[0]
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return

    def get_num_lock(self):
        return bool(self.report & LockCode.NUMLOCK)

    def get_caps_lock(self):
        return bool(self.report & LockCode.CAPSLOCK)

    def get_scroll_lock(self):
        return bool(self.report & LockCode.SCROLLLOCK)

    def get_compose(self):
        return bool(self.report & LockCode.COMPOSE)

    def get_kana(self):
        return bool(self.report & LockCode.KANA)
