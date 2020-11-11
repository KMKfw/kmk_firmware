import busio

from kmk.extensions import Extension
from kmk.matrix import intify_coordinate
from storage import getmount


class SplitType:
    UART = 1
    I2C = 2  # unused
    ONEWIRE = 3  # unused


class Split(Extension):
    def __init__(
        self,
        is_target=True,
        extra_data_pin=None,
        split_offset=None,
        split_flip=True,
        split_side=None,
        split_type=SplitType.UART,
        target_left=True,
        uart_flip=True,
        uart_pin=None,
        uart_pin2=None,
        uart_timeout=20,
    ):
        self._is_target = is_target
        self.extra_data_pin = extra_data_pin
        self.split_offsets = split_offset
        self.split_flip = split_flip
        self.split_side = split_side
        self.split_type = split_type
        self.split_target_left = target_left
        self._uart = None
        self._uart_buffer = []
        self.uart_flip = uart_flip
        self.uart_pin = uart_pin
        self.uart_pin2 = uart_pin2
        self.uart_timeout = uart_timeout

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        try:
            # Working around https://github.com/adafruit/circuitpython/issues/1769
            keyboard._hid_helper_inst.create_report([]).send()
            # Line above is broken and needs fixed for aut detection
            self._is_target = True
        except OSError:
            self._is_target = False
        if self.split_side is None:
            l_or_r = str(getmount('/').label)
            if l_or_r.endswith('L'):
                # If name ends in 'L' assume left and strip from name
                self.split_side = 0
            elif l_or_r.endswith('R'):
                # If name ends in 'R' assume right and strip from name
                self.split_side = 1

        if self.split_flip and not self._is_target:
            keyboard.col_pins = list(reversed(keyboard.col_pins))
        if self.split_side == 0:
            self.split_target_left = self._is_target
        elif self.split_side == 1:
            self.split_target_left = not self._is_target

        if self.uart_pin is not None:
            if self._is_target:
                self._uart = busio.UART(
                    tx=self.uart_pin2, rx=self.uart_pin, timeout=self.uart_timeout
                )
            else:
                self._uart = busio.UART(
                    tx=self.uart_pin, rx=self.uart_pin2, timeout=self.uart_timeout
                )
        # Attempt to sanely guess a coord_mapping if one is not provided.
        if not keyboard.coord_mapping:
            keyboard.coord_mapping = []

            self.split_offset = len(keyboard.col_pins)

            rows_to_calc = len(keyboard.row_pins) * 2
            cols_to_calc = len(keyboard.col_pins) * 2

            for ridx in range(rows_to_calc):
                for cidx in range(cols_to_calc):
                    keyboard.coord_mapping.append(intify_coordinate(ridx, cidx))

    def before_matrix_scan(self, keyboard):
        if self._is_target or self.uart_pin2:
            return self._receive()
        return None

    def after_matrix_scan(self, keyboard, matrix_update):
        if matrix_update is not None and not self._is_target:
            self._send(matrix_update)

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def _send(self, update):
        if self.split_target_left:
            update[1] += self.split_offset
        else:
            update[1] -= self.split_offsets
        if self._uart is not None:
            self._uart.write(update)

    def _receive(self):
        if self._uart is not None and self._uart.in_waiting > 0 or self._uart_buffer:
            if self._uart.in_waiting >= 60:
                # This is a dirty hack to prevent crashes in unrealistic cases
                import microcontroller

                microcontroller.reset()

            while self._uart.in_waiting >= 3:
                self._uart_buffer.append(self._uart.read(3))
            if self._uart_buffer:
                update = bytearray(self._uart_buffer.pop(0))

                return update

        return None
