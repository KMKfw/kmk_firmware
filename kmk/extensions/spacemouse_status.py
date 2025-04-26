import usb_hid
from micropython import const

from kmk.extensions import Extension

_SIX_AXIS_USAGE = const(0x08)
_LED = const(0x01)


class SpacemouseStatus(Extension):
    def __init__(self):
        self.report = 0
        self.hid = None
        self._report_updated = False

    def __repr__(self):
        return f'SpacemouseStatus(report={self.report})'

    def during_bootup(self, sandbox):
        for device in usb_hid.devices:
            if device.usage == _SIX_AXIS_USAGE:
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
        report = self.hid.get_last_received_report(4)
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

    def get_led(self):
        return bool(self.report & _LED)
