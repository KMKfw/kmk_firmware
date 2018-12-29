from kmk.keycodes import KC, make_key
from kmk.handlers.stock import passthrough
from kmk.types import KeySequenceMeta


def sequence_press_handler(key, state, KC, *args, **kwargs):
    old_keys_pressed = state.keys_pressed
    state.keys_pressed = set()

    for ikey in key.meta.seq:
        if not getattr(ikey, 'no_press', None):
            state.process_key(ikey, True)
            state.config._send_hid()
        if not getattr(ikey, 'no_release', None):
            state.process_key(ikey, False)
            state.config._send_hid()

    state.keys_pressed = old_keys_pressed

    return state


def simple_key_sequence(seq):
    return make_key(
        meta=KeySequenceMeta(seq),
        on_press=sequence_press_handler,
        on_release=passthrough,
    )


def send_string(message):
    seq = []

    for char in message:
        kc = KC[char]

        if char.isupper():
            kc = KC.LSHIFT(kc)

        seq.append(kc)

    return simple_key_sequence(seq)
