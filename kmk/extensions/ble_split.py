'''Enables splitting keyboards wirelessly'''
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from kmk.extensions import Extension
from kmk.hid import HIDModes
from kmk.kmktime import ticks_diff, ticks_ms
from kmk.matrix import intify_coordinate


class BLE_Split(Extension):
    '''Enables splitting keyboards wirelessly'''

    def __init__(self, split_flip=True, split_side=None, hid_type=HIDModes.BLE):
        self._is_target = True
        self._uart_buffer = []
        self.hid_type = hid_type
        self.split_flip = split_flip
        self.split_side = split_side
        self.split_offset = None
        self._ble = BLERadio()
        self._ble_last_scan = ticks_ms() - 5000
        self._is_target = True
        self._connection_count = 0
        self._uart = None
        self._uart_connection = None
        self._advertisment = None
        self._advertising = False

    def __repr__(self):
        return f'BLE_SPLIT({self._to_dict()})'

    def _to_dict(self):
        return f'''
        BLE_Split( _ble={self._ble}
        _ble_last_scan={self._ble_last_scan}
        _is_target={self._is_target}
        _uart_buffer={self._uart_buffer}
        _split_flip={self.split_flip}
        _split_side={self.split_side} )
        '''

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        self._is_target = bool(self.split_side == 'Left')

        if self.split_flip and not self._is_target:
            keyboard.col_pins = list(reversed(keyboard.col_pins))

        self.split_offset = len(keyboard.col_pins)

        # Attempt to sanely guess a coord_mapping if one is not provided.
        if not keyboard.coord_mapping:
            keyboard.coord_mapping = []

            rows_to_calc = len(keyboard.row_pins) * 2
            cols_to_calc = len(keyboard.col_pins) * 2

            for ridx in range(rows_to_calc):
                for cidx in range(cols_to_calc):
                    keyboard.coord_mapping.append(intify_coordinate(ridx, cidx))

    def before_matrix_scan(self, keyboard):
        self._check_all_connections()
        return self._receive()

    def after_matrix_scan(self, keyboard, matrix_update):
        if matrix_update:
            matrix_update = self._send(matrix_update)
            return matrix_update
        return None

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

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
                if UARTService in connection:
                    self._uart_connection = connection
                    self._uart_connection.connection_interval = 11.25
                    self._uart = self._uart_connection[UARTService]
                    break

        if not self._uart:
            print('Scanning')
            self._ble.stop_scan()
            for adv in self._ble.start_scan(ProvideServicesAdvertisement, timeout=20):
                print('Scanning')
                if UARTService in adv.services:
                    self._uart_connection = self._ble.connect(adv)
                    self._uart_connection.connection_interval = 11.25
                    self._uart = self._uart_connection[UARTService]
                    self._ble.stop_scan()
                    print('Scan complete')
                    break
        self._ble.stop_scan()

    def _target_advertise(self):
        '''Advertises the target for the initiator to find'''
        self._ble.stop_advertising()
        print('Advertising')
        # Uart must not change on this connection if reconnecting
        if not self._uart:
            self._uart = UARTService()
        advertisement = ProvideServicesAdvertisement(self._uart)

        self._ble.stop_advertising()
        self._ble.start_advertising(advertisement)

        self.ble_time_reset()
        while not self.ble_rescan_timer():
            self._connection_count = len(self._ble.connections)
            if self._connection_count > 1:
                self.ble_time_reset()
                print('Advertising complete')
                break
        self._ble.stop_advertising()

    def ble_rescan_timer(self):
        '''If true, the rescan timer is up'''
        return bool(ticks_diff(ticks_ms(), self._ble_last_scan) > 5000)

    def ble_time_reset(self):
        '''Resets the rescan timer'''
        self._ble_last_scan = ticks_ms()

    def _send(self, update):
        if self._uart:
            try:
                if not self._is_target:
                    update[1] += self.split_offset
                self._uart.write(update)
            except OSError:
                try:
                    self._uart.disconnect()
                except:  # noqa: E722
                    print('UART disconnect failed')
                print('Connection error')
                self._uart_connection = None
                self._uart = None
        return update

    def _receive(self):
        if self._uart is not None and self._uart.in_waiting > 0 or self._uart_buffer:
            while self._uart.in_waiting >= 3:
                self._uart_buffer.append(self._uart.read(3))
            if self._uart_buffer:
                update = bytearray(self._uart_buffer.pop(0))
                return update

        return None
