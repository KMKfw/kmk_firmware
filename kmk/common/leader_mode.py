import logging

from kmk.common.event_defs import PROCESS_LEADER_EVENT
from kmk.common.keycodes import FIRST_KMK_INTERNAL_KEYCODE, Keycodes

CANCEL_TRIGGERS = {
    Keycodes.KMK.KC_GESC, Keycodes.Common.KC_ESC,
    Keycodes.KMK.KC_LEAD,
}


class LeaderHelper:
    def __init__(self, store, log_level=logging.NOTSET):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        self.store = store
        self.store.subscribe(
            lambda state, action: self._subscription(state, action),
        )

    def _subscription(self, state, action):
        if state.leader_mode:
            for key in state.keys_pressed:
                if key.code >= FIRST_KMK_INTERNAL_KEYCODE:
                    continue
                else:
                    if key.code is Keycodes.Common.KC_ENT.code and \
                            state.leader_mode_enter:
                        # DO THE THING then give control back
                        return self.process(state)
                    elif key.code in CANCEL_TRIGGERS:
                        # Clean state and turn leader mode off.
                        return self.clean_exit(state)
                    else:
                        # Add key if not needing to escape
                        state = state.leader_mode_history.append(key)

        if action.type == PROCESS_LEADER_EVENT:
            self.process(state)

        return state

    def clean_exit(self, state):
        state.leader_mode_history = []
        state.hid_pending = True
        state.leader_mode = False
        state.start_time['leader'] = None
        return state

    def process(self, state):
        # DO THE THING
        return self.clean_exit(self)
