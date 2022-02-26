'''Enables splitting keyboards wirelessly or wired'''
from micropython import const

from storage import getmount

from kmk.matrix import KeyEvent, intify_coordinate
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
    '''Enables splitting keyboards wirelessly, or wired. Wrapper around other Split modules.'''

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

        if split_type == SplitType.UART:
            if use_pio:
                from kmk.transports.pio_split import PioSplit

                self.protocol = PioSplit(
                    split_flip=split_flip,
                    split_side=split_side,
                    split_target_left=split_target_left,
                    uart_interval=uart_interval,
                    data_pin=data_pin,
                    data_pin2=data_pin2,
                    uart_flip=uart_flip,
                )
            else:
                from kmk.transports.uart_split import UartSplit

                self.protocol = UartSplit(
                    split_flip=split_flip,
                    split_side=split_side,
                    split_target_left=split_target_left,
                    uart_interval=uart_interval,
                    data_pin=data_pin,
                    data_pin2=data_pin2,
                    uart_flip=uart_flip,
                )
        elif split_type == SplitType.BLE:
            from kmk.transports.ble_split import BleSplit

            self.protocol = BleSplit(
                split_flip=split_flip,
                split_side=split_side,
                split_target_left=split_target_left,
                uart_interval=uart_interval,
                debug_enabled=debug_enabled,
            )
        elif split_type == SplitType.I2C:
            raise NotImplementedError
        elif split_type == SplitType.ONEWIRE:
            raise NotImplementedError

    def during_bootup(self, keyboard):
        self.protocol.during_bootup(keyboard)

    def before_matrix_scan(self, keyboard):
        self.protocol.before_matrix_scan(keyboard)

    def after_matrix_scan(self, keyboard):
        self.protocol.after_matrix_scan(keyboard)

    def before_hid_send(self, keyboard):
        self.protocol.before_hid_send(keyboard)

    def after_hid_send(self, keyboard):
        self.protocol.after_hid_send(keyboard)

    def on_powersave_enable(self, keyboard):
        self.protocol.on_powersave_enable(keyboard)

    def on_powersave_disable(self, keyboard):
        self.protocol.on_powersave_disable(keyboard)


class AbstractSplit(Module):
    def __init__(
        self,
        *,
        split_flip=True,
        split_side=None,
        split_target_left=True,
    ):
        self._is_target = True
        self.split_flip = split_flip
        self.split_side = split_side
        self.split_target_left = split_target_left
        self.split_offset = None

        self.UPDATE_SIZE = 2
        # Headers differentiate updates types
        self.MATRIX_HEADER = bytearray([0xB2])

    def during_bootup(self, keyboard):
        self._detect_sides_and_target()

        if not self._is_target:
            keyboard._hid_send_enabled = False

        if self.split_offset is None:
            self.split_offset = len(keyboard.col_pins) * len(keyboard.row_pins)

        self._fill_missing_coord_mapping(keyboard)

        if self.split_side == SplitSide.RIGHT:
            keyboard.matrix.offset = self.split_offset

    def before_matrix_scan(self, keyboard):
        raise NotImplementedError('subclasses must override before_matrix_scan()!')

    def after_matrix_scan(self, keyboard):
        raise NotImplementedError('subclasses must override after_matrix_scan()!')

    def before_hid_send(self, keyboard):
        if not self._is_target:
            keyboard.hid_pending = False

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass

    def _detect_sides_and_target(self):
        # Set up name for target side detection
        name = str(getmount('/').label)

        # if split side was given, find master from split_side.
        if self.split_side == SplitSide.LEFT:
            self._is_target = bool(self.split_target_left)
        elif self.split_side == SplitSide.RIGHT:
            self._is_target = not bool(self.split_target_left)
        else:
            self._is_target = name.endswith('L') == self.split_target_left

            if name.endswith('L'):
                self.split_side = SplitSide.LEFT
            elif name.endswith('R'):
                self.split_side = SplitSide.RIGHT

    def _fill_missing_coord_mapping(self, keyboard):
        # Attempt to sanely guess a coord_mapping if one is not provided.
        if not keyboard.coord_mapping:
            keyboard.coord_mapping = []

            rows_to_calc = len(keyboard.row_pins)
            cols_to_calc = len(keyboard.col_pins)

            # Flips the col order if PCB is the same but flipped on right
            cols_rhs = list(range(cols_to_calc))
            if self.split_flip:
                cols_rhs = list(reversed(cols_rhs))

            for ridx in range(rows_to_calc):
                for cidx in range(cols_to_calc):
                    keyboard.coord_mapping.append(
                        intify_coordinate(ridx, cidx, cols_to_calc)
                    )
                for cidx in cols_rhs:
                    keyboard.coord_mapping.append(
                        intify_coordinate(rows_to_calc + ridx, cidx, cols_to_calc)
                    )

    def _serialize_update(self, update):
        buffer = bytearray(self.UPDATE_SIZE)
        buffer[0] = update.key_number
        buffer[1] = update.pressed
        return buffer

    def _deserialize_update(self, update):
        kevent = KeyEvent(key_number=update[0], pressed=update[1])
        return kevent

    def _checksum(self, update):
        checksum = bytes([sum(update) & 0xFF])
        return checksum
