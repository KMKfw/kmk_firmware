from supervisor import ticks_ms

from storage import getmount

from kmk.kmktime import check_deadline
from kmk.modules.split import AbstractSplit


class BleSplit(AbstractSplit):
    '''Enables splitting keyboards wirelessly'''

    def __init__(
        self,
        *,
        split_flip=True,
        split_side=None,
        split_target_left=True,
        uart_interval=20,
        debug_enabled=False,
    ):
        super().__init__(
            split_flip=split_flip,
            split_side=split_side,
            split_target_left=split_target_left,
        )
        self._uart_interval = uart_interval
        self._debug_enabled = debug_enabled

        self._uart = None
        self._uart_buffer = []

        # BLE imports and inits
        try:
            from adafruit_ble import BLERadio
            from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
            from adafruit_ble.services.nordic import UARTService

            self.ProvideServicesAdvertisement = ProvideServicesAdvertisement
            self.UARTService = UARTService
        except ImportError:
            print('BLE Import error')
            return  # BLE isn't supported on this platform
        self._ble = BLERadio()
        self._ble_last_scan = ticks_ms() - 5000
        self._connection_count = 0
        self._uart_connection = None
        self._advertisment = None
        self._advertising = False
        self._psave_enable = False

    def during_bootup(self, keyboard):
        super().during_bootup(keyboard)

        # Set up name for BLE advertisment
        name = str(getmount('/').label)
        self._ble.name = name

    def before_matrix_scan(self, keyboard):
        self._check_all_connections()
        self._receive_ble(keyboard)

    def after_matrix_scan(self, keyboard):
        if keyboard.matrix_update:
            self._send_ble(keyboard.matrix_update)

    def on_powersave_enable(self, keyboard):
        if self._uart_connection and not self._psave_enable:
            self._uart_connection.connection_interval = self._uart_interval
            self._psave_enable = True

    def on_powersave_disable(self, keyboard):
        if self._uart_connection and self._psave_enable:
            self._uart_connection.connection_interval = 11.25
            self._psave_enable = False

    def _send_ble(self, update):
        if self._uart:
            try:
                update = self._serialize_update(update)
                self._uart.write(self.MATRIX_HEADER)
                self._uart.write(update)
                self._uart.write(self._checksum(update))
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

    def _receive_ble(self, keyboard):
        if self._uart is not None and self._uart.in_waiting > 0 or self._uart_buffer:
            while self._uart.in_waiting >= self.UPDATE_SIZE + 2:
                # Check the header
                if self._uart.read(1) == self.MATRIX_HEADER:
                    update = self._uart.read(self.UPDATE_SIZE)

                    # check the checksum
                    if self._checksum(update) == self._uart.read(1):
                        self._uart_buffer.append(self._deserialize_update(update))
            if self._uart_buffer:
                keyboard.secondary_matrix_update = self._uart_buffer.pop(0)

    def _check_all_connections(self):
        '''Validates the correct number of BLE connections'''
        self._connection_count = len(self._ble.connections)
        if self._is_target and self._connection_count < 2:
            self._target_advertise()
        elif not self._is_target and self._connection_count < 1:
            self._initiator_scan()

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
        self._ble.stop_advertising()
        if self._debug_enabled:
            print('Advertising')
        # Uart must not change on this connection if reconnecting
        if not self._uart:
            self._uart = self.UARTService()
        advertisement = self.ProvideServicesAdvertisement(self._uart)

        self._ble.start_advertising(advertisement)

        self.ble_time_reset()
        while not self.ble_rescan_timer():
            self._connection_count = len(self._ble.connections)
            if self._connection_count > 1:
                self.ble_time_reset()
                if self._debug_enabled:
                    print('Advertising complete')
                break
        self._ble.stop_advertising()

    def ble_rescan_timer(self):
        '''If true, the rescan timer is up'''
        return not bool(check_deadline(ticks_ms(), self._ble_last_scan, 5000))

    def ble_time_reset(self):
        '''Resets the rescan timer'''
        self._ble_last_scan = ticks_ms()
