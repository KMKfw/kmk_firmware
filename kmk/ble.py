from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from kmk.hid import HID_REPORT_SIZES, AbstractHID

BLE_APPEARANCE_HID_KEYBOARD = 961


class BLEHID(AbstractHID):
    def post_init(self, ble_name='KMK Keyboard', **kwargs):
        self.conn = []

        self.ble = BLERadio()
        self.ble.name = ble_name
        self.hid = HIDService()

        # Security-wise this is not right. While you're away someone turns
        # on your keyboard and they can pair with it nice and clean and then
        # listen to keystrokes.
        # On the other hand we don't have LESC so it's like shouting your
        # keystrokes in the air
        if not self.ble.connected:
            self.start_advertising()
            while not self.ble.connected or not self.hid.devices:
                pass

        # int, can be looked up in HIDReportTypes
        reporting_device_const = self.report_device[0]

        self.conn = self.hid.devices[reporting_device_const]

        self.ble.stop_advertising()

    def hid_send(self, evt):
        # int, can be looked up in HIDReportTypes
        reporting_device_const = self.report_device[0]

        report_size = HID_REPORT_SIZES[reporting_device_const]

        while len(evt) < report_size + 1:
            evt.append(0)

        print(self.conn)
        return self.conn.send_report(
            evt[1 : report_size + 1]
        )

    def clear_bonds(self):
        import _bleio

        _bleio.adapter.erase_bonding()

    def start_advertising(self):
        advertisement = ProvideServicesAdvertisement(self.hid)
        advertisement.appearance = BLE_APPEARANCE_HID_KEYBOARD

        self.ble.start_advertising(advertisement)

    def stop_advertising(self):
        self.ble.stop_advertising()
