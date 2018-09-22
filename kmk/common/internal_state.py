import logging
import sys

from kmk.common.consts import DiodeOrientation
from kmk.common.event_defs import (INIT_FIRMWARE_EVENT, KEY_DOWN_EVENT,
                                   KEY_UP_EVENT)
from kmk.common.internal_keycodes import process as process_internal


class ReduxStore:
    def __init__(self, reducer, log_level=logging.NOTSET):
        self.reducer = reducer
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.state = self.reducer(logger=self.logger)
        self.callbacks = []

    def dispatch(self, action):
        self.logger.debug('Dispatching action: {}'.format(action))
        self.state = self.reducer(self.state, action)
        self.logger.debug('Dispatching complete: {}'.format(action))

        self.logger.debug('New state: {}'.format(self.state))

        for cb in self.callbacks:
            if cb is not None:
                try:
                    cb(self.state, action)
                except Exception as e:
                    self.logger.error('Callback failed, moving on')
                    print(sys.print_exception(e), file=sys.stderr)

    def get_state(self):
        return self.state

    def subscribe(self, callback):
        self.callbacks.append(callback)
        return len(self.callbacks) - 1

    def unsubscribe(self, idx):
        self.callbacks[idx] = None


class InternalState:
    modifiers_pressed = frozenset()
    keys_pressed = frozenset()
    keymap = []
    row_pins = []
    col_pins = []
    matrix = []
    diode_orientation = DiodeOrientation.COLUMNS
    active_layers = [0]
    _oldstates = []

    def __init__(self, preserve_intermediate_states=False):
        self.preserve_intermediate_states = preserve_intermediate_states

    def to_dict(self, verbose=False):
        ret = {
            'keys_pressed': self.keys_pressed,
            'modifiers_pressed': self.modifiers_pressed,
            'active_layers': self.active_layers,
        }

        if verbose:
            ret.update({
                'keymap': self.keymap,
                'matrix': self.matrix,
                'col_pins': self.col_pins,
                'row_pins': self.row_pins,
                'diode_orientation': self.diode_orientation,
            })

        return ret

    def __repr__(self):
        return 'InternalState({})'.format(self.to_dict())

    def update(self, **kwargs):
        if self.preserve_intermediate_states:
            self._oldstates.append(repr(self.to_dict(verbose=True)))

        for k, v in kwargs.items():
            setattr(self, k, v)

        return self


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
        newstate = state.update(
            keys_pressed=frozenset(
                key for key in state.keys_pressed if key != action['keycode']
            ),
            matrix=[
                r if ridx != action['row'] else [
                    c if cidx != action['col'] else False
                    for cidx, c in enumerate(r)
                ]
                for ridx, r in enumerate(state.matrix)
            ],
        )

        if action['keycode'].code >= 1000:
            return process_internal(newstate, action, logger=logger)

        return newstate

    if action['type'] == KEY_DOWN_EVENT:
        newstate = state.update(
            keys_pressed=(
                state.keys_pressed | {action['keycode']}
            ),
            matrix=[
                r if ridx != action['row'] else [
                    c if cidx != action['col'] else True
                    for cidx, c in enumerate(r)
                ]
                for ridx, r in enumerate(state.matrix)
            ],
        )

        if action['keycode'].code >= 1000:
            return process_internal(newstate, action, logger=logger)

        return newstate

    if action['type'] == INIT_FIRMWARE_EVENT:
        return state.update(
            keymap=action['keymap'],
            row_pins=action['row_pins'],
            col_pins=action['col_pins'],
            diode_orientation=action['diode_orientation'],
            matrix=[
                [False for c in action['col_pins']]
                for r in action['row_pins']
            ],
        )
