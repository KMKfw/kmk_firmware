from kmk.common.event_defs import (hid_report_event, keycode_down_event,
                                   keycode_up_event)
from kmk.common.macros import KMKMacro


def simple_key_sequence(seq):
    def _simple_key_sequence(state):
        for key in seq:
            if not getattr(key, 'no_press', None):
                yield keycode_down_event(key)
                yield hid_report_event()

            if not getattr(key, 'no_release', None):
                yield keycode_up_event(key)
                yield hid_report_event()

    return KMKMacro(keydown=_simple_key_sequence)
