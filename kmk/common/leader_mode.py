import logging

from kmk.common.event_defs import PROCESS_LEADER_EVENT
from kmk.common.keycodes import Keycodes


class LeaderHelper:
    """
        Acts as a hid to absorb keypress, and perform macros when a timer
        or enter key is pressed depending on the mode set.
    """
    def __init__(self, store, log_level=logging.NOTSET):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        self.store = store
        self.store.subscribe(
            lambda state, action: self._subscription(state, action),
        )

    def _subscription(self, state, action):
        """
        Subscribes to the state machine, and dispatches actions based
        based on incoming keypresses, or when a timer runs out depending
        on the mode.
        :param state:
        :param action:
        :return state:
        """
        try:
            from kmk_keyboard_user import LEADER_DICTIONARY
        except ImportError:
            LEADER_DICTIONARY = {}

        if action.type == PROCESS_LEADER_EVENT:
            state = self.process(state, LEADER_DICTIONARY)
            return self.clean_exit(state)

        if state.leader_mode:
            for key in state.keys_pressed:
                if key.code is Keycodes.Common.KC_ENT.code and \
                        state.leader_mode_enter:
                    # Process the action and remove the extra KC.ENT that was added to get here
                    state = self.process(state, LEADER_DICTIONARY)
                    state.keys_pressed.discard(Keycodes.Common.KC_ENT)
                    return self.clean_exit(state)
                elif key.code == Keycodes.Common.KC_ESC:
                    # Clean state and turn leader mode off.
                    state.keys_pressed.discard(Keycodes.Common.KC_ESC)
                    return self.clean_exit(state)
                else:
                    # Add key if not needing to escape
                    return state.leader_mode_history.append(key)

        return state

    def clean_exit(self, state):
        """
        Cleans up the state and hands the HID control back.
        :param state:
        :return state:
        """
        state.leader_mode_history = []
        if not state.macro_pending:
            state.hid_pending = True
        state.leader_mode = False
        if 'leader' in state.start_time:
            state.start_time['leader'] = None
        return state

    def process(self, state, leader_dictionary):
        """
        Checks if there are iny matching sequences of keys, and
        performs the macro specified by the user.
        :param state:
        :param leader_dictionary:
        :return state:
        """
        lmh = tuple(state.leader_mode_history)
        for k, v in leader_dictionary.items():
            if k == lmh:
                state.hid_pending = True
                state.macro_pending = v.keydown
                state.hid_pending = False
        return state
