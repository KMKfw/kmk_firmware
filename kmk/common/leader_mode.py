import logging

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
        if state.leader_mode % 2 == 1:
            for key in state.keys_pressed:
                if key == Keycodes.Common.KC_ENT:
                    # Process the action and remove the extra KC.ENT that was added to get here
                    state = process(state)
                    state.keys_pressed.discard(Keycodes.Common.KC_ENT)
                    return clean_exit(state)
                elif key == Keycodes.Common.KC_ESC:
                    # Clean state and turn leader mode off.
                    return clean_exit(state)
                elif key == Keycodes.KMK.KC_LEAD:
                    return state
                else:
                    # Add key if not needing to escape
                    # This needs replaced later with a proper debounce
                    state.leader_mode_history.append(key)
                    return state.keys_pressed.discard(key)

        return state


def clean_exit(state):
    """
    Cleans up the state and hands the HID control back.
    :param state:
    :return state:
    """
    state.leader_mode_history = []
    state.leader_mode -= 1
    state.keys_pressed.discard(Keycodes.Common.KC_ESC)
    return state


def process(state):
    """
    Checks if there are iny matching sequences of keys, and
    performs the macro specified by the user.
    :param state:
    :param leader_dictionary:
    :return state:
    """
    lmh = tuple(state.leader_mode_history)
    for k, v in state.LEADER_DICTIONARY.items():
        if k == lmh:
            state.macro_pending = v.keydown
    return state
