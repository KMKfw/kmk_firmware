from kmk.kmktime import ticks_diff, ticks_ms


def mt_pressed(key, state, *args, **kwargs):
    # Sets the timer start and acts like a modifier otherwise
    state.keys_pressed.add(key.meta.mods)

    state.start_time['mod_tap'] = ticks_ms()
    return state


def mt_released(key, state, *args, **kwargs):
    # On keyup, check timer, and press key if needed.
    state.keys_pressed.discard(key.meta.mods)
    timer_name = 'mod_tap'
    if state.start_time[timer_name] and (
        ticks_diff(ticks_ms(), state.start_time[timer_name]) < state.config.tap_time
    ):
        state.hid_pending = True
        state.tap_key(key.meta.kc)

    state.start_time[timer_name] = None
    return state
