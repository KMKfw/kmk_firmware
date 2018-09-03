import logging

from kmk.common.event_defs import KEY_DOWN_EVENT, KEY_UP_EVENT


class ReduxStore:
    def __init__(self, reducer, log_level=logging.NOTSET):
        self.reducer = reducer
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.state = self.reducer(logger=self.logger)

    def dispatch(self, action):
        self.logger.debug('Dispatching action: {}'.format(action))
        self.state = self.reducer(self.state, action)
        self.logger.debug('Dispatching complete: {}'.format(action))

    def get_state(self):
        return self.state


class InternalState:
    modifiers_pressed = frozenset()
    keys_pressed = frozenset()

    def __repr__(self):
        return 'InternalState(mods={}, keys={})'.format(
            self.modifiers_pressed,
            self.keys_pressed,
        )

    def copy(self, modifiers_pressed=None, keys_pressed=None):
        new_state = InternalState()

        if modifiers_pressed is None:
            new_state.modifiers_pressed = self.modifiers_pressed.copy()
        else:
            new_state.modifiers_pressed = modifiers_pressed

        if keys_pressed is None:
            new_state.keys_pressed = self.keys_pressed.copy()
        else:
            new_state.keys_pressed = keys_pressed

        return new_state


def kmk_reducer(state=None, action=None, logger=None):
    if state is None:
        state = InternalState()

        if logger is not None:
            logger.debug('Reducer received state of None, creating new')

    if action is None:
        if logger is not None:
            logger.debug('No action received, returning state unmodified')

        return state

    if action['type'] == KEY_UP_EVENT:
        return state.copy(keys_pressed=frozenset(
            key for key in state.keys_pressed if key != action['keycode']
        ))

    if action['type'] == KEY_DOWN_EVENT:
        return state.copy(keys_pressed=(
            state.keys_pressed | {action['keycode']}
        ))
