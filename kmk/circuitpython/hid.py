import usb_hid
from kmk.abstract.hid import AbstractHidHelper
from kmk.consts import HID_REPORT_SIZES, HIDReportTypes, HIDUsage, HIDUsagePage


class HIDHelper(AbstractHidHelper):
    REPORT_BYTES = 9

    def post_init(self):
        self.devices = {}

        for device in usb_hid.devices:
            if device.usage_page == HIDUsagePage.CONSUMER and device.usage == HIDUsage.CONSUMER:
                self.devices[HIDReportTypes.CONSUMER] = device
                continue

            if device.usage_page == HIDUsagePage.KEYBOARD and device.usage == HIDUsage.KEYBOARD:
                self.devices[HIDReportTypes.KEYBOARD] = device
                continue

            if device.usage_page == HIDUsagePage.MOUSE and device.usage == HIDUsage.MOUSE:
                self.devices[HIDReportTypes.MOUSE] = device
                continue

            if (
                device.usage_page == HIDUsagePage.SYSCONTROL and
                device.usage == HIDUsage.SYSCONTROL
            ):
                self.devices[HIDReportTypes.SYSCONTROL] = device
                continue

    def hid_send(self, evt):
        # int, can be looked up in HIDReportTypes
        reporting_device_const = self.report_device[0]

        return self.devices[reporting_device_const].send_report(
            evt[1:HID_REPORT_SIZES[reporting_device_const] + 1],
        )
