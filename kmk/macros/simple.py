from kmk.common.event_defs import (hid_report_event, keycode_down_event,
                                   keycode_up_event)
from kmk.common.keycodes import Common, Modifiers
from kmk.macros import KMKMacro


def simple_key_sequence(seq):
    def _simple_key_sequence():
        for key in seq:
            yield keycode_down_event(key)
            yield hid_report_event()
            yield keycode_up_event(key)
            yield hid_report_event()

    return KMKMacro(keydown=_simple_key_sequence)


def ibus_unicode_sequence(codepoints):
    seq = []

    for codepoint in codepoints:
        seq.append(Modifiers.KC_LCTRL(Modifiers.KC_LSHIFT(Common.KC_U)))

        for codepoint_fragment in codepoint:
            seq.append(getattr(Common, 'KC_{}'.format(codepoint_fragment.upper())))

        seq.append(Common.KC_ENTER)

    return simple_key_sequence(seq)
