from kmk.kmktime import sleep_ms
from kmk.util import reset_bootloader, reset_keyboard


def passthrough(key, state, *args, **kwargs):
    return state


def default_pressed(key, state, KC, coord_int=None, coord_raw=None):
    state.hid_pending = True

    if coord_int is not None:
        state.coord_keys_pressed[coord_int] = key

    state.keys_pressed.add(key)

    return state


def default_released(key, state, KC, coord_int=None, coord_raw=None):
    state.hid_pending = True
    state.keys_pressed.discard(key)

    if coord_int is not None:
        state.keys_pressed.discard(state.coord_keys_pressed.get(coord_int, None))
        state.coord_keys_pressed[coord_int] = None

    return state


def reset(*args, **kwargs):
    reset_keyboard()


def bootloader(*args, **kwargs):
    reset_bootloader()


def debug_pressed(key, state, KC, *args, **kwargs):
    if state.config.debug_enabled:
        print('Disabling debug mode, bye!')
    else:
        print('Enabling debug mode. Welcome to the jungle.')

    state.config.debug_enabled = not state.config.debug_enabled

    return state


def gesc_pressed(key, state, KC, *args, **kwargs):
    GESC_TRIGGERS = {KC.LSHIFT, KC.RSHIFT, KC.LGUI, KC.RGUI}

    if GESC_TRIGGERS.intersection(state.keys_pressed):
        # if Shift is held, KC_GRAVE will become KC_TILDE on OS level
        state.keys_pressed.add(KC.GRAVE)
        return state

    # else return KC_ESC
    state.keys_pressed.add(KC.ESCAPE)
    state.hid_pending = True

    return state


def gesc_released(key, state, KC, *args, **kwargs):
    state.keys_pressed.discard(KC.ESCAPE)
    state.keys_pressed.discard(KC.GRAVE)
    state.hid_pending = True
    return state


def sleep_pressed(key, state, KC, *args, **kwargs):
    sleep_ms(key.meta.ms)
    return state


def uc_mode_pressed(key, state, *args, **kwargs):
    state.config.unicode_mode = key.meta.mode

    return state


def leader_pressed(key, state, *args, **kwargs):
    return state._begin_leader_mode()


def td_pressed(key, state, *args, **kwargs):
    return state._process_tap_dance(key, True)


def td_released(key, state, *args, **kwargs):
    return state._process_tap_dance(key, False)
