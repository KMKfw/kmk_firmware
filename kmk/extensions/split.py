import busio
import gc

from kmk.extensions import Extension
from kmk.kmktime import sleep_ms
from kmk.matrix import intify_coordinate


class SplitType:
    UART = 1
    I2C = 2  # unused
    ONEWIRE = 3  # unused
    BLE = 4  # unused


class Split(Extension):
    def __init__(
        self,
        extra_data_pin=None,
        offsets=(),
        flip=False,
        side=None,
        stype=None,
        master_left=True,
        uart_flip=True,
        uart_pin=None,
        uart_timeout=20,
    ):
        self.extra_data_pin = extra_data_pin
        self.split_offsets = offsets
        self.split_flip = flip
        self.split_side = side
        self.split_type = stype
        self.split_master_left = master_left
        self._uart = None
        self.uart_flip = uart_flip
        self.uart_pin = uart_pin
        self.uart_timeout = uart_timeout

    def during_bootup(self, keyboard):
        if self.split_type is not None:
            try:
                # Working around https://github.com/adafruit/circuitpython/issues/1769
                keyboard._hid_helper_inst.create_report([]).send()
                self._is_master = True

                # Sleep 2s so master portion doesn't "appear" to boot quicker than
                # dependent portions (which will take ~2s to time out on the HID send)
                sleep_ms(2000)
            except OSError:
                self._is_master = False

            if self.split_flip and not self._is_master:
                keyboard.col_pins = list(reversed(self.col_pins))
            if self.split_side == 'Left':
                self.split_master_left = self._is_master
            elif self.split_side == 'Right':
                self.split_master_left = not self._is_master
        else:
            self._is_master = True

        if self.uart_pin is not None:
            if self._is_master:
                self._uart = busio.UART(
                    tx=None, rx=self.uart_pin, timeout=self.uart_timeout
                )
            else:
                self._uart = busio.UART(
                    tx=self.uart_pin, rx=None, timeout=self.uart_timeout
                )

        # Attempt to sanely guess a coord_mapping if one is not provided.
        if not keyboard.coord_mapping:
            keyboard.coord_mapping = []

            rows_to_calc = len(keyboard.row_pins)
            cols_to_calc = len(keyboard.col_pins)

            if self.split_offsets:
                rows_to_calc *= 2
                cols_to_calc *= 2

            for ridx in range(rows_to_calc):
                for cidx in range(cols_to_calc):
                    keyboard.coord_mapping.append(intify_coordinate(ridx, cidx))

        gc.collect()

    def before_matrix_scan(self, keyboard_state):
        if self.split_type is not None and self._is_master:
            return self._receive_from_slave()

    def after_matrix_scan(self, keyboard_state, matrix_update):
        if matrix_update is not None and not self._is_master:
            self._send_to_master(matrix_update)

    def _send_to_master(self, update):
        if self.split_master_left:
            update[1] += self.split_offsets[update[0]]
        else:
            update[1] -= self.split_offsets[update[0]]
        if self._uart is not None:
            self._uart.write(update)
