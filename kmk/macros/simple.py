import string

from kmk.keycodes import (Keycodes, Macro, RawKeycodes, char_lookup,
                          lookup_kc_with_cache)
from kmk.kmktime import sleep_ms


def simple_key_sequence(seq):
    def _simple_key_sequence(state):
        return seq

    return Macro(keydown=_simple_key_sequence)


def send_string(message):
    seq = []

    for char in message:
        kc = None

        if char in char_lookup:
            kc = char_lookup[char]
        elif char in string.ascii_letters + string.digits:
            kc = lookup_kc_with_cache(char)

            if char.isupper():
                kc = Keycodes.Modifiers.KC_LSHIFT(kc)

        seq.append(kc)

    return simple_key_sequence(seq)
