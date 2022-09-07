'''Enables splitting keyboards wirelessly or wired'''
from micropython import const
from supervisor import runtime

from keypad import Event as KeyEvent
from storage import getmount

from kmk.modules import Module


class SplitSide:
    LEFT = const(1)
    RIGHT = const(2)


class SplitType:
    UART = const(1)
    I2C = const(2)  # unused
    ONEWIRE = const(3)  # unused
    BLE = const(4)
    PIO_UART = const(5)


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
        self.uart_flip = uart_flip
        self._use_pio = use_pio
        self._transport = None
        self._uart_interval = uart_interval
        self._debug_enabled = debug_enabled
        self.uart_header = bytearray([0xB2])  # Any non-zero byte should work

        if split_type == SplitType.UART and use_pio:
            split_type = SplitType.PIO_UART

        if split_type == SplitType.UART:
            import busio
        elif split_type == SplitType.PIO_UART:
            from kmk.transports.pio_uart import PIO_UART
        elif split_type == SplitType.BLE:
            from kmk.transports.ble import BLE_UART

    def during_bootup(self, keyboard):
        # Set up name for target side detection and BLE advertisment
        if not self.data_pin:
            self.data_pin = keyboard.data_pin

        self._get_side()

        if not self._is_target:
            keyboard._hid_send_enabled = False

        if self.split_offset is None:
            self.split_offset = keyboard.matrix[-1].coord_mapping[-1] + 1

        self._init_transport(keyboard)

        # Attempt to sanely guess a coord_mapping if one is not provided.
        if not keyboard.coord_mapping:
            self._guess_coord_mapping()

        if self.split_side == SplitSide.RIGHT:
            offset = self.split_offset
            for matrix in keyboard.matrix:
                matrix.offset = offset
                offset += matrix.key_count

    def before_matrix_scan(self, keyboard):
        if self.split_type == SplitType.BLE:
            self._transport.check_connection(keyboard)

        if self.split_type == SplitType.UART:
            if self._is_target or self.data_pin2:
                self._receive_uart(keyboard)
        else:
            self._receive_uart(keyboard)

    def after_matrix_scan(self, keyboard):
        if keyboard.matrix_update:
            if self.split_type == SplitType.UART:
                if not self._is_target or self.data_pin2:
                    self._send_uart(keyboard.matrix_update)
                else:
                    pass  # explicit pass just for dev sanity...
            else:
                self._send_uart(keyboard.matrix_update)

    def before_hid_send(self, keyboard):
        if not self._is_target:
            keyboard.hid_pending = False

        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        if self.split_type == SplitType.BLE:
            self._transport.enable_powersave(True)

    def on_powersave_disable(self, keyboard):
        if self.split_type == SplitType.BLE:
            self._transport.enable_powersave(False)

    def _serialize_update(self, update):
        buffer = bytearray(2)
        buffer[0] = update.key_number
        buffer[1] = update.pressed
        return buffer

    def _deserialize_update(self, update):
        kevent = KeyEvent(key_number=update[0], pressed=update[1])
        return kevent

    def _checksum(self, update):
        checksum = bytes([sum(update) & 0xFF])

        return checksum

    def _send_uart(self, update):
        # Change offsets depending on where the data is going to match the correct
        # matrix location of the receiever
        update = self._serialize_update(update)
        self._transport.write(self.uart_header)
        self._transport.write(update)
        self._transport.write(self._checksum(update))

    def _receive_uart(self, keyboard):
        if self._transport.in_waiting > 0 or self._uart_buffer:
            if self._transport.in_waiting >= 60:
                # This is a dirty hack to prevent crashes in unrealistic cases
                import microcontroller

                microcontroller.reset()

            while self._transport.in_waiting >= 4:
                # Check the header
                if self._transport.read(1) == self.uart_header:
                    update = self._transport.read(2)

                    # check the checksum
                    if self._checksum(update) == self._transport.read(1):
                        self._uart_buffer.append(self._deserialize_update(update))
            if self._uart_buffer:
                keyboard.secondary_matrix_update = self._uart_buffer.pop(0)

    def _get_side(self):
        name = str(getmount('/').label)
        # if split side was given, find target from split_side.
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

            if name.endswith('L'):
                self.split_side = SplitSide.LEFT
            elif name.endswith('R'):
                self.split_side = SplitSide.RIGHT

    def _init_transport(self, keyboard):
        if self._is_target or not self.uart_flip:
            tx_pin = self.data_pin2
            rx_pin = self.data_pin
        else:
            tx_pin = self.data_pin
            rx_pin = self.data_pin2

        if split_type == SplitType.UART:
            self._transport = busio.UART(tx=tx_pin, rx=rx_pin, timeout=self._uart_interval)
        elif split_type == SplitType.PIO_UART:
            self._transport = PIO_UART(tx=tx_pin, rx=rx_pin)
        elif split_type == SplitType.BLE:
            self._transport = BLE_UART(self._is_target, uart_interval)
        else:
            raise NotImplementedError

    def _guess_coord_mapping(self, keyboard):
        cm = []

        rows_to_calc = len(keyboard.row_pins)
        cols_to_calc = len(keyboard.col_pins)

        # Flips the col order if PCB is the same but flipped on right
        cols_rhs = list(range(cols_to_calc))
        if self.split_flip:
            cols_rhs = list(reversed(cols_rhs))

        for ridx in range(rows_to_calc):
            for cidx in range(cols_to_calc):
                cm.append(cols_to_calc * ridx + cidx)
            for cidx in cols_rhs:
                cm.append(cols_to_calc * (rows_to_calc + ridx) + cidx)

        keyboard.coord_mapping = tuple(cm)
