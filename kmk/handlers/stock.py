from kmk.kmktime import sleep_ms


def passthrough(key, state, *args, **kwargs):
    return state


def default_pressed(key, state, KC, coord_int=None, coord_raw=None, *args, **kwargs):
    state.hid_pending = True

    if coord_int is not None:
        state._coordkeys_pressed[coord_int] = key

    state.keys_pressed.add(key)

    return state


def default_released(key, state, KC, coord_int=None, coord_raw=None, *args, **kwargs):
    state.hid_pending = True
    state.keys_pressed.discard(key)

    if coord_int is not None:
        state.keys_pressed.discard(state._coordkeys_pressed.get(coord_int, None))
        state._coordkeys_pressed[coord_int] = None

    return state


def reset(*args, **kwargs):
    import microcontroller

    microcontroller.reset()


def bootloader(*args, **kwargs):
    import microcontroller

    microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
    microcontroller.reset()


def debug_pressed(key, state, KC, *args, **kwargs):
    if state.debug_enabled:
        print('DebugDisable()')
    else:
        print('DebugEnable()')

    state.debug_enabled = not state.debug_enabled

    return state


def gesc_pressed(key, state, KC, *args, **kwargs):
    GESC_TRIGGERS = {KC.LSHIFT, KC.RSHIFT, KC.LGUI, KC.RGUI}

    if GESC_TRIGGERS.intersection(state.keys_pressed):
        # First, release GUI if already pressed
        state._send_hid()
        # if Shift is held, KC_GRAVE will become KC_TILDE on OS level
        state.keys_pressed.add(KC.GRAVE)
        state.hid_pending = True
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


def bkdl_pressed(key, state, KC, *args, **kwargs):
    BKDL_TRIGGERS = {KC.LGUI, KC.RGUI}

    if BKDL_TRIGGERS.intersection(state.keys_pressed):
        state._send_hid()
        state.keys_pressed.add(KC.DEL)
        state.hid_pending = True
        return state

    # else return KC_ESC
    state.keys_pressed.add(KC.BKSP)
    state.hid_pending = True

    return state


def bkdl_released(key, state, KC, *args, **kwargs):
    state.keys_pressed.discard(KC.BKSP)
    state.keys_pressed.discard(KC.DEL)
    state.hid_pending = True
    return state


def sleep_pressed(key, state, KC, *args, **kwargs):
    sleep_ms(key.meta.ms)
    return state


def uc_mode_pressed(key, state, *args, **kwargs):
    state.unicode_mode = key.meta.mode

    return state


def td_pressed(key, state, *args, **kwargs):
    return state._process_tap_dance(key, True)


def td_released(key, state, *args, **kwargs):
    return state._process_tap_dance(key, False)
