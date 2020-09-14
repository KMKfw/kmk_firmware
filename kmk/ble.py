from adafruit_ble import BLERadio
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from kmk.hid import (
    HID_REPORT_SIZES,
    AbstractHID,
    HIDReportTypes,
    HIDUsage,
    HIDUsagePage,
)

BLE_APPEARANCE_HID_KEYBOARD = 961


class BLEHID(AbstractHID):
    def post_init(self, ble_name='KMK Keyboard', **kwargs):
        self.devices = {}

        hid = HIDService()

        advertisement = ProvideServicesAdvertisement(hid)
        advertisement.appearance = BLE_APPEARANCE_HID_KEYBOARD

        ble = BLERadio()
        ble.name = ble_name
        # ble.tx_power = 2

        if not ble.connected:
            ble.start_advertising(advertisement)
            while not ble.connected:
                pass

        for device in hid.devices:
            us = device.usage
            up = device.usage_page

            if up == HIDUsagePage.CONSUMER and us == HIDUsage.CONSUMER:
                self.devices[HIDReportTypes.CONSUMER] = device
                continue

            if up == HIDUsagePage.KEYBOARD and us == HIDUsage.KEYBOARD:
                self.devices[HIDReportTypes.KEYBOARD] = device
                continue

            if up == HIDUsagePage.MOUSE and us == HIDUsage.MOUSE:
                self.devices[HIDReportTypes.MOUSE] = device
                continue

            if up == HIDUsagePage.SYSCONTROL and us == HIDUsage.SYSCONTROL:
                self.devices[HIDReportTypes.SYSCONTROL] = device
                continue

    def hid_send(self, evt):
        # int, can be looked up in HIDReportTypes
        reporting_device_const = self.report_device[0]

        report_size = HID_REPORT_SIZES[reporting_device_const]

        while len(evt) < report_size + 1:
            evt.append(0)

        return self.devices[reporting_device_const].send_report(
            evt[1 : report_size + 1]
        )
