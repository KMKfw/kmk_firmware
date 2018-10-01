import logging

from kmk.common.event_defs import KEY_DOWN_EVENT, KEY_UP_EVENT
from kmk.common.keycodes import Keycodes, RawKeycodes

GESC_TRIGGERS = {
    Keycodes.Modifiers.KC_LSHIFT, Keycodes.Modifiers.KC_RSHIFT,
    Keycodes.Modifiers.KC_LGUI, Keycodes.Modifiers.KC_RGUI,
}


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
    elif changed_key.code == RawKeycodes.KC_TG:
        return tg(state, action_type, changed_key, logger=logger)
    elif changed_key.code == RawKeycodes.KC_TO:
        return to(state, action_type, changed_key, logger=logger)
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


def lm(layer, mod):
    """As MO(layer) but with mod active"""


def lt(layer, kc):
    """Momentarily activates layer if held, sends kc if tapped"""


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


def tt(layer):
    """Momentarily activates layer if held, toggles it if tapped repeatedly"""


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
