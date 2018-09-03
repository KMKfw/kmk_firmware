import logging

from kmk.common.event_defs import init_firmware
from kmk.common.internal_state import ReduxStore, kmk_reducer
from kmk.common.keymap import Keymap

try:
    from kmk.circuitpython.matrix import MatrixScanner
except ImportError:
    from kmk.micropython.matrix import MatrixScanner


class Firmware:
    def __init__(
        self, keymap, row_pins, col_pins, diode_orientation,
        log_level=logging.NOTSET,
    ):
        self.cached_state = None
        self.store = ReduxStore(kmk_reducer, log_level=log_level)
        self.store.subscribe(
            lambda state, action: self._subscription(state, action),
        )
        self.store.dispatch(init_firmware(
            keymap=keymap,
            row_pins=row_pins,
            col_pins=col_pins,
            diode_orientation=diode_orientation,
        ))

    def _subscription(self, state, action):
        if self.cached_state is None or self.cached_state.keymap != state.keymap:
            self.keymap = Keymap(state.keymap)

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
            self.keymap.parse(self.matrix.raw_scan(), store=self.store)
