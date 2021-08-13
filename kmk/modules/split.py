'''Enables splitting keyboards wirelessly or wired'''
import busio
from micropython import const

from storage import getmount
from typing import Any, List, Optional, Tuple, Type, Union

from kmk.kmk_keyboard import KMKKeyboard
from kmk.kmktime import ticks_diff, ticks_ms
from kmk.matrix import intify_coordinate
from kmk.modules import Module

UartBuffer = List[Optional[Union[bytes, None]]]


class SplitSide:
    LEFT: int = const(1)
    RIGHT: int = const(2)


class SplitType:
    UART: int = const(1)
    I2C: int = const(2)  # unused
    ONEWIRE: int = const(3)  # unused
    BLE: int = const(4)


class Split(Module):
    '''Enables splitting keyboards wirelessly, or wired'''

    def __init__(
        self,
        split_flip: bool = True,
        split_side: Optional[int] = None,
        split_type: int = SplitType.UART,
        split_target_left: bool = True,
        uart_interval: int = 20,
        data_pin: Optional[Any] = None,
        data_pin2: Optional[Any] = None,
        target_left: bool = True,
        uart_flip: bool = True,
        debug_enabled: bool = False,
    ) -> None:
        self._is_target: bool = True
        self._uart_buffer: UartBuffer = []
        self.split_flip: bool = split_flip
        self.split_side: Optional[int] = split_side
        self.split_type: int = split_type
        self.split_target_left: bool = split_target_left
        self.split_offset: Optional[int] = None
        self.data_pin: Optional[Any] = data_pin
        self.data_pin2: Optional[Any] = data_pin2
        self.target_left: bool = target_left
        self.uart_flip: bool = uart_flip
        self._is_target: bool = True
        self._uart: Optional[busio.UART] = None
        self._uart_interval: int = uart_interval
        self._debug_enabled: bool = debug_enabled
        if self.split_type == SplitType.BLE:
            try:
                from adafruit_ble import BLEConnection, BLERadio
                from adafruit_ble.advertising.standard import (
                    ProvideServicesAdvertisement,
                )
                from adafruit_ble.services.nordic import UARTService

                self.ProvideServicesAdvertisement: Type[
                    ProvideServicesAdvertisement
                ] = ProvideServicesAdvertisement
                self.UARTService: Type[UARTService] = UARTService
            except ImportError:
                print('BLE Import error')
                return  # BLE isn't supported on this platform
            self._ble: BLERadio = BLERadio()
            self._ble_last_scan: float = ticks_ms() - 5000
            self._connection_count: int = 0
            self._uart_connection: Optional[BLEConnection] = None
            self._advertisment: Optional[ProvideServicesAdvertisement] = None
            self._advertising: bool = False
            self._psave_enable: bool = False

    def during_bootup(self, keyboard: KMKKeyboard) -> None:
        # Set up name for target side detection and BLE advertisment
        name: str = str(getmount('/').label)
        if self.split_type == SplitType.BLE:
            self._ble.name = name
        else:
            # Try to guess data pins if not supplied
            if not self.data_pin:
                self.data_pin = keyboard.data_pin

        # Detect split side from name
        if self.split_side is None:
            if name.endswith('L'):
                # If name ends in 'L' assume left and strip from name
                self._is_target = bool(self.split_target_left)
                self.split_side = SplitSide.LEFT
            elif name.endswith('R'):
                # If name ends in 'R' assume right and strip from name
                self._is_target = not bool(self.split_target_left)
                self.split_side = SplitSide.RIGHT

        # if split side was given, find master from split_side.
        elif self.split_side == SplitSide.LEFT:
            self._is_target = bool(self.split_target_left)
        elif self.split_side == SplitSide.RIGHT:
            self._is_target = not bool(self.split_target_left)

        # Flips the col pins if PCB is the same but flipped on right
        if self.split_flip and self.split_side == SplitSide.RIGHT:
            keyboard.col_pins = list(reversed(keyboard.col_pins))

        self.split_offset = len(keyboard.col_pins)

        if self.split_type == SplitType.UART and self.data_pin is not None:
            if self._is_target:
                self._uart = busio.UART(
                    tx=self.data_pin2, rx=self.data_pin, timeout=self._uart_interval
                )
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

    def before_matrix_scan(self, keyboard: KMKKeyboard) -> None:
        if self.split_type == SplitType.BLE:
            self._check_all_connections()
            self._receive_ble(keyboard)
        elif self.split_type == SplitType.UART:
            if self._is_target or self.data_pin2:
                self._receive_uart(keyboard)
        elif self.split_type == SplitType.ONEWIRE:
            pass  # Protocol needs written
        return

    def after_matrix_scan(self, keyboard: KMKKeyboard) -> None:
        if keyboard.matrix_update:
            if self.split_type == SplitType.UART and self._is_target:
                pass  # explicit pass just for dev sanity...
            elif self.split_type == SplitType.UART and (
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

    def before_hid_send(self, keyboard: KMKKeyboard) -> None:
        if not self._is_target:
            keyboard.hid_pending = False

        return

    def after_hid_send(self, keyboard: KMKKeyboard) -> None:
        return

    def on_powersave_enable(self, keyboard: KMKKeyboard) -> None:
        if self.split_type == SplitType.BLE:
            if self._uart_connection and not self._psave_enable:
                self._uart_connection.connection_interval = self._uart_interval
                self._psave_enable = True

    def on_powersave_disable(self, keyboard: KMKKeyboard) -> None:
        if self.split_type == SplitType.BLE:
            if self._uart_connection and self._psave_enable:
                self._uart_connection.connection_interval = 11.25
                self._psave_enable = False

    def _check_all_connections(self) -> None:
        '''Validates the correct number of BLE connections'''
        self._connection_count = len(self._ble.connections)
        if self._is_target and self._connection_count < 2:
            self._target_advertise()
        elif not self._is_target and self._connection_count < 1:
            self._initiator_scan()

    def _initiator_scan(self) -> None:
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

    def _target_advertise(self) -> None:
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

    def ble_rescan_timer(self) -> bool:
        '''If true, the rescan timer is up'''
        return bool(ticks_diff(ticks_ms(), self._ble_last_scan) > 5000)

    def ble_time_reset(self) -> None:
        '''Resets the rescan timer'''
        self._ble_last_scan = ticks_ms()

    def _send_ble(self, update: List) -> None:
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

    def _receive_ble(self, keyboard: KMKKeyboard) -> None:
        if self._uart is not None and self._uart.in_waiting > 0 or self._uart_buffer:
            while self._uart.in_waiting >= 3:
                self._uart_buffer.append(self._uart.read(3))
            if self._uart_buffer:
                keyboard.secondary_matrix_update = bytearray(self._uart_buffer.pop(0))
                return

    def _send_uart(self, update: List) -> None:
        # Change offsets depending on where the data is going to match the correct
        # matrix location of the receiever
        if self._is_target:
            if self.split_target_left:
                update[1] += self.split_offset
            else:
                update[1] -= self.split_offset
        else:
            if self.split_target_left:
                update[1] += self.split_offset
            else:
                update[1] -= self.split_offset

        if self._uart is not None:
            self._uart.write(update)

    def _receive_uart(self, keyboard: KMKKeyboard) -> None:
        if self._uart is not None and self._uart.in_waiting > 0 or self._uart_buffer:
            if self._uart.in_waiting >= 60:
                # This is a dirty hack to prevent crashes in unrealistic cases
                import microcontroller

                microcontroller.reset()

            while self._uart.in_waiting >= 3:
                self._uart_buffer.append(self._uart.read(3))
            if self._uart_buffer:
                keyboard.secondary_matrix_update = bytearray(self._uart_buffer.pop(0))

                return
