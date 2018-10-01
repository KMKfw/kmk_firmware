import string

from kmk.common.event_defs import (hid_report_event, keycode_down_event,
                                   keycode_up_event)
from kmk.common.keycodes import Keycodes, Macro, RawKeycodes, char_lookup
from kmk.common.util import sleep_ms


def simple_key_sequence(seq):
    def _simple_key_sequence(state):
        for key in seq:
            if key.code == RawKeycodes.KC_MACRO_SLEEP_MS:
                sleep_ms(key.ms)
                continue

            if not getattr(key, 'no_press', None):
                yield keycode_down_event(key)
                yield hid_report_event()

            if not getattr(key, 'no_release', None):
                yield keycode_up_event(key)
                yield hid_report_event()

    return Macro(keydown=_simple_key_sequence)


def send_string(message):
    seq = []

    for char in message:
        kc = None

        if char in char_lookup:
            kc = char_lookup[char]
        elif char in string.ascii_letters + string.digits:
            kc = getattr(Keycodes.Common, 'KC_{}'.format(char.upper()))

            if char.isupper():
                kc = Keycodes.Modifiers.KC_LSHIFT(kc)

        seq.append(kc)

    return simple_key_sequence(seq)
