import logging

from kmk.common.event_defs import KEY_DOWN_EVENT, KEY_UP_EVENT
from kmk.common.keycodes import Keycodes


def process(state, action, logger=None):
    if action['keycode'].code < 1000:
        return state

    if logger is None:
        logger = logging.getLogger(__name__)

    logger.warning(action['keycode'])
    if action['keycode'] == Keycodes.KMK.KC_RESET:
        return reset(state, action, logger=logger)
    elif action['keycode'].code == Keycodes.Layers._KC_DF:
        return df(state, action, logger=logger)
    elif action['keycode'].code == Keycodes.Layers._KC_MO:
        return tilde(state, action, logger=logger)
    elif action['keycode'].code == Keycodes.Layers.KC_TILDE:
        pass
    else:
        return state


def tilde(state, action, logger):
    # TODO Actually process keycodes
    return state


def reset(state, action, logger):
    logger.debug('Rebooting to bootloader')
    import machine
    machine.bootloader()


def df(state, action, logger):
    """Switches the default layer"""
    state.active_layers[0] = action['keycode'].layer

    return state


def mo(state, action, logger):
    """Momentarily activates layer, switches off when you let go"""
    if action['type'] == KEY_UP_EVENT:
        state.active_layers = [
            layer for layer in state.active_layers
            if layer != action['keycode'].layer
        ]
    elif action['type'] == KEY_DOWN_EVENT:
        state.active_layers.append(action['keycode'].layer)

    return state


def lm(layer, mod):
    """As MO(layer) but with mod active"""


def lt(layer, kc):
    """Momentarily activates layer if held, sends kc if tapped"""


def tg(layer):
    """Toggles the layer (enables it if no active, and vise versa)"""


def to(layer):
    """Activates layer and deactivates all other layers"""


def tt(layer):
    """Momentarily activates layer if held, toggles it if tapped repeatedly"""
