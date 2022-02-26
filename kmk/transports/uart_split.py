import busio
from supervisor import runtime

from storage import getmount

from kmk.modules.split import AbstractSplit, SplitSide


class UartSplit(AbstractSplit):
    '''Enables splitting wired keyboards'''

    def __init__(
        self,
        *,
        split_flip=True,
        split_side=None,
        split_target_left=True,
        uart_interval=20,
        data_pin=None,
        data_pin2=None,
        uart_flip=True,
    ):
        super().__init__(
            split_flip=split_flip,
            split_side=split_side,
            split_target_left=split_target_left,
        )
        self._uart_interval = uart_interval
        self.data_pin = data_pin
        self.data_pin2 = data_pin2
        self.uart_flip = uart_flip

        self._uart = None
        self._uart_buffer = []

    def during_bootup(self, keyboard):
        super().during_bootup(keyboard)

        # Fallback to default data pin in keyboard config
        if not self.data_pin:
            self.data_pin = keyboard.data_pin

        if self.data_pin is None:
            raise Exception('UART Split requires data_pin argument')

        # Init the protocol
        if self._is_target or not self.uart_flip:
            self._uart = busio.UART(
                tx=self.data_pin2, rx=self.data_pin, timeout=self._uart_interval
            )
        else:
            self._uart = busio.UART(
                tx=self.data_pin, rx=self.data_pin2, timeout=self._uart_interval
            )

    def before_matrix_scan(self, keyboard):
        if self._is_target or self.data_pin2:
            self._receive_uart(keyboard)

    def after_matrix_scan(self, keyboard):
        if keyboard.matrix_update and (self.data_pin2 or not self._is_target):
            self._send_uart(keyboard.matrix_update)

    def _detect_sides_and_target(self):
        name = str(getmount('/').label)

        if self.split_side is None:
            self._is_target = runtime.usb_connected
            if name.endswith('L'):
                self.split_side = SplitSide.LEFT
            elif name.endswith('R'):
                self.split_side = SplitSide.RIGHT
        else:
            super()._detect_sides_and_target()

    def _send_uart(self, update):
        # Change offsets depending on where the data is going to match the correct
        # matrix location of the receiver
        if self._uart is not None:
            update = self._serialize_update(update)
            self._uart.write(self.MATRIX_HEADER)
            self._uart.write(update)
            self._uart.write(self._checksum(update))

    def _receive_uart(self, keyboard):
        if self._uart is not None and self._uart.in_waiting > 0 or self._uart_buffer:
            if self._uart.in_waiting >= 60:
                # This is a dirty hack to prevent crashes in unrealistic cases
                import microcontroller

                microcontroller.reset()

            while self._uart.in_waiting >= self.UPDATE_SIZE + 2:
                # Check the header
                if self._uart.read(1) == self.MATRIX_HEADER:
                    update = self._uart.read(self.UPDATE_SIZE)

                    # check the checksum
                    if self._checksum(update) == self._uart.read(1):
                        self._uart_buffer.append(self._deserialize_update(update))
            if self._uart_buffer:
                keyboard.secondary_matrix_update = self._uart_buffer.pop(0)
