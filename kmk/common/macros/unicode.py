from kmk.common.consts import UnicodeModes
from kmk.common.event_defs import (hid_report_event, keycode_down_event,
                                   keycode_up_event)
from kmk.common.keycodes import Common, Modifiers
from kmk.common.macros import KMKMacro
from kmk.common.macros.simple import simple_key_sequence

IBUS_KEY_COMBO = Modifiers.KC_LCTRL(Modifiers.KC_LSHIFT(Common.KC_U))


def generate_codepoint_keysym_seq(codepoint):
    return [
        getattr(Common, 'KC_{}'.format(codepoint_fragment.upper()))
        for codepoint_fragment in codepoint
    ]


def unicode_sequence(codepoints):
    def _unicode_sequence(state):
        if state.unicode_mode == UnicodeModes.IBUS:
            yield from _ibus_unicode_sequence(codepoints, state)
        elif state.unicode_mode == UnicodeModes.RALT:
            yield from _ralt_unicode_sequence(codepoints, state)
        elif state.unicode_mode == UnicodeModes.WINC:
            yield from _winc_unicode_sequence(codepoints, state)

    return KMKMacro(keydown=_unicode_sequence)


def _ralt_unicode_sequence(codepoints, state):
    for codepoint in codepoints:
        yield keycode_down_event(Modifiers.RALT(no_release=True))
        yield from simple_key_sequence(generate_codepoint_keysym_seq(codepoint)).keydown(state)
        yield keycode_up_event(Modifiers.RALT(no_press=True))


def _ibus_unicode_sequence(codepoints, state):
    for codepoint in codepoints:
        yield keycode_down_event(IBUS_KEY_COMBO)
        yield hid_report_event()
        yield keycode_up_event(IBUS_KEY_COMBO)
        yield hid_report_event()

        seq = generate_codepoint_keysym_seq(codepoint)
        seq.append(Common.KC_ENTER)

        yield from simple_key_sequence(seq).keydown(state)


def _winc_unicode_sequence(codepoints, state):
    '''
    Send unicode sequence using WinCompose:

    http://wincompose.info/
    https://github.com/SamHocevar/wincompose
    '''
    for codepoint in codepoints:
        yield keycode_down_event(Modifiers.RALT())
        yield keycode_down_event(Common.KC_U())
        yield from simple_key_sequence(generate_codepoint_keysym_seq(codepoint)).keydown(state)
