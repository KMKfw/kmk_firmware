import logging

from kmk.common.event_defs import KEY_DOWN_EVENT, KEY_UP_EVENT
from kmk.common.keycodes import Keycodes
from kmk.common.keycodes import (FIRST_KMK_INTERNAL_KEYCODE)


class LeaderHelper:
    def __init__(self, store, log_level=logging.NOTSET):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        self.store = store
        self.store.subscribe(
            lambda state, action: self._subscription(state, action),
        )

    def _subscription(self, state, action):
        if action.type == KEY_DOWN_EVENT and state.leader_mode:
            for key in state.keys_pressed:
                if key.code >= FIRST_KMK_INTERNAL_KEYCODE:
                    continue
                else:
                    if key.code is Keycodes.Common.KC_ENT.code and \
                            state.leader_mode_enter:
                        # DO THE THING then give control back
                        state.leader_mode_history = []
                        state.hid_pending = True
                        state.leader_mode = False
                    elif key.code is Keycodes.KMK.KC_LEAD.code:
                        # Clean state and turn leader mode off.
                        state.leader_mode_history = []
                        state.hid_pending = True
                        state.leader_mode = False
                    else:
                        # Add key if not needing to escape
                        state.leader_mode_history.append(key)

