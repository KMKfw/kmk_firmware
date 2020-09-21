from kmk.kmktime import sleep_ms


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
    try:
        import machine

        machine.reset()

    except ImportError:
        import microcontroller

        microcontroller.reset()


def bootloader(*args, **kwargs):
    try:
        import machine

        machine.bootloader()

    except ImportError:
        import microcontroller

        microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
        microcontroller.reset()


def debug_pressed(key, state, KC, *args, **kwargs):
    if state.config.debug_enabled:
        print('DebugDisable()')
    else:
        print('DebugEnable()')

    state.config.debug_enabled = not state.config.debug_enabled

    return state


def gesc_pressed(key, state, KC, *args, **kwargs):
    GESC_TRIGGERS = {KC.LSHIFT, KC.RSHIFT, KC.LGUI, KC.RGUI}

    if GESC_TRIGGERS.intersection(state.keys_pressed):
        # First, release GUI if already pressed
        state.config._send_hid()
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
        state.config._send_hid()
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
    state.config.unicode_mode = key.meta.mode

    return state


def leader_pressed(key, state, *args, **kwargs):
    return state._begin_leader_mode()


def td_pressed(key, state, *args, **kwargs):
    return state._process_tap_dance(key, True)


def td_released(key, state, *args, **kwargs):
    return state._process_tap_dance(key, False)


def rgb_tog(key, state, *args, **kwargs):
    if state.config.pixels.animation_mode == 'static_standby':
        state.config.pixels.animation_mode = 'static'
    state.config.pixels.enabled = not state.config.pixels.enabled
    return state


def rgb_hui(key, state, *args, **kwargs):
    state.config.pixels.increase_hue()
    return state


def rgb_hud(key, state, *args, **kwargs):
    state.config.pixels.decrease_hue()
    return state


def rgb_sai(key, state, *args, **kwargs):
    state.config.pixels.increase_sat()
    return state


def rgb_sad(key, state, *args, **kwargs):
    state.config.pixels.decrease_sat()
    return state


def rgb_vai(key, state, *args, **kwargs):
    state.config.pixels.increase_val()
    return state


def rgb_vad(key, state, *args, **kwargs):
    state.config.pixels.decrease_val()
    return state


def rgb_ani(key, state, *args, **kwargs):
    state.config.pixels.increase_ani()
    return state


def rgb_and(key, state, *args, **kwargs):
    state.config.pixels.decrease_ani()
    return state


def rgb_mode_static(key, state, *args, **kwargs):
    state.config.pixels.effect_init = True
    state.config.pixels.animation_mode = 'static'
    return state


def rgb_mode_breathe(key, state, *args, **kwargs):
    state.config.pixels.effect_init = True
    state.config.pixels.animation_mode = 'breathing'
    return state


def rgb_mode_breathe_rainbow(key, state, *args, **kwargs):
    state.config.pixels.effect_init = True
    state.config.pixels.animation_mode = 'breathing_rainbow'
    return state


def rgb_mode_rainbow(key, state, *args, **kwargs):
    state.config.pixels.effect_init = True
    state.config.pixels.animation_mode = 'rainbow'
    return state


def rgb_mode_swirl(key, state, *args, **kwargs):
    state.config.pixels.effect_init = True
    state.config.pixels.animation_mode = 'swirl'
    return state


def rgb_mode_knight(key, state, *args, **kwargs):
    state.config.pixels.effect_init = True
    state.config.pixels.animation_mode = 'knight'
    return state


def led_tog(key, state, *args, **kwargs):
    if state.config.led.animation_mode == 'static_standby':
        state.config.led.animation_mode = 'static'
    state.config.led.enabled = not state.config.led.enabled
    return state


def led_inc(key, state, *args, **kwargs):
    state.config.led.increase_brightness()
    return state


def led_dec(key, state, *args, **kwargs):
    state.config.led.decrease_brightness()
    return state


def led_ani(key, state, *args, **kwargs):
    state.config.led.increase_ani()
    return state


def led_and(key, state, *args, **kwargs):
    state.config.led.decrease_ani()
    return state


def led_mode_static(key, state, *args, **kwargs):
    state.config.led.effect_init = True
    state.config.led.animation_mode = 'static'
    return state


def led_mode_breathe(key, state, *args, **kwargs):
    state.config.led.effect_init = True
    state.config.led.animation_mode = 'breathing'
    return state


def bt_clear_bonds(key, state, *args, **kwargs):
    state.config._hid_helper_inst.clear_bonds()
    return state


def bt_next_conn(key, state, *args, **kwargs):
    state.config._hid_helper_inst.next_connection()
    return state


def bt_prev_conn(key, state, *args, **kwargs):
    state.config._hid_helper_inst.previous_connection()
    return state
