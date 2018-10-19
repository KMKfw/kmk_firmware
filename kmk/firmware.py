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

import gc
import supervisor
import board
import busio

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

    split_type = None
    split_offsets = ()
    split_flip = True
    split_master_left = True
    uart = None

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
        # if self.split_type is not None and not self.split_master_left:
            # update[1] += self.split_offsets[update[1]]
        print(update[1])

        if update is not None:
            self._state.matrix_changed(
                update[0],
                update[1],
                update[2],
            )

        if self._state.hid_pending:
            self._send_hid()

        for key in self._state.pending_keys:
            self._send_key(key)
            self._state.pending_key_handled()

        if self._state.macro_pending:
            for key in self._state.macro_pending(self):
                self._send_key(key)

            self._state.resolve_macro()

        if self.debug_enabled:
            print('New State: {}'.format(self._state._to_dict()))

    def _send_to_master(self, update):
        if self.split_type == "UART":
            if self.uart is None:
                self.uart = busio.UART(board.TX, board.RX, timeout=1)


            self.uart.write(update)

    def _receive_from_slave(self):
        if self.split_type == "UART":
            if self.uart is None:
                self.uart = busio.UART(board.TX, board.RX, timeout=1)

            if self.uart.in_waiting > 0:
                update = bytearray(self.uart.read())
                if self.split_master_left:
                    update[1] += self.split_offsets[update[0]]
                return update

        return None

    def go(self):
        assert self.keymap, 'must define a keymap with at least one row'
        assert self.row_pins, 'no GPIO pins defined for matrix rows'
        assert self.col_pins, 'no GPIO pins defined for matrix columns'
        assert self.diode_orientation is not None, 'diode orientation must be defined'

        if self.split_flip and not supervisor.runtime.serial_connected:
            self.col_pins = list(reversed(self.col_pins))

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
            if self.split_type is not None and supervisor.runtime.serial_connected:
                update = self._receive_from_slave()
                if update is not None:
                    print(str(update))
                    self._handle_update(update)

            for update in self.matrix.scan_for_changes():
                if update is not None:
                    # Abstract this later. Bluetooth will fail here
                    if supervisor.runtime.serial_connected:
                        print(str(update))
                        self._handle_update(update)

                    else:
                        # This keyboard is a slave, and needs to send data to master
                        self._send_to_master(update)

            gc.collect()
