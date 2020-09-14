import usb_hid

from kmk.keys import FIRST_KMK_INTERNAL_KEY, ConsumerKey, ModifierKey


class HIDModes:
    NOOP = 0  # currently unused; for testing?
    USB = 1
    BLE = 2  # currently unused; for bluetooth

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

        self.post_init(**kwargs)

    def __repr__(self):
        return '{}(REPORT_BYTES={})'.format(self.__class__.__name__, self.REPORT_BYTES)

    def post_init(self):
        pass

    def create_report(self, keys_pressed):
        self.clear_all()

        consumer_key = None
        for key in keys_pressed:
            if isinstance(key, ConsumerKey):
                consumer_key = key
                break

        reporting_device = self.report_device[0]
        needed_reporting_device = HIDReportTypes.KEYBOARD

        if consumer_key:
            needed_reporting_device = HIDReportTypes.CONSUMER

        if reporting_device != needed_reporting_device:
            # If we are about to change reporting devices, release
            # all keys and close our proverbial tab on the existing
            # device, or keys will get stuck (mostly when releasing
            # media/consumer keys)
            self.send()

        self.report_device[0] = needed_reporting_device

        if consumer_key:
            self.add_key(consumer_key)
        else:
            for key in keys_pressed:
                if key.code >= FIRST_KMK_INTERNAL_KEY:
                    continue

                if isinstance(key, ModifierKey):
                    self.add_modifier(key)
                else:
                    self.add_key(key)

                    if key.has_modifiers:
                        for mod in key.has_modifiers:
                            self.add_modifier(mod)

        return self

    def hid_send(self, evt):
        # Don't raise a NotImplementedError so this can serve as our "dummy" HID
        # when MCU/board doesn't define one to use (which should almost always be
        # the CircuitPython-targeting one, except when unit testing or doing
        # something truly bizarre. This will likely change eventually when Bluetooth
        # is added)
        pass

    def send(self):
        self.hid_send(self._evt)

        return self

    def clear_all(self):
        for idx, _ in enumerate(self.report_keys):
            self.report_keys[idx] = 0x00

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

        if self.report_device[0] == HIDReportTypes.CONSUMER:
            where_to_place = self.report_keys

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

        if self.report_device[0] == HIDReportTypes.CONSUMER:
            where_to_place = self.report_keys

        for idx, _ in enumerate(where_to_place):
            if where_to_place[idx] == key.code:
                where_to_place[idx] = 0x00

        return self


class USBHID(AbstractHID):
    REPORT_BYTES = 9

    def post_init(self, **kwargs):
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
        # int, can be looked up in HIDReportTypes
        reporting_device_const = self.report_device[0]

        return self.devices[reporting_device_const].send_report(
            evt[1 : HID_REPORT_SIZES[reporting_device_const] + 1]
        )
