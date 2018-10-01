from kmk.common.event_defs import (hid_report_event, keycode_down_event,
                                   keycode_up_event)
from kmk.macros import KMKMacro


def simple_key_sequence(seq):
    def _simple_key_sequence():
        for key in seq:
            yield keycode_down_event(key)
            yield hid_report_event()
            yield keycode_up_event(key)
            yield hid_report_event()

    return KMKMacro(keydown=_simple_key_sequence)
