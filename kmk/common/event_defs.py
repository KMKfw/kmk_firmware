from micropython import const

KEY_UP_EVENT = const(1)
KEY_DOWN_EVENT = const(2)


def key_up_event(keycode):
    return {
        'type': KEY_UP_EVENT,
        'keycode': keycode,
    }


def key_down_event(keycode):
    return {
        'type': KEY_DOWN_EVENT,
        'keycode': keycode,
    }
