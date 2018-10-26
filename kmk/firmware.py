# Welcome to RAM and stack size hacks central, I'm your host, klardotsh!
# We really get stuck between a rock and a hard place on CircuitPython
# sometimes: our import structure is deeply nested enough that stuff
# breaks in some truly bizarre ways, including:
# - explicit RuntimeError exceptions, complaining that our
#   stack depth is too deep
#
# - silent hard locks of the device (basically unrecoverable without
#   UF2 flash if done in main.py, fixable with a reboot if done
#   in REPL)
#
# However, there's a hackaround that works for us! Because sys.modules
# caches everything it sees (and future imports will use that cached
# copy of the module), let's take this opportunity _way_ up the import
# chain to import _every single thing_ KMK eventually uses in a normal
# workflow, in order from fewest to least nested dependencies.

# First, stuff that has no dependencies, or only C/MPY deps
import collections  # isort:skip
import kmk.consts  # isort:skip
import kmk.kmktime  # isort:skip
import kmk.types  # isort:skip

# Now stuff that depends on the above (and so on)
import kmk.keycodes  # isort:skip
import kmk.matrix  # isort:skip

import kmk.hid  # isort:skip
import kmk.internal_state  # isort:skip

# GC runs automatically after CircuitPython imports. If we ever go back to
# supporting MicroPython, we'll need a GC here (and probably after each
# chunk of the above)

# Thanks for sticking around. Now let's do real work, starting below

import busio
import gc

import supervisor
from kmk.consts import LeaderMode, UnicodeModes
from kmk.hid import USB_HID
from kmk.internal_state import InternalState
from kmk.matrix import MatrixScanner


class Firmware:
    debug_enabled = False

    keymap = None

    row_pins = None
    col_pins = None
    diode_orientation = None

    unicode_mode = UnicodeModes.NOOP
    tap_time = 300
    leader_mode = LeaderMode.TIMEOUT
    leader_dictionary = {}
    leader_timeout = 1000

    hid_helper = USB_HID

    split_offsets = ()
    split_flip = False
    split_side = None
    split_master_left = True
    is_master = None
    uart = None
    uart_flip = True

    def __init__(self):
        self._state = InternalState(self)

    def _send_hid(self):
        self._hid_helper_inst.create_report(self._state.keys_pressed).send()
        self._state.resolve_hid()

    def _send_key(self, key):
        if not getattr(key, 'no_press', None):
            self._state.force_keycode_down(key)
            self._send_hid()

        if not getattr(key, 'no_release', None):
            self._state.force_keycode_up(key)
            self._send_hid()

    def _handle_update(self, update):
        '''
        Bulk processing of update code for each cycle
        :param update:
        '''
        if update is not None:
            self._state.matrix_changed(
                update[0],
                update[1],
                update[2],
            )

            if self._state.hid_pending:
                self._send_hid()

            if self.debug_enabled:
                print('New State: {}'.format(self._state._to_dict()))

        self._state.process_timeouts()

        for key in self._state.pending_keys:
            self._send_key(key)
            self._state.pending_key_handled()

        if self._state.macro_pending:
            for key in self._state.macro_pending(self):
                self._send_key(key)

            self._state.resolve_macro()

    def _send_to_master(self, update):
        if self.split_master_left:
            update[1] += self.split_offsets[update[0]]
        else:
            update[1] -= self.split_offsets[update[0]]
        if self.uart is not None:
            self.uart.write(update)

    def _receive_from_slave(self):
        if self.uart is not None and self.uart.in_waiting > 0:
            update = bytearray(self.uart.read(3))
            # Built in debug mode switch
            if update == b'DEB':
                # TODO Pretty up output
                print(self.uart.readline())
                return None
            return update

        return None

    def _send_debug(self, message):
        '''
        Prepends DEB and appends a newline to allow debug messages to
        be detected and handled differently than typical keypresses.
        :param message: Debug message
        '''
        if self.uart is not None:
            self.uart.write('DEB')
            self.uart.write(message, '\n')

    def _master_half(self):
        return supervisor.runtime.serial_connected

    def init_uart(self, tx=None, rx=None, timeout=20):
        if self._master_half():
            # If running with one wire, only receive on master
            if rx is None or self.uart_flip:
                return busio.UART(tx=rx, rx=None, timeout=timeout)
            else:
                return busio.UART(tx=tx, rx=rx, timeout=timeout)

        else:
            return busio.UART(tx=tx, rx=rx, timeout=timeout)

    def go(self):
        assert self.keymap, 'must define a keymap with at least one row'
        assert self.row_pins, 'no GPIO pins defined for matrix rows'
        assert self.col_pins, 'no GPIO pins defined for matrix columns'
        assert self.diode_orientation is not None, 'diode orientation must be defined'

        self.is_master == self._master_half()

        if self.split_flip and not self._master_half():
            self.col_pins = list(reversed(self.col_pins))

        if self.split_side == "Left":
                self.split_master_left = self.is_master
        elif self.split_side == "Right":
            self.split_master_left = not self.is_master

        self.matrix = MatrixScanner(
            cols=self.col_pins,
            rows=self.row_pins,
            diode_orientation=self.diode_orientation,
            rollover_cols_every_rows=getattr(self, 'rollover_cols_every_rows', None),
            swap_indicies=getattr(self, 'swap_indicies', None),
        )

        self._hid_helper_inst = self.hid_helper()

        if self.debug_enabled:
            print("Firin' lazers. Keyboard is booted.")

        while True:
            if self.split_type is not None and self._master_half:
                update = self._receive_from_slave()
                if update is not None:
                    self._handle_update(update)

            update = self.matrix.scan_for_changes()

            if update is not None:
                if self._master_half():
                    self._handle_update(update)

                else:
                    # This keyboard is a slave, and needs to send data to master
                    self._send_to_master(update)

            gc.collect()
