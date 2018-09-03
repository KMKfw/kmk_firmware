import logging

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
        self.raw_keymap = keymap
        self.keymap = Keymap(keymap)
        self.matrix = MatrixScanner(col_pins, row_pins, diode_orientation)
        self.store = ReduxStore(kmk_reducer, log_level=log_level)

    def go(self):
        while True:
            self.keymap.parse(self.matrix.raw_scan(), store=self.store)
