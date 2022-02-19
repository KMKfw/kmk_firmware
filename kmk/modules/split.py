'''Enables splitting keyboards wirelessly or wired'''
import busio
from micropython import const
from supervisor import runtime, ticks_ms

from storage import getmount

from kmk.hid import HIDModes
from kmk.kmktime import check_deadline
from kmk.matrix import intify_coordinate
from kmk.modules import Module


class SplitSide:
    LEFT = const(1)
    RIGHT = const(2)


class SplitType:
    UART = const(1)
    I2C = const(2)  # unused
    ONEWIRE = const(3)  # unused
    BLE = const(4)


class Split(Module):
    '''Enables splitting keyboards wirelessly, or wired'''

    def __init__(
        self,
        split_flip=True,
        split_side=None,
        split_type=SplitType.UART,
        split_target_left=True,
        uart_interval=20,
        data_pin=None,
        data_pin2=None,
        target_left=True,
        uart_flip=True,
        use_pio=False,
        debug_enabled=False,
    ):
        self._is_target = True
        self._uart_buffer = []
        self.split_flip = split_flip
        self.split_side = split_side
        self.split_type = split_type
        self.split_target_left = split_target_left
        self.split_offset = None
        self.data_pin = data_pin
        self.data_pin2 = data_pin2
        self.target_left = target_left
        self.uart_flip = uart_flip
        self._use_pio = use_pio
        self._uart = None
        self._uart_interval = uart_interval
        self._debug_enabled = debug_enabled
        self.uart_header = bytearray([0xB2])  # Any non-zero byte should work

        if self.split_type == SplitType.BLE:
            try:
                from adafruit_ble import BLERadio
                from adafruit_ble.advertising.standard import (
                    ProvideServicesAdvertisement,
                )
                from adafruit_ble.services.nordic import UARTService

                self.BLERadio = BLERadio
                self.ProvideServicesAdvertisement = ProvideServicesAdvertisement
                self.UARTService = UARTService
            except ImportError:
                print('BLE Import error')
                return  # BLE isn't supported on this platform
            self._ble_last_scan = ticks_ms() - 5000
            self._connection_count = 0
            self._split_connected = False
            self._uart_connection = None
            self._advertisment = None  # Seems to not be used anywhere
            self._advertising = False
            self._psave_enable = False

        if self._use_pio:
            from kmk.transports.pio_uart import PIO_UART

            self.PIO_UART = PIO_UART

    def during_bootup(self, keyboard):
        # Set up name for target side detection and BLE advertisment
        name = str(getmount('/').label)
        if self.split_type == SplitType.BLE:
            if keyboard.hid_type == HIDModes.BLE:
                self._ble = keyboard._hid_helper.ble
            else:
                self._ble = self.BLERadio()
                self._ble.name = name
        else:
            # Try to guess data pins if not supplied
            if not self.data_pin:
                self.data_pin = keyboard.data_pin

        # if split side was given, find master from split_side.
        if self.split_side == SplitSide.LEFT:
            self._is_target = bool(self.split_target_left)
        elif self.split_side == SplitSide.RIGHT:
            self._is_target = not bool(self.split_target_left)
        else:
            # Detect split side from name
            if (
                self.split_type == SplitType.UART
                or self.split_type == SplitType.ONEWIRE
            ):
                self._is_target = runtime.usb_connected
            elif self.split_type == SplitType.BLE:
                self._is_target = name.endswith('L') == self.split_target_left

            if name.endswith('L'):
                self.split_side = SplitSide.LEFT
            elif name.endswith('R'):
                self.split_side = SplitSide.RIGHT

        if not self._is_target:
            keyboard._hid_send_enabled = False

        # Flips the col pins if PCB is the same but flipped on right
        if self.split_flip and self.split_side == SplitSide.RIGHT:
            keyboard.col_pins = list(reversed(keyboard.col_pins))

        self.split_offset = len(keyboard.col_pins)

        if self.split_type == SplitType.UART and self.data_pin is not None:
            if self._is_target or not self.uart_flip:
                if self._use_pio:
                    self._uart = self.PIO_UART(tx=self.data_pin2, rx=self.data_pin)
                else:
                    self._uart = busio.UART(
                        tx=self.data_pin2, rx=self.data_pin, timeout=self._uart_interval
                    )
            else:
                if self._use_pio:
                    self._uart = self.PIO_UART(tx=self.data_pin, rx=self.data_pin2)
                else:
                    self._uart = busio.UART(
                        tx=self.data_pin, rx=self.data_pin2, timeout=self._uart_interval
                    )

        # Attempt to sanely guess a coord_mapping if one is not provided.
        if not keyboard.coord_mapping:
            keyboard.coord_mapping = []

            rows_to_calc = len(keyboard.row_pins) * 2
            cols_to_calc = len(keyboard.col_pins) * 2

            for ridx in range(rows_to_calc):
                for cidx in range(cols_to_calc):
                    keyboard.coord_mapping.append(intify_coordinate(ridx, cidx))

    def before_matrix_scan(self, keyboard):
        if self.split_type == SplitType.BLE:
            self._check_all_connections()
            self._receive_ble(keyboard)
        elif self.split_type == SplitType.UART:
            if self._is_target or self.data_pin2:
                self._receive_uart(keyboard)
        elif self.split_type == SplitType.ONEWIRE:
            pass  # Protocol needs written
        return

    def after_matrix_scan(self, keyboard):
        if keyboard.matrix_update:
            if self.split_type == SplitType.UART and self._is_target:
                pass  # explicit pass just for dev sanity...

            if self.split_type == SplitType.UART and (
                self.data_pin2 or not self._is_target
            ):
                self._send_uart(keyboard.matrix_update)
            elif self.split_type == SplitType.BLE:
                self._send_ble(keyboard.matrix_update)
            elif self.split_type == SplitType.ONEWIRE:
                pass  # Protocol needs written
            else:
                print('Unexpected case in after_matrix_scan')

        return

    def before_hid_send(self, keyboard):
        if not self._is_target:
            keyboard.hid_pending = False

        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        if self.split_type == SplitType.BLE:
            if self._uart_connection and not self._psave_enable:
                self._uart_connection.connection_interval = self._uart_interval
                self._psave_enable = True

    def on_powersave_disable(self, keyboard):
        if self.split_type == SplitType.BLE:
            if self._uart_connection and self._psave_enable:
                self._uart_connection.connection_interval = 11.25
                self._psave_enable = False

    def _check_all_connections(self):
        '''Validates the correct number of BLE connections'''
        self._previous_connection_count = self._connection_count
        self._connection_count = len(self._ble.connections)
        if self._is_target:
            if self._advertising or not self._check_if_split_connected():
                self._target_advertise()
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

    def _send_ble(self, update):
        if self._uart:
            try:
                if not self._is_target:
                    update[1] += self.split_offset
                self._uart.write(update)
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
            while self._uart.in_waiting >= 3:
                self._uart_buffer.append(self._uart.read(3))
            if self._uart_buffer:
                keyboard.secondary_matrix_update = bytearray(self._uart_buffer.pop(0))
                return

    def _checksum(self, update):
        checksum = bytes([sum(update) & 0xFF])

        return checksum

    def _send_uart(self, update):
        # Change offsets depending on where the data is going to match the correct
        # matrix location of the receiever

        if self.split_side == SplitSide.RIGHT:
            # if we're on the right, we by definition are sending to the left, so we need to offset.
            update[1] += self.split_offset

        if self._uart is not None:
            self._uart.write(self.uart_header)
            self._uart.write(update)
            self._uart.write(self._checksum(update))

    def _receive_uart(self, keyboard):
        if self._uart is not None and self._uart.in_waiting > 0 or self._uart_buffer:
            if self._uart.in_waiting >= 60:
                # This is a dirty hack to prevent crashes in unrealistic cases
                import microcontroller

                microcontroller.reset()

            while self._uart.in_waiting >= 5:
                # Check the header
                if self._uart.read(1) == self.uart_header:
                    update = self._uart.read(3)

                    # check the checksum
                    if self._checksum(update) == self._uart.read(1):
                        self._uart_buffer.append(update)

            if self._uart_buffer:
                keyboard.secondary_matrix_update = bytearray(self._uart_buffer.pop(0))

                return
