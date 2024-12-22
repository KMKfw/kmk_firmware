import supervisor
import usb_hid
from micropython import const

from storage import getmount

from kmk.keys import ConsumerKey, KeyboardKey, ModifierKey, MouseKey
from kmk.scheduler import cancel_task, create_task
from kmk.utils import Debug, clamp

try:
    from adafruit_ble import BLERadio
    from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
    from adafruit_ble.services.standard.hid import HIDService
except ImportError:
    # BLE not supported on this platform
    pass


debug = Debug(__name__)


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
    report_bytes_default = 8
    report_bytes_nkro = 17
    REPORT_BYTES = report_bytes_default
    hid_devices = {}
    hid_ready = False

    def __init__(self, **kwargs):
        self._nkro = False
        self._mouse = True
        self._pan = False
        self.find_devices()
        self.setup_keyboard_hid()
        self.setup_consumer_control()
        self.setup_mouse_hid()

    def show_debug(self):
        if self._nkro:
            debug('use NKRO')
        else:
            debug('use 6KRO')
        if self._mouse and self._pan:
            debug('enable horizontal scrolling mouse')
        elif self._mouse:
            debug('enable mouse')
        else:
            debug('disable mouse')

    def find_devices(self):
        self.devices = {}

        for device in self.hid_devices:
            if not hasattr(device, 'send_report'):
                continue
            us = device.usage
            up = device.usage_page

            if up == HIDUsagePage.CONSUMER and us == HIDUsage.CONSUMER:
                self.devices[HIDReportTypes.CONSUMER] = device
            elif up == HIDUsagePage.KEYBOARD and us == HIDUsage.KEYBOARD:
                self.devices[HIDReportTypes.KEYBOARD] = device
            elif up == HIDUsagePage.MOUSE and us == HIDUsage.MOUSE:
                self.devices[HIDReportTypes.MOUSE] = device
            elif up == HIDUsagePage.SYSCONTROL and us == HIDUsage.SYSCONTROL:
                self.devices[HIDReportTypes.SYSCONTROL] = device

    def setup_keyboard_hid(self):
        self.REPORT_BYTES = self.report_bytes_default
        self._evt = bytearray(self.REPORT_BYTES)
        self._evt[0] = HIDReportTypes.KEYBOARD

        # bodgy NKRO autodetect
        try:
            self.hid_send(self._evt)
        except ValueError:
            self.REPORT_BYTES = self.report_bytes_nkro
            self._evt = bytearray(self.REPORT_BYTES)
            self._evt[0] = HIDReportTypes.KEYBOARD
            self._nkro = True

        self._prev_evt = bytearray(self.REPORT_BYTES)

        # Landmine alert for HIDReportTypes.KEYBOARD: byte index 1 of this view
        # is "reserved" and evidently (mostly?) unused. However, other modes (or
        # at least consumer, so far) will use this byte, which is the main reason
        # this view exists. For KEYBOARD, use report_mods and report_non_mods
        self.report_keys = memoryview(self._evt)[1:]

        self.report_mods = memoryview(self._evt)[1:2]
        self.report_non_mods = memoryview(self._evt)[3:]

    def setup_consumer_control(self):
        self._cc_report = bytearray(HID_REPORT_SIZES[HIDReportTypes.CONSUMER] + 1)
        self._cc_report[0] = HIDReportTypes.CONSUMER
        self._cc_pending = False

    def setup_mouse_hid(self):
        self._pd_report = bytearray(HID_REPORT_SIZES[HIDReportTypes.MOUSE] + 1)
        self._pd_report[0] = HIDReportTypes.MOUSE
        self._pd_pending = False

        # bodgy pointing device panning autodetect
        try:
            self.hid_send(self._pd_report)
        except ValueError:
            self._pd_report = bytearray(6)
            self._pd_report[0] = HIDReportTypes.MOUSE
            self._pan = True
        except KeyError:
            self._mouse = False

    def __repr__(self):
        return f'{self.__class__.__name__}(REPORT_BYTES={self.REPORT_BYTES})'

    def create_report(self, keys_pressed, axes):
        self.clear_all()

        for key in keys_pressed:
            if isinstance(key, KeyboardKey):
                self.add_key(key)
            elif isinstance(key, ModifierKey):
                self.add_modifier(key)
            elif isinstance(key, ConsumerKey):
                self.add_cc(key)
            elif isinstance(key, MouseKey):
                self.add_pd(key)

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
            self.report_mods[0] |= modifier.code
        else:
            self.report_mods[0] |= modifier

        return self

    def remove_modifier(self, modifier):
        if isinstance(modifier, ModifierKey):
            self.report_mods[0] ^= modifier.code
        else:
            self.report_mods[0] ^= modifier

        return self

    def add_key(self, key):
        if not self._nkro:
            # Try to find the first empty slot in the key report, and fill it
            idx = self._evt.find(b'\x00', 3)

            if idx < len(self._evt):
                self._evt[idx] = key.code
            else:
                # TODO what do we do here?......
                pass
        else:
            self.report_keys[(key.code >> 3) + 1] |= 1 << (key.code & 0x07)

    def remove_key(self, key):
        if not self._nkro:
            code = key.code.to_bytes(1, 'little')
            idx = self._evt.find(code, 3)
            self._evt[idx] = 0x00
        else:
            self.report_keys[(key.code >> 3) + 1] &= ~(1 << (key.code & 0x07))

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
        try:
            self._pd_report[axis.code + 2] = 0xFF & delta
            self._pd_pending = True
        except IndexError:
            if debug.enabled:
                debug('Axis(', axis.code, ') not supported')

    def clear_axis(self):
        for idx in range(2, len(self._pd_report)):
            self._pd_report[idx] = 0x00

    def has_key(self, key):
        if isinstance(key, ModifierKey):
            return bool(self.report_mods[0] & key.code)
        else:
            if not self._nkro:
                code = key.code.to_bytes(1, 'little')
                return self.report_non_mods.find(code) > 0
            else:
                part = self.report_keys[(key.code >> 3) + 1]
                return bool(part & (1 << (key.code & 0x07)))
        return False


class USBHID(AbstractHID):
    report_bytes_default = 9
    REPORT_BYTES = report_bytes_default

    def __init__(self, **kwargs):
        self.hid = usb_hid
        self.hid_devices = self.hid.devices
        super().__init__(**kwargs)
        self._setup_task = self.wait_until_connected()

    def test_reports(self):
        if self._connected():
            try:
                self.hid_ready = True
                self.setup_keyboard_hid()
                self.setup_consumer_control()
                self.setup_mouse_hid()
                cancel_task(self._setup_task)
                self._setup_task = None
                if debug.enabled:
                    self.show_debug()
                self.hid_ready = True
            except OSError as e:
                if debug.enabled:
                    debug(type(e), ':', e)

    def wait_until_connected(self, period_ms=200):
        return create_task(self.test_reports, period_ms=period_ms)

    def _connected(self):
        return supervisor.runtime.usb_connected

    def hid_send(self, evt):
        if not self.hid_ready or not self._connected():
            return

        # int, can be looked up in HIDReportTypes
        reporting_device_const = evt[0]

        return self.devices[reporting_device_const].send_report(evt[1:])


class BLEHID(AbstractHID):
    BLE_APPEARANCE_HID_KEYBOARD = const(961)
    # Hardcoded in CPy
    MAX_CONNECTIONS = const(2)
    ble_connected = False

    def __init__(self, ble_name=str(getmount('/').label), **kwargs):
        self.ble_name = ble_name
        self.ble = BLERadio()
        self.ble.name = self.ble_name
        self.hid = HIDService()
        self.hid_devices = self.hid.devices
        self.hid.protocol_mode = 0  # Boot protocol
        super().__init__(**kwargs)
        self.start_ble_monitor()

    def _connected(self):
        return self.ble.connected

    def ble_monitor(self):
        if self.ble_connected != self._connected():
            self.ble_connected = self._connected()
            if self._connected():
                self.find_devices()
                self.hid_ready = True
                if debug.enabled:
                    debug('BLE connected')
            else:
                self.hid_ready = False
                # Security-wise this is not right. While you're away someone turns
                # on your keyboard and they can pair with it nice and clean and then
                # listen to keystrokes.
                # On the other hand we don't have LESC so it's like shouting your
                # keystrokes in the air
                self.start_advertising()
                if debug.enabled:
                    debug('BLE disconnected')

    def start_ble_monitor(self, period_ms=200):
        return create_task(self.setup, period_ms=period_ms)

    def hid_send(self, evt):
        if not self.hid_ready or not self._connected():
            return

        # int, can be looked up in HIDReportTypes
        reporting_device_const = evt[0]

        device = self.devices[reporting_device_const]

        report_size = len(device._characteristic.value)
        while len(evt) < report_size + 1:
            evt.append(0)

        return device.send_report(evt[1 : report_size + 1])  # noqa: E203

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
