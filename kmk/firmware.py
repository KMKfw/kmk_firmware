import logging

from kmk.event_defs import init_firmware
from kmk.internal_state import Store, kmk_reducer
from kmk.leader_mode import LeaderHelper


class Firmware:
    def __init__(
        self, keymap, row_pins, col_pins,
            diode_orientation,
            hid=None,
            log_level=logging.NOTSET,
            matrix_scanner=None,
    ):
        assert matrix_scanner is not None
        self.matrix_scanner = matrix_scanner

        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)

        import kmk_keyboard_user
        self.encoders = getattr(kmk_keyboard_user, 'encoders', [])

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

        self.leader_helper = LeaderHelper(store=self.store, log_level=log_level)

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

            if update:
                self.store.dispatch(update)

            for encoder in self.encoders:
                eupdate = encoder.scan()

                if eupdate:
                    for event in eupdate:
                        self.store.dispatch(event)
