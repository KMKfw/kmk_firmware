class UART:
    def __init__(self, tx=None, rx=None, is_target=True, uart_interval=20):
        self._debug_enabled = True
        self._uart_connection = None
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

    def powersave(enable: bool):
        return

    def write(self, buffer, update):
        if self._uart is not None:
            if not self._is_target or self.data_pin2:
                update = self._serialize_update(update)
                self._uart.write(self.uart_header)
                self._uart.write(update)
                self._uart.write(self._checksum(update))

    def receive(self, keyboard):
        if self._transport.in_waiting > 0 or self._uart_buffer:
            if self._transport.in_waiting >= 60:
                # This is a dirty hack to prevent crashes in unrealistic cases
                # TODO See if this hack is needed with checksum, and if not, use
                # that to fix it.
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
                return self._uart_buffer.pop(0)

        return None
