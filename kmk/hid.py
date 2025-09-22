import supervisor
import usb_hid
from micropython import const

from struct import pack, pack_into

from kmk.keys import (
    Axis,
    ConsumerKey,
    KeyboardKey,
    ModifierKey,
    MouseKey,
    SixAxis,
    SpacemouseKey,
)
from kmk.scheduler import cancel_task, create_task
from kmk.utils import Debug, clamp

try:
    from adafruit_ble import BLERadio
    from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
    from adafruit_ble.services.standard.hid import HIDService
    from storage import getmount

    _BLE_APPEARANCE_HID_KEYBOARD = const(961)
except ImportError:
    # BLE not supported on this platform
    pass


debug = Debug(__name__)


class HIDModes:
    NOOP = 0  # currently unused; for testing?
    USB = 1
    BLE = 2


_USAGE_PAGE_CONSUMER = const(0x0C)
_USAGE_PAGE_KEYBOARD = const(0x01)
_USAGE_PAGE_MOUSE = const(0x01)
_USAGE_PAGE_SIXAXIS = const(0x01)
_USAGE_PAGE_SYSCONTROL = const(0x01)

_USAGE_CONSUMER = const(0x01)
_USAGE_KEYBOARD = const(0x06)
_USAGE_MOUSE = const(0x02)
_USAGE_SIXAXIS = const(0x08)
_USAGE_SYSCONTROL = const(0x80)

_REPORT_SIZE_CONSUMER = const(2)
_REPORT_SIZE_KEYBOARD = const(8)
_REPORT_SIZE_KEYBOARD_NKRO = const(16)
_REPORT_SIZE_MOUSE = const(4)
_REPORT_SIZE_MOUSE_HSCROLL = const(5)
_REPORT_SIZE_SIXAXIS = const(12)
_REPORT_SIZE_SIXAXIS_BUTTON = const(2)
_REPORT_SIZE_SYSCONTROL = const(8)


def find_device(devices, usage_page, usage):
    for device in devices:
        if (
            device.usage_page == usage_page
            and device.usage == usage
            and hasattr(device, 'send_report')
        ):
            return device


class Report:
    def __init__(self, size):
        self.buffer = bytearray(size)
        self.pending = False

    def clear(self):
        for k, v in enumerate(self.buffer):
            if v:
                self.buffer[k] = 0x00
                self.pending = True

    def get_action_map(self):
        return {}


class KeyboardReport(Report):
    def __init__(self, size=_REPORT_SIZE_KEYBOARD):
        self.buffer = bytearray(size)
        self.prev_buffer = bytearray(size)

    @property
    def pending(self):
        return self.buffer != self.prev_buffer

    @pending.setter
    def pending(self, v):
        if v is False:
            self.prev_buffer[:] = self.buffer[:]

    def clear(self):
        for idx in range(len(self.buffer)):
            self.buffer[idx] = 0x00

    def add_key(self, key):
        # Find the first empty slot in the key report, and fill it; drop key if
        # report is full.
        idx = self.buffer.find(b'\x00', 2)

        if 0 < idx < _REPORT_SIZE_KEYBOARD:
            self.buffer[idx] = key.code

    def remove_key(self, key):
        idx = self.buffer.find(pack('B', key.code), 2)
        if 0 < idx:
            self.buffer[idx] = 0x00

    def add_modifier(self, modifier):
        self.buffer[0] |= modifier.code

    def remove_modifier(self, modifier):
        self.buffer[0] &= ~modifier.code

    def get_action_map(self):
        return {KeyboardKey: self.add_key, ModifierKey: self.add_modifier}


class NKROKeyboardReport(KeyboardReport):
    def __init__(self):
        super().__init__(_REPORT_SIZE_KEYBOARD_NKRO)

    def add_key(self, key):
        self.buffer[(key.code >> 3) + 1] |= 1 << (key.code & 0x07)

    def remove_key(self, key):
        self.buffer[(key.code >> 3) + 1] &= ~(1 << (key.code & 0x07))


class ConsumerControlReport(Report):
    def __init__(self):
        super().__init__(_REPORT_SIZE_CONSUMER)

    def add_cc(self, cc):
        pack_into('<H', self.buffer, 0, cc.code)
        self.pending = True

    def remove_cc(self):
        if self.buffer != b'\x00\x00':
            self.buffer = b'\x00\x00'
            self.pending = True

    def get_action_map(self):
        return {ConsumerKey: self.add_cc}


class PointingDeviceReport(Report):
    def __init__(self, size=_REPORT_SIZE_MOUSE):
        super().__init__(size)

    def add_button(self, key):
        self.buffer[0] |= key.code
        self.pending = True

    def remove_button(self, key):
        self.buffer[0] &= ~key.code
        self.pending = True

    def move_axis(self, axis):
        delta = clamp(axis.delta, -127, 127)
        axis.delta -= delta
        try:
            self.buffer[axis.code + 1] = 0xFF & delta
            self.pending = True
        except IndexError:
            if debug.enabled:
                debug(axis, ' not supported')

    def get_action_map(self):
        return {Axis: self.move_axis, MouseKey: self.add_button}


class HSPointingDeviceReport(PointingDeviceReport):
    def __init__(self):
        super().__init__(_REPORT_SIZE_MOUSE_HSCROLL)


class SixAxisDeviceReport(Report):
    def __init__(self, size=_REPORT_SIZE_SIXAXIS):
        super().__init__(size)

    def move_six_axis(self, axis):
        delta = clamp(axis.delta, -500, 500)
        axis.delta -= delta
        index = 2 * axis.code
        try:
            self.buffer[index] = 0xFF & delta
            self.buffer[index + 1] = 0xFF & (delta >> 8)
            self.pending = True
        except IndexError:
            if debug.enabled:
                debug(axis, ' not supported')

    def get_action_map(self):
        return {SixAxis: self.move_six_axis}


class SixAxisDeviceButtonReport(Report):
    def __init__(self, size=_REPORT_SIZE_SIXAXIS_BUTTON):
        super().__init__(size)

    def add_six_axis_button(self, key):
        self.buffer[0] |= key.code
        self.pending = True

    def remove_six_axis_button(self, key):
        self.buffer[0] &= ~key.code
        self.pending = True

    def get_action_map(self):
        return {SpacemouseKey: self.add_six_axis_button}


class IdentifiedDevice:
    def __init__(self, device, report_id):
        self.device = device
        self.report_id = report_id

    def send_report(self, buffer):
        self.device.send_report(buffer, self.report_id)


class AbstractHID:
    def __init__(self):
        self.report_map = {}
        self.device_map = {}
        self._setup_task = create_task(self.setup, period_ms=100)

    def __repr__(self):
        return self.__class__.__name__

    def create_report(self, keys):
        for report in self.device_map.keys():
            report.clear()

        for key in keys:
            if action := self.report_map.get(type(key)):
                action(key)

    def send(self):
        for report in self.device_map.keys():
            if report.pending:
                self.device_map[report].send_report(report.buffer)
                report.pending = False

    def setup(self):
        if not self.connected:
            return

        try:
            self.setup_keyboard_hid()
            self.setup_consumer_control()
            self.setup_mouse_hid()
            self.setup_sixaxis_hid()

            cancel_task(self._setup_task)
            self._setup_task = None
            if debug.enabled:
                self.show_debug()

        except OSError as e:
            if debug.enabled:
                debug(type(e), ':', e)

    def setup_keyboard_hid(self):
        if device := find_device(self.devices, _USAGE_PAGE_KEYBOARD, _USAGE_KEYBOARD):
            # bodgy NKRO autodetect
            try:
                report = KeyboardReport()
                device.send_report(report.buffer)
            except ValueError:
                report = NKROKeyboardReport()

            self.report_map.update(report.get_action_map())
            self.device_map[report] = device

    def setup_consumer_control(self):
        if device := find_device(self.devices, _USAGE_PAGE_CONSUMER, _USAGE_CONSUMER):
            report = ConsumerControlReport()
            self.report_map.update(report.get_action_map())
            self.device_map[report] = device

    def setup_mouse_hid(self):
        if device := find_device(self.devices, _USAGE_PAGE_MOUSE, _USAGE_MOUSE):
            # bodgy pointing device panning autodetect
            try:
                report = PointingDeviceReport()
                device.send_report(report.buffer)
            except ValueError:
                report = HSPointingDeviceReport()

            self.report_map.update(report.get_action_map())
            self.device_map[report] = device

    def setup_sixaxis_hid(self):
        if device := find_device(self.devices, _USAGE_PAGE_SIXAXIS, _USAGE_SIXAXIS):
            report = SixAxisDeviceReport()
            self.report_map.update(report.get_action_map())
            self.device_map[report] = IdentifiedDevice(device, 1)
            report = SixAxisDeviceButtonReport()
            self.report_map.update(report.get_action_map())
            self.device_map[report] = IdentifiedDevice(device, 3)

    def show_debug(self):
        for report in self.device_map.keys():
            debug('use ', report.__class__.__name__)


class USBHID(AbstractHID):
    @property
    def connected(self):
        return supervisor.runtime.usb_connected

    @property
    def devices(self):
        return usb_hid.devices


class BLEHID(AbstractHID):
    def __init__(self, ble_name=None):
        super().__init__()

        self.ble = BLERadio()
        self.ble.name = ble_name if ble_name else getmount('/').label
        self.ble_connected = False

        self.hid = HIDService()
        self.hid.protocol_mode = 0  # Boot protocol

        create_task(self.ble_monitor, period_ms=1000)

    @property
    def connected(self):
        return self.ble.connected

    @property
    def devices(self):
        return self.hid.devices

    def ble_monitor(self):
        if self.ble_connected != self.connected:
            self.ble_connected = self.connected
            if debug.enabled:
                if self.connected:
                    debug('BLE connected')
                else:
                    debug('BLE disconnected')

        if not self.connected:
            # Security-wise this is not right. While you're away someone turns
            # on your keyboard and they can pair with it nice and clean and then
            # listen to keystrokes.
            # On the other hand we don't have LESC so it's like shouting your
            # keystrokes in the air
            self.start_advertising()

    def clear_bonds(self):
        import _bleio

        _bleio.adapter.erase_bonding()

    def start_advertising(self):
        if not self.ble.advertising:
            advertisement = ProvideServicesAdvertisement(self.hid)
            advertisement.appearance = _BLE_APPEARANCE_HID_KEYBOARD

            self.ble.start_advertising(advertisement)

    def stop_advertising(self):
        self.ble.stop_advertising()
