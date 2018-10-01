import logging
import sys

from kmk.common.consts import DiodeOrientation, UnicodeModes
from kmk.common.event_defs import (HID_REPORT_EVENT, INIT_FIRMWARE_EVENT,
                                   KEY_DOWN_EVENT, KEY_UP_EVENT,
                                   KEYCODE_DOWN_EVENT, KEYCODE_UP_EVENT,
                                   MACRO_COMPLETE_EVENT, NEW_MATRIX_EVENT)
from kmk.common.internal_keycodes import process_internal_key_event
from kmk.common.keycodes import FIRST_KMK_INTERNAL_KEYCODE, Keycodes
from kmk.common.macros import KMKMacro


class ReduxStore:
    def __init__(self, reducer, log_level=logging.NOTSET):
        self.reducer = reducer
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.state = self.reducer(logger=self.logger)
        self.callbacks = []

    def dispatch(self, action):
        if callable(action):
            self.logger.debug('Received thunk')
            action(self.dispatch, self.get_state)
            self.logger.debug('Finished thunk')
            return None

        self.logger.debug('Dispatching action: Type {} >> {}'.format(action['type'], action))
        self.state = self.reducer(self.state, action, logger=self.logger)
        self.logger.debug('Dispatching complete: Type {}'.format(action['type']))

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
    macro_pending = None
    unicode_mode = UnicodeModes.NOOP
    keymap = []
    row_pins = []
    col_pins = []
    matrix = []
    diode_orientation = DiodeOrientation.COLUMNS
    active_layers = [0]
    _oldstates = []

    def __init__(self, preserve_intermediate_states=False):
        self.preserve_intermediate_states = preserve_intermediate_states

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def to_dict(self, verbose=False):
        ret = {
            'keys_pressed': self.keys_pressed,
            'modifiers_pressed': self.modifiers_pressed,
            'active_layers': self.active_layers,
            'unicode_mode': self.unicode_mode,
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


def find_key_in_map(state, row, col):
    # Later-added layers have priority. Sift through the layers
    # in reverse order until we find a valid keycode object
    for layer in reversed(state.active_layers):
        layer_key = state.keymap[layer][row][col]

        if not layer_key or layer_key == Keycodes.KMK.KC_TRNS:
            continue

        if layer_key == Keycodes.KMK.KC_NO:
            break

        return layer_key


def kmk_reducer(state=None, action=None, logger=None):
    if state is None:
        state = InternalState()

        if logger is not None:
            logger.debug('Reducer received state of None, creating new')

    if action is None:
        if logger is not None:
            logger.debug('No action received, returning state unmodified')

        return state

    if action['type'] == NEW_MATRIX_EVENT:
        return state.update(
            matrix=action['matrix'],
        )

    if action['type'] == KEYCODE_UP_EVENT:
        return state.update(
            keys_pressed=frozenset(
                key for key in state.keys_pressed if key != action['keycode']
            ),
        )

    if action['type'] == KEYCODE_DOWN_EVENT:
        return state.update(
            keys_pressed=(
                state.keys_pressed | {action['keycode']}
            ),
        )

    if action['type'] == KEY_UP_EVENT:
        row = action['row']
        col = action['col']

        changed_key = find_key_in_map(state, row, col)

        logger.debug('Detected change to key: {}'.format(changed_key))

        if not changed_key:
            return state

        if isinstance(changed_key, KMKMacro):
            if changed_key.keyup:
                return state.update(
                    macro_pending=changed_key.keyup,
                )

            return state

        newstate = state.update(
            keys_pressed=frozenset(
                key for key in state.keys_pressed if key != changed_key
            ),
        )

        if changed_key.code >= FIRST_KMK_INTERNAL_KEYCODE:
            return process_internal_key_event(newstate, action, changed_key, logger=logger)

        return newstate

    if action['type'] == KEY_DOWN_EVENT:
        row = action['row']
        col = action['col']

        changed_key = find_key_in_map(state, row, col)

        logger.debug('Detected change to key: {}'.format(changed_key))

        if not changed_key:
            return state

        if isinstance(changed_key, KMKMacro):
            if changed_key.keydown:
                return state.update(
                    macro_pending=changed_key.keydown,
                )

            return state

        newstate = state.update(
            keys_pressed=(
                state.keys_pressed | {changed_key}
            ),
        )

        if changed_key.code >= FIRST_KMK_INTERNAL_KEYCODE:
            return process_internal_key_event(newstate, action, changed_key, logger=logger)

        return newstate

    if action['type'] == INIT_FIRMWARE_EVENT:
        return state.update(
            keymap=action['keymap'],
            row_pins=action['row_pins'],
            col_pins=action['col_pins'],
            diode_orientation=action['diode_orientation'],
            unicode_mode=action['unicode_mode'],
            matrix=[
                [False for c in action['col_pins']]
                for r in action['row_pins']
            ],
        )

    # HID events are non-mutating, used exclusively for listeners to know
    # they should be doing things. This could/should arguably be folded back
    # into KEY_UP_EVENT and KEY_DOWN_EVENT, but for now it's nice to separate
    # this out for debugging's sake.
    if action['type'] == HID_REPORT_EVENT:
        return state

    if action['type'] == MACRO_COMPLETE_EVENT:
        return state.update(macro_pending=None)

    # On unhandled events, log and do not mutate state
    logger.warning('Unhandled event! Returning state unmodified.')
    return state
