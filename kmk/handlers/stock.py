from time import sleep


def passthrough(key, keyboard, *args, **kwargs):
    return keyboard


def default_pressed(key, keyboard, KC, coord_int=None, coord_raw=None, *args, **kwargs):
    keyboard.hid_pending = True

    keyboard.keys_pressed.add(key)

    return keyboard


def default_released(
    key, keyboard, KC, coord_int=None, coord_raw=None, *args, **kwargs  # NOQA
):
    keyboard.hid_pending = True
    keyboard.keys_pressed.discard(key)

    return keyboard


def reset(*args, **kwargs):
    import microcontroller

    microcontroller.reset()


def bootloader(*args, **kwargs):
    import microcontroller

    microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
    microcontroller.reset()


def debug_pressed(key, keyboard, KC, *args, **kwargs):
    if keyboard.debug_enabled:
        print('DebugDisable()')
    else:
        print('DebugEnable()')

    keyboard.debug_enabled = not keyboard.debug_enabled

    return keyboard


def gesc_pressed(key, keyboard, KC, *args, **kwargs):
    GESC_TRIGGERS = {KC.LSHIFT, KC.RSHIFT, KC.LGUI, KC.RGUI}

    if GESC_TRIGGERS.intersection(keyboard.keys_pressed):
        # First, release GUI if already pressed
        keyboard._send_hid()
        # if Shift is held, KC_GRAVE will become KC_TILDE on OS level
        keyboard.keys_pressed.add(KC.GRAVE)
        keyboard.hid_pending = True
        return keyboard

    # else return KC_ESC
    keyboard.keys_pressed.add(KC.ESCAPE)
    keyboard.hid_pending = True

    return keyboard


def gesc_released(key, keyboard, KC, *args, **kwargs):
    keyboard.keys_pressed.discard(KC.ESCAPE)
    keyboard.keys_pressed.discard(KC.GRAVE)
    keyboard.hid_pending = True
    return keyboard


def bkdl_pressed(key, keyboard, KC, *args, **kwargs):
    BKDL_TRIGGERS = {KC.LGUI, KC.RGUI}

    if BKDL_TRIGGERS.intersection(keyboard.keys_pressed):
        keyboard._send_hid()
        keyboard.keys_pressed.add(KC.DEL)
        keyboard.hid_pending = True
        return keyboard

    # else return KC_ESC
    keyboard.keys_pressed.add(KC.BKSP)
    keyboard.hid_pending = True

    return keyboard


def bkdl_released(key, keyboard, KC, *args, **kwargs):
    keyboard.keys_pressed.discard(KC.BKSP)
    keyboard.keys_pressed.discard(KC.DEL)
    keyboard.hid_pending = True
    return keyboard


def sleep_pressed(key, keyboard, KC, *args, **kwargs):
    sleep(key.meta.ms / 1000)
    return keyboard


def uc_mode_pressed(key, keyboard, *args, **kwargs):
    keyboard.unicode_mode = key.meta.mode

    return keyboard


def hid_switch(key, keyboard, *args, **kwargs):
    keyboard.hid_type, keyboard.secondary_hid_type = (
        keyboard.secondary_hid_type,
        keyboard.hid_type,
    )
    keyboard._init_hid()
    return keyboard
