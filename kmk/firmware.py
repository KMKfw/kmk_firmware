import logging

from kmk.common.event_defs import init_firmware
from kmk.common.internal_state import ReduxStore, kmk_reducer

try:
    from kmk.circuitpython.matrix import MatrixScanner
except ImportError:
    from kmk.micropython.matrix import MatrixScanner


class Firmware:
    def __init__(
        self, keymap, row_pins, col_pins,
        diode_orientation, unicode_mode=None,
        hid=None, log_level=logging.NOTSET,
    ):
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)

        self.cached_state = None
        self.store = ReduxStore(kmk_reducer, log_level=log_level)
        self.store.subscribe(
            lambda state, action: self._subscription(state, action),
        )

        if not hid:
            logger.warning(
                "Must provide a HIDHelper (arg: hid), disabling HID\n"
                "Board will run in debug mode",
            )

        self.hid = hid(store=self.store, log_level=log_level)

        self.store.dispatch(init_firmware(
            keymap=keymap,
            row_pins=row_pins,
            col_pins=col_pins,
            diode_orientation=diode_orientation,
            unicode_mode=unicode_mode,
        ))

    def _subscription(self, state, action):
        if self.cached_state is None or any(
            getattr(self.cached_state, k) != getattr(state, k)
            for k in state.__dict__.keys()
        ):
            self.matrix = MatrixScanner(
                state.col_pins,
                state.row_pins,
                state.diode_orientation,
            )

    def go(self):
        while True:
            state = self.store.get_state()
            update = self.matrix.scan_for_changes(state.matrix)

            if update:
                self.store.dispatch(update)
