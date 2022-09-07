from supervisor import ticks_ms

from kmk.hid import HIDModes
from kmk.kmktime import check_deadline


class BLE_UART:
    def __init__(self, is_target, uart_interval=20):
        try:
            from adafruit_ble import BLERadio
            from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
            from adafruit_ble.services.nordic import UARTService

            self.BLERadio = BLERadio
            self.ProvideServicesAdvertisement = ProvideServicesAdvertisement
            self.UARTService = UARTService
        except ImportError:
            print('BLE Import error')
            return  # BLE isn't supported on this platform

        self._debug_enabled = True
        self._ble_last_scan = ticks_ms() - 5000
        self._connection_count = 0
        self._split_connected = False
        self._uart_connection = None
        self._advertisment = None  # Seems to not be used anywhere
        self._advertising = False
        self._psave_enabled = False
        self._uart = None
        self._uart_interval = uart_interval
        self._is_target = is_target

    @property
    def in_waiting(self):
        return self._uart.in_waiting

    def read(self, n):
        return self._uart.read(n)

    def readinto(self, buf):
        return self._uart.readinto(buf)

    def write(self, buffer):
        try:
            self._uart.write(buffer)
        except OSError:
            try:
                self._uart.disconnect()
            except:  # noqa: E722
                if self._debug_enabled:
                    print('UART disconnect failed')

            if self._debug_enabled:
                print('Connection error')
            self._uart_connection = None
            self._uart = None

    def check_connection(self, keyboard):
        self._check_all_connections(keyboard)

    def enable_powersave(self, enable=True):
        if enable:
            if self._uart_connection and not self._psave_enable:
                self._uart_connection.connection_interval = self._uart_interval
                self._psave_enabled = True
        else:
            if self._uart_connection and self._psave_enable:
                self._uart_connection.connection_interval = 11.25
                self._psave_enable = False

    def _check_all_connections(self, keyboard):
        '''Validates the correct number of BLE connections'''
        self._previous_connection_count = self._connection_count
        self._connection_count = len(self._ble.connections)
        if self._is_target:
            if self._advertising or not self._check_if_split_connected():
                self._target_advertise()
            elif self._connection_count < 2 and keyboard.hid_type == HIDModes.BLE:
                keyboard._hid_helper.start_advertising()

        elif not self._is_target and self._connection_count < 1:
            self._initiator_scan()

    def _check_if_split_connected(self):
        # I'm looking for a way how to recognize which connection is on and which one off
        # For now, I found that service name relation to having other CP device
        if self._connection_count == 0:
            return False
        if self._connection_count == 2:
            self._split_connected = True
            return True

        # Polling this takes some time so I check only if connection_count changed
        if self._previous_connection_count == self._connection_count:
            return self._split_connected

        bleio_connection = self._ble.connections[0]._bleio_connection
        connection_services = bleio_connection.discover_remote_services()
        for service in connection_services:
            if str(service.uuid).startswith("UUID('adaf0001"):
                self._split_connected = True
                return True
        return False

    def _initiator_scan(self):
        '''Scans for target device'''
        self._uart = None
        self._uart_connection = None
        # See if any existing connections are providing UARTService.
        self._connection_count = len(self._ble.connections)
        if self._connection_count > 0 and not self._uart:
            for connection in self._ble.connections:
                if self.UARTService in connection:
                    self._uart_connection = connection
                    self._uart_connection.connection_interval = 11.25
                    self._uart = self._uart_connection[self.UARTService]
                    break

        if not self._uart:
            if self._debug_enabled:
                print('Scanning')
            self._ble.stop_scan()
            for adv in self._ble.start_scan(
                self.ProvideServicesAdvertisement, timeout=20
            ):
                if self._debug_enabled:
                    print('Scanning')
                if self.UARTService in adv.services and adv.rssi > -70:
                    self._uart_connection = self._ble.connect(adv)
                    self._uart_connection.connection_interval = 11.25
                    self._uart = self._uart_connection[self.UARTService]
                    self._ble.stop_scan()
                    if self._debug_enabled:
                        print('Scan complete')
                    break
        self._ble.stop_scan()

    def _target_advertise(self):
        '''Advertises the target for the initiator to find'''
        # Give previous advertising some time to complete
        if self._advertising:
            if self._check_if_split_connected():
                if self._debug_enabled:
                    print('Advertising complete')
                self._ble.stop_advertising()
                self._advertising = False
                return

            if not self.ble_rescan_timer():
                return

            if self._debug_enabled:
                print('Advertising not answered')

        self._ble.stop_advertising()
        if self._debug_enabled:
            print('Advertising')
        # Uart must not change on this connection if reconnecting
        if not self._uart:
            self._uart = self.UARTService()
        advertisement = self.ProvideServicesAdvertisement(self._uart)

        self._ble.start_advertising(advertisement)
        self._advertising = True
        self.ble_time_reset()

    def ble_rescan_timer(self):
        '''If true, the rescan timer is up'''
        return not bool(check_deadline(ticks_ms(), self._ble_last_scan, 5000))

    def ble_time_reset(self):
        '''Resets the rescan timer'''
        self._ble_last_scan = ticks_ms()
