import logging

from kmk.common.event_defs import KEY_DOWN_EVENT, KEY_UP_EVENT
from kmk.common.keycodes import Keycodes


def process_internal_key_event(state, action, changed_key, logger=None):
    if logger is None:
        logger = logging.getLogger(__name__)

    if changed_key.code == Keycodes.Layers._KC_DF:
        return df(state, action, changed_key, logger=logger)
    elif changed_key.code == Keycodes.Layers._KC_MO:
        return mo(state, action, changed_key, logger=logger)
    elif changed_key.code == Keycodes.Layers._KC_TG:
        return tg(state, action, changed_key, logger=logger)
    elif changed_key.code == Keycodes.Layers._KC_TO:
        return to(state, action, changed_key, logger=logger)
    else:
        return state


def tilde(state, action, changed_key, logger):
    # TODO Actually process keycodes
    return state


def df(state, action, changed_key, logger):
    """Switches the default layer"""
    if action['type'] == KEY_DOWN_EVENT:
        state.active_layers[0] = changed_key.layer

    return state


def mo(state, action, changed_key, logger):
    """Momentarily activates layer, switches off when you let go"""
    if action['type'] == KEY_UP_EVENT:
        state.active_layers = [
            layer for layer in state.active_layers
            if layer != changed_key.layer
        ]
    elif action['type'] == KEY_DOWN_EVENT:
        state.active_layers.append(changed_key.layer)

    return state


def lm(layer, mod):
    """As MO(layer) but with mod active"""


def lt(layer, kc):
    """Momentarily activates layer if held, sends kc if tapped"""


def tg(state, action, changed_key, logger):
    """Toggles the layer (enables it if not active, and vise versa)"""
    if action['type'] == KEY_DOWN_EVENT:
        if changed_key.layer in state.active_layers:
            state.active_layers = [
                layer for layer in state.active_layers
                if layer != changed_key.layer
            ]
        else:
            state.active_layers.append(changed_key.layer)

    return state


def to(state, action, changed_key, logger):
    """Activates layer and deactivates all other layers"""
    if action['type'] == KEY_DOWN_EVENT:
        state.active_layers = [changed_key.layer]

    return state


def tt(layer):
    """Momentarily activates layer if held, toggles it if tapped repeatedly"""
