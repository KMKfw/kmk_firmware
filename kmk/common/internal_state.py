import logging
import sys

from kmk.common import kmktime
from kmk.common.consts import DiodeOrientation, UnicodeModes
from kmk.common.event_defs import (HID_REPORT_EVENT, INIT_FIRMWARE_EVENT,
                                   KEY_DOWN_EVENT, KEY_UP_EVENT,
                                   KEYCODE_DOWN_EVENT, KEYCODE_UP_EVENT,
                                   MACRO_COMPLETE_EVENT, NEW_MATRIX_EVENT,
                                   PENDING_KEYCODE_POP_EVENT)
from kmk.common.keycodes import (FIRST_KMK_INTERNAL_KEYCODE, Keycodes,
                                 RawKeycodes)

GESC_TRIGGERS = {
    Keycodes.Modifiers.KC_LSHIFT, Keycodes.Modifiers.KC_RSHIFT,
    Keycodes.Modifiers.KC_LGUI, Keycodes.Modifiers.KC_RGUI,
}


class Store:
    '''
    A data store very loosely inspired by Redux, but with most of the fancy
    functional and immutable abilities unavailable because microcontrollers.
    This serves as the event dispatcher at the heart of KMK. All changes to the
    state of the keyboard should be triggered by events (see event_defs.py)
    dispatched through this store, and listened to (for side-effects or other
    handling) by subscription functions.
    '''
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

        self.logger.debug('Dispatching action: Type {} >> {}'.format(action.type, action))
        self.state = self.reducer(self.state, action, logger=self.logger)
        self.logger.debug('Dispatching complete: Type {}'.format(action.type))

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
    keys_pressed = set()
    pending_keys = set()
    macro_pending = None
    hid_pending = False
    unicode_mode = UnicodeModes.NOOP
    tap_time = 300
    keymap = []
    row_pins = []
    col_pins = []
    matrix = []
    diode_orientation = DiodeOrientation.COLUMNS
    active_layers = [0]
    start_time = {
        'lt': None,
        'tg': None,
        'tt': None,
    }
    tick_time = {
        'lt': None,
        'tg': None,
        'tt': None,
    }
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
            'active_layers': self.active_layers,
            'unicode_mode': self.unicode_mode,
            'tap_time': self.tap_time,
            'start_time': self.start_time,
            'tick_time': self.tick_time,
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

    if action.type == NEW_MATRIX_EVENT:
        matrix_keys_pressed = {
            find_key_in_map(state, row, col)
            for row, col, in action.matrix
        }

        pressed = matrix_keys_pressed - state.keys_pressed
        released = state.keys_pressed - matrix_keys_pressed

        if not pressed and not released:
            return state

        for changed_key in released:
            if not changed_key:
                continue
            elif changed_key.code >= FIRST_KMK_INTERNAL_KEYCODE:
                state = process_internal_key_event(state,
                                                   KEY_UP_EVENT,
                                                   changed_key,
                                                   logger=logger)

        for changed_key in pressed:
            if not changed_key:
                continue
            elif changed_key.code >= FIRST_KMK_INTERNAL_KEYCODE:
                state = process_internal_key_event(
                    state,
                    KEY_DOWN_EVENT,
                    changed_key,
                    logger=logger,
                )

        state.matrix = action.matrix
        state.keys_pressed |= pressed
        state.keys_pressed -= released
        state.hid_pending = True

        return state

    if action.type == KEYCODE_UP_EVENT:
        state.keys_pressed.discard(action.keycode)
        state.hid_pending = True
        return state

    if action.type == KEYCODE_DOWN_EVENT:
        state.keys_pressed.add(action.keycode)
        state.hid_pending = True
        return state

    if action.type == INIT_FIRMWARE_EVENT:
        return state.update(
            keymap=action.keymap,
            row_pins=action.row_pins,
            col_pins=action.col_pins,
            diode_orientation=action.diode_orientation,
            unicode_mode=action.unicode_mode,
        )

    # HID events are non-mutating, used exclusively for listeners to know
    # they should be doing things. This could/should arguably be folded back
    # into KEY_UP_EVENT and KEY_DOWN_EVENT, but for now it's nice to separate
    # this out for debugging's sake.
    if action.type == HID_REPORT_EVENT:
        state.hid_pending = False
        return state

    if action.type == MACRO_COMPLETE_EVENT:
        return state.update(macro_pending=None)

    if action.type == PENDING_KEYCODE_POP_EVENT:
        state.pending_keys.pop()
        return state

    # On unhandled events, log and do not mutate state
    logger.warning('Unhandled event! Returning state unmodified.')
    return state


def process_internal_key_event(state, action_type, changed_key, logger=None):
    if logger is None:
        logger = logging.getLogger(__name__)

    # Since the key objects can be chained into new objects
    # with, for example, no_press set, always check against
    # the underlying code rather than comparing Keycode
    # objects

    if changed_key.code == RawKeycodes.KC_DF:
        return df(state, action_type, changed_key, logger=logger)
    elif changed_key.code == RawKeycodes.KC_MO:
        return mo(state, action_type, changed_key, logger=logger)
    elif changed_key.code == RawKeycodes.KC_LM:
        return lm(state, action_type, changed_key, logger=logger)
    elif changed_key.code == RawKeycodes.KC_LT:
        return lt(state, action_type, changed_key, logger=logger)
    elif changed_key.code == RawKeycodes.KC_TG:
        return tg(state, action_type, changed_key, logger=logger)
    elif changed_key.code == RawKeycodes.KC_TO:
        return to(state, action_type, changed_key, logger=logger)
    elif changed_key.code == RawKeycodes.KC_TT:
        return tt(state, action_type, changed_key, logger=logger)
    elif changed_key.code == Keycodes.KMK.KC_GESC.code:
        return grave_escape(state, action_type, logger=logger)
    elif changed_key.code == RawKeycodes.KC_UC_MODE:
        return unicode_mode(state, action_type, changed_key, logger=logger)
    elif changed_key.code == RawKeycodes.KC_MACRO:
        return macro(state, action_type, changed_key, logger=logger)
    else:
        return state


def grave_escape(state, action_type, logger):
    if action_type == KEY_DOWN_EVENT:
        if any(key in GESC_TRIGGERS for key in state.keys_pressed):
            # if Shift is held, KC_GRAVE will become KC_TILDE on OS level
            state.keys_pressed.add(Keycodes.Common.KC_GRAVE)
            return state

        # else return KC_ESC
        state.keys_pressed.add(Keycodes.Common.KC_ESCAPE)
        return state

    elif action_type == KEY_UP_EVENT:
        state.keys_pressed.discard(Keycodes.Common.KC_ESCAPE)
        state.keys_pressed.discard(Keycodes.Common.KC_GRAVE)
        return state

    return state


def df(state, action_type, changed_key, logger):
    """Switches the default layer"""
    if action_type == KEY_DOWN_EVENT:
        state.active_layers[0] = changed_key.layer

    return state


def mo(state, action_type, changed_key, logger):
    """Momentarily activates layer, switches off when you let go"""
    if action_type == KEY_UP_EVENT:
        state.active_layers = [
            layer for layer in state.active_layers
            if layer != changed_key.layer
        ]
    elif action_type == KEY_DOWN_EVENT:
        state.active_layers.append(changed_key.layer)

    return state


def lm(state, action_type, changed_key, logger):
    """As MO(layer) but with mod active"""
    if action_type == KEY_DOWN_EVENT:
        # Sets the timer start and acts like MO otherwise
        state.start_time['lm'] = kmktime.ticks_ms()
        state.keys_pressed.add(changed_key.kc)
        state = mo(state, action_type, changed_key, logger)
    elif action_type == KEY_UP_EVENT:
        state.keys_pressed.discard(changed_key.kc)
        state.start_time['lm'] = None
        state = mo(state, action_type, changed_key)

    return state


def lt(state, action_type, changed_key, logger):
    """Momentarily activates layer if held, sends kc if tapped"""
    if action_type == KEY_DOWN_EVENT:
        # Sets the timer start and acts like MO otherwise
        state.start_time['lt'] = kmktime.ticks_ms()
        state = mo(state, action_type, changed_key, logger)
    elif action_type == KEY_UP_EVENT:
        # On keyup, check timer, and press key if needed.
        if state.start_time['lt'] and (
            kmktime.ticks_diff(kmktime.ticks_ms(), state.start_time['lt']) < state.tap_time
        ):
            state.pending_keys.add(changed_key.kc)

        state.start_time['lt'] = None
        state = mo(state, action_type, changed_key, logger)

    return state


def tg(state, action_type, changed_key, logger):
    """Toggles the layer (enables it if not active, and vise versa)"""
    if action_type == KEY_DOWN_EVENT:
        if changed_key.layer in state.active_layers:
            state.active_layers = [
                layer for layer in state.active_layers
                if layer != changed_key.layer
            ]
        else:
            state.active_layers.append(changed_key.layer)

    return state


def to(state, action_type, changed_key, logger):
    """Activates layer and deactivates all other layers"""
    if action_type == KEY_DOWN_EVENT:
        state.active_layers = [changed_key.layer]

    return state


def tt(state, action_type, changed_key, logger):
    """Momentarily activates layer if held, toggles it if tapped repeatedly"""
    # TODO Make this work with tap dance to function more correctly, but technically works.
    if action_type == KEY_DOWN_EVENT:
        if state.start_time['tt'] is None:
            # Sets the timer start and acts like MO otherwise
            state.start_time['tt'] = kmktime.ticks_ms()
            state = mo(state, action_type, changed_key, logger)
        elif kmktime.ticks_diff(kmktime.ticks_ms(), state.start_time['tt']) < state.tap_time:
            state.start_time['tt'] = None
            state = tg(state, action_type, changed_key, logger)
    elif action_type == KEY_UP_EVENT and (
        state.start_time['tt'] is None or
        kmktime.ticks_diff(kmktime.ticks_ms(), state.start_time['tt']) >= state.tap_time
    ):
        # On first press, works like MO. On second press, does nothing unless let up within
        # time window, then acts like TG.
        state.start_time['tt'] = None
        state = mo(state, action_type, changed_key, logger)

    return state


def unicode_mode(state, action_type, changed_key, logger):
    if action_type == KEY_DOWN_EVENT:
        state.unicode_mode = changed_key.mode

    return state


def macro(state, action_type, changed_key, logger):
    if action_type == KEY_UP_EVENT:
        if changed_key.keyup:
            state.macro_pending = changed_key.keyup
            return state

    elif action_type == KEY_DOWN_EVENT:
        if changed_key.keydown:
            state.macro_pending = changed_key.keydown
            return state

    return state
