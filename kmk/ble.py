from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from kmk.hid import AbstractHID

BLE_APPEARANCE_HID_KEYBOARD = 961
# Hardcoded in CPy
MAX_CONNECTIONS = 2


class BLEHID(AbstractHID):
    def post_init(self, ble_name='KMK Keyboard', **kwargs):
        self.conn_id = -1

        self.ble = BLERadio()
        self.ble.name = ble_name
        self.hid = HIDService()
        self.hid.protocol_mode = 0  # Boot protocol

        # Security-wise this is not right. While you're away someone turns
        # on your keyboard and they can pair with it nice and clean and then
        # listen to keystrokes.
        # On the other hand we don't have LESC so it's like shouting your
        # keystrokes in the air
        if not self.ble.connected or not self.hid.devices:
            self.start_advertising()

        self.conn_id = 0

    @property
    def devices(self):
        '''Search through the provided list of devices to find the ones with the
        send_report attribute.'''
        if not self.ble.connected:
            return []

        result = []
        # Security issue:
        # This introduces a race condition. Let's say you have 2 active
        # connections: Alice and Bob - Alice is connection 1 and Bob 2.
        # Now Chuck who has already paired with the device in the past
        # (this assumption is needed only in the case of LESC)
        # wants to gather the keystrokes you send to Alice. You have
        # selected right now to talk to Alice (1) and you're typing a secret.
        # If Chuck kicks Alice off and is quick enough to connect to you,
        # which means quicker than the running interval of this function,
        # he'll be earlier in the `self.hid.devices` so will take over the
        # selected 1 position in the resulted array.
        # If no LESC is in place, Chuck can sniff the keystrokes anyway
        for device in self.hid.devices:
            if hasattr(device, 'send_report'):
                result.append(device)

        return result

    def _check_connection(self):
        devices = self.devices
        if not devices:
            return False

        if self.conn_id >= len(devices):
            self.conn_id = len(devices) - 1

        if self.conn_id < 0:
            return False

        if not devices[self.conn_id]:
            return False

        return True

    def hid_send(self, evt):
        if not self._check_connection():
            return

        device = self.devices[self.conn_id]

        while len(evt) < len(device._characteristic.value) + 1:
            evt.append(0)

        return device.send_report(evt[1:])

    def clear_bonds(self):
        import _bleio

        _bleio.adapter.erase_bonding()

    def next_connection(self):
        self.conn_id = (self.conn_id + 1) % len(self.devices)

    def previous_connection(self):
        self.conn_id = (self.conn_id - 1) % len(self.devices)

    def start_advertising(self):
        advertisement = ProvideServicesAdvertisement(self.hid)
        advertisement.appearance = BLE_APPEARANCE_HID_KEYBOARD

        self.ble.start_advertising(advertisement)

    def stop_advertising(self):
        self.ble.stop_advertising()
