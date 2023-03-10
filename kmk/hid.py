import supervisor
import usb_hid
from micropython import const

from storage import getmount

from kmk.keys import FIRST_KMK_INTERNAL_KEY, ConsumerKey, ModifierKey, MouseKey
from kmk.utils import clamp

try:
    from adafruit_ble import BLERadio
    from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
    from adafruit_ble.services.standard.hid import HIDService
except ImportError:
    # BLE not supported on this platform
    pass


class HIDModes:
    NOOP = 0  # currently unused; for testing?
    USB = 1
    BLE = 2

    ALL_MODES = (NOOP, USB, BLE)


class HIDReportTypes:
    KEYBOARD = 1
    MOUSE = 2
    CONSUMER = 3
    SYSCONTROL = 4


class HIDUsage:
    KEYBOARD = 0x06
    MOUSE = 0x02
    CONSUMER = 0x01
    SYSCONTROL = 0x80


class HIDUsagePage:
    CONSUMER = 0x0C
    KEYBOARD = MOUSE = SYSCONTROL = 0x01


HID_REPORT_SIZES = {
    HIDReportTypes.KEYBOARD: 8,
    HIDReportTypes.MOUSE: 4,
    HIDReportTypes.CONSUMER: 2,
    HIDReportTypes.SYSCONTROL: 8,  # TODO find the correct value for this
}


class AbstractHID:
    REPORT_BYTES = 8

    def __init__(self, **kwargs):
        self._prev_evt = bytearray(self.REPORT_BYTES)
        self._evt = bytearray(self.REPORT_BYTES)
        self.report_device = memoryview(self._evt)[0:1]
        self.report_device[0] = HIDReportTypes.KEYBOARD

        # Landmine alert for HIDReportTypes.KEYBOARD: byte index 1 of this view
        # is "reserved" and evidently (mostly?) unused. However, other modes (or
        # at least consumer, so far) will use this byte, which is the main reason
        # this view exists. For KEYBOARD, use report_mods and report_non_mods
        self.report_keys = memoryview(self._evt)[1:]

        self.report_mods = memoryview(self._evt)[1:2]
        self.report_non_mods = memoryview(self._evt)[3:]

        self._cc_report = bytearray(HID_REPORT_SIZES[HIDReportTypes.CONSUMER] + 1)
        self._cc_report[0] = HIDReportTypes.CONSUMER
        self._cc_pending = False

        self._pd_report = bytearray(HID_REPORT_SIZES[HIDReportTypes.MOUSE] + 1)
        self._pd_report[0] = HIDReportTypes.MOUSE
        self._pd_pending = False

        self.post_init()

    def __repr__(self):
        return f'{self.__class__.__name__}(REPORT_BYTES={self.REPORT_BYTES})'

    def post_init(self):
        pass

    def create_report(self, keys_pressed, axes):
        self.clear_all()

        for key in keys_pressed:
            if key.code >= FIRST_KMK_INTERNAL_KEY:
                continue

            if isinstance(key, ModifierKey):
                self.add_modifier(key)
            elif isinstance(key, ConsumerKey):
                self.add_cc(key)
            elif isinstance(key, MouseKey):
                self.add_pd(key)
            else:
                self.add_key(key)
                if key.has_modifiers:
                    for mod in key.has_modifiers:
                        self.add_modifier(mod)

        for axis in axes:
            self.move_axis(axis)

    def hid_send(self, evt):
        # Don't raise a NotImplementedError so this can serve as our "dummy" HID
        # when MCU/board doesn't define one to use (which should almost always be
        # the CircuitPython-targeting one, except when unit testing or doing
        # something truly bizarre. This will likely change eventually when Bluetooth
        # is added)
        pass

    def send(self):
        if self._evt != self._prev_evt:
            self._prev_evt[:] = self._evt
            self.hid_send(self._evt)

        if self._cc_pending:
            self.hid_send(self._cc_report)
            self._cc_pending = False

        if self._pd_pending:
            self.hid_send(self._pd_report)
            self._pd_pending = False

        return self

    def clear_all(self):
        for idx, _ in enumerate(self.report_keys):
            self.report_keys[idx] = 0x00

        self.remove_cc()
        self.remove_pd()
        self.clear_axis()

        return self

    def clear_non_modifiers(self):
        for idx, _ in enumerate(self.report_non_mods):
            self.report_non_mods[idx] = 0x00

        return self

    def add_modifier(self, modifier):
        if isinstance(modifier, ModifierKey):
            if modifier.code == ModifierKey.FAKE_CODE:
                for mod in modifier.has_modifiers:
                    self.report_mods[0] |= mod
            else:
                self.report_mods[0] |= modifier.code
        else:
            self.report_mods[0] |= modifier

        return self

    def remove_modifier(self, modifier):
        if isinstance(modifier, ModifierKey):
            if modifier.code == ModifierKey.FAKE_CODE:
                for mod in modifier.has_modifiers:
                    self.report_mods[0] ^= mod
            else:
                self.report_mods[0] ^= modifier.code
        else:
            self.report_mods[0] ^= modifier

        return self

    def add_key(self, key):
        # Try to find the first empty slot in the key report, and fill it
        placed = False

        where_to_place = self.report_non_mods

        for idx, _ in enumerate(where_to_place):
            if where_to_place[idx] == 0x00:
                where_to_place[idx] = key.code
                placed = True
                break

        if not placed:
            # TODO what do we do here?......
            pass

        return self

    def remove_key(self, key):
        where_to_place = self.report_non_mods

        for idx, _ in enumerate(where_to_place):
            if where_to_place[idx] == key.code:
                where_to_place[idx] = 0x00

        return self

    def add_cc(self, cc):
        # Add (or write over) consumer control report. There can only be one CC
        # active at any time.
        memoryview(self._cc_report)[1:3] = cc.code.to_bytes(2, 'little')
        self._cc_pending = True

    def remove_cc(self):
        # Remove consumer control report.
        report = memoryview(self._cc_report)[1:3]
        if report != b'\x00\x00':
            report[:] = b'\x00\x00'
            self._cc_pending = True

    def add_pd(self, key):
        self._pd_report[1] |= key.code
        self._pd_pending = True

    def remove_pd(self):
        if self._pd_report[1]:
            self._pd_pending = True
            self._pd_report[1] = 0x00

    def move_axis(self, axis):
        delta = clamp(axis.delta, -127, 127)
        axis.delta -= delta
        self._pd_report[axis.code + 2] = 0xFF & delta
        self._pd_pending = True

    def clear_axis(self):
        for idx in range(2, len(self._pd_report)):
            self._pd_report[idx] = 0x00


class USBHID(AbstractHID):
    REPORT_BYTES = 9

    def post_init(self):
        self.devices = {}

        for device in usb_hid.devices:
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
        if not supervisor.runtime.usb_connected:
            return

        # int, can be looked up in HIDReportTypes
        reporting_device_const = evt[0]

        return self.devices[reporting_device_const].send_report(
            evt[1 : HID_REPORT_SIZES[reporting_device_const] + 1]
        )


class BLEHID(AbstractHID):
    BLE_APPEARANCE_HID_KEYBOARD = const(961)
    # Hardcoded in CPy
    MAX_CONNECTIONS = const(2)

    def __init__(self, ble_name=str(getmount('/').label), **kwargs):
        self.ble_name = ble_name
        super().__init__()

    def post_init(self):
        self.ble = BLERadio()
        self.ble.name = self.ble_name
        self.hid = HIDService()
        self.hid.protocol_mode = 0  # Boot protocol

        # Security-wise this is not right. While you're away someone turns
        # on your keyboard and they can pair with it nice and clean and then
        # listen to keystrokes.
        # On the other hand we don't have LESC so it's like shouting your
        # keystrokes in the air
        if not self.ble.connected or not self.hid.devices:
            self.start_advertising()

    @property
    def devices(self):
        '''Search through the provided list of devices to find the ones with the
        send_report attribute.'''
        if not self.ble.connected:
            return {}

        result = {}

        for device in self.hid.devices:
            if not hasattr(device, 'send_report'):
                continue
            us = device.usage
            up = device.usage_page

            if up == HIDUsagePage.CONSUMER and us == HIDUsage.CONSUMER:
                result[HIDReportTypes.CONSUMER] = device
                continue

            if up == HIDUsagePage.KEYBOARD and us == HIDUsage.KEYBOARD:
                result[HIDReportTypes.KEYBOARD] = device
                continue

            if up == HIDUsagePage.MOUSE and us == HIDUsage.MOUSE:
                result[HIDReportTypes.MOUSE] = device
                continue

            if up == HIDUsagePage.SYSCONTROL and us == HIDUsage.SYSCONTROL:
                result[HIDReportTypes.SYSCONTROL] = device
                continue

        return result

    def hid_send(self, evt):
        if not self.ble.connected:
            return

        # int, can be looked up in HIDReportTypes
        reporting_device_const = evt[0]

        device = self.devices[reporting_device_const]

        report_size = len(device._characteristic.value)
        while len(evt) < report_size + 1:
            evt.append(0)

        return device.send_report(evt[1 : report_size + 1])

    def clear_bonds(self):
        import _bleio

        _bleio.adapter.erase_bonding()

    def start_advertising(self):
        if not self.ble.advertising:
            advertisement = ProvideServicesAdvertisement(self.hid)
            advertisement.appearance = self.BLE_APPEARANCE_HID_KEYBOARD

            self.ble.start_advertising(advertisement)

    def stop_advertising(self):
        self.ble.stop_advertising()
