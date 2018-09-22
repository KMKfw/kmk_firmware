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
        return reset(logger)
    elif action['keycode'] == Keycodes.Layers.KC_DF:
        return df(state, "Filler", action, logger=logger)
    elif action['keycode'] == Keycodes.Layers.KC_MO:
        return mo(state, "Filler", action, logger=logger)


def reset(logger):
    logger.debug('Rebooting to bootloader')
    import machine
    machine.bootloader()


def df(state, layer, action, logger):
    """Switches the default layer"""
    state.active_layers = [1]

    return state


def mo(state, layer, action, logger):
    """Momentarily activates layer, switches off when you let go"""
    if action['type'] == KEY_UP_EVENT:
        state.active_layers = [0]
    elif action['type'] == KEY_DOWN_EVENT:
        state.active_layers = [0, 1]

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
