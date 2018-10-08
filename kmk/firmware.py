import logging

from kmk.common.consts import LeaderMode
from kmk.common.event_defs import init_firmware, process_leader
from kmk.common.internal_state import Store, kmk_reducer
from kmk.common.kmktime import ticks_diff, ticks_ms


class Firmware:
    def __init__(
        self, keymap, row_pins, col_pins,
            diode_orientation, unicode_mode=None,
            hid=None, leader_helper=None,
            log_level=logging.NOTSET,
            matrix_scanner=None,
    ):
        assert matrix_scanner is not None
        self.matrix_scanner = matrix_scanner

        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)

        self.hydrated = False

        self.store = Store(kmk_reducer, log_level=log_level)
        self.store.subscribe(
            lambda state, action: self._subscription(state, action),
        )

        if hid:
            self.hid = hid(store=self.store, log_level=log_level)
        else:
            logger.warning(
                "Must provide a HIDHelper (arg: hid), disabling HID\n"
                "Board will run in debug mode",
            )

        self.leader_helper = leader_helper(store=self.store, log_level=log_level)

        self.store.dispatch(init_firmware(
            keymap=keymap,
            row_pins=row_pins,
            col_pins=col_pins,
            diode_orientation=diode_orientation,
        ))

    def _subscription(self, state, action):
        if not self.hydrated:
            self.matrix = self.matrix_scanner(
                state.col_pins,
                state.row_pins,
                state.diode_orientation,
            )
            self.hydrated = True

    def go(self):
        while True:
            update = self.matrix.scan_for_pressed()
            if self.store.state.leader_mode == LeaderMode.Default_Active:
                if ticks_diff(ticks_ms(), self.store.state.start_time['leader']) >=\
                        self.store.state.leader_timeout:
                    # This MUST be done here as the rest of the system hangs
                    # waiting for matrix updates Fire an event that triggers leader
                    self.store.dispatch(process_leader())

            if update:
                self.store.dispatch(update)
