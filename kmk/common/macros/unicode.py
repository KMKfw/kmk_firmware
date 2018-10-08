from kmk.common.consts import UnicodeModes
from kmk.common.event_defs import (hid_report_event, keycode_down_event,
                                   keycode_up_event)
from kmk.common.keycodes import Common, Macro, Modifiers
from kmk.common.macros.simple import lookup_kc_with_cache, simple_key_sequence
from kmk.common.util import get_wide_ordinal

IBUS_KEY_COMBO = Modifiers.KC_LCTRL(Modifiers.KC_LSHIFT(Common.KC_U))
IBUS_KEY_DOWN = keycode_down_event(IBUS_KEY_COMBO)
IBUS_KEY_UP = keycode_up_event(IBUS_KEY_COMBO)
RALT_DOWN = keycode_down_event(Modifiers.KC_RALT)
RALT_UP = keycode_up_event(Modifiers.KC_RALT)
U_DOWN = keycode_down_event(Common.KC_U)
U_UP = keycode_up_event(Common.KC_U)
ENTER_DOWN = keycode_down_event(Common.KC_ENTER)
ENTER_UP = keycode_up_event(Common.KC_ENTER)
RALT_DOWN_NO_RELEASE = keycode_down_event(Modifiers.KC_RALT(no_release=True))
RALT_UP_NO_PRESS = keycode_up_event(Modifiers.KC_RALT(no_press=True))


def generate_codepoint_keysym_seq(codepoint):
    # To make MacOS and Windows happy, always try to send
    # sequences that are of length 4 at a minimum
    # On Linux systems, we can happily send longer strings.
    # They will almost certainly break on MacOS and Windows,
    # but this is a documentation problem more than anything.
    # Not sure how to send emojis on Mac/Windows like that,
    # though, since (for example) the Canadian flag is assembled
    # from two five-character codepoints, 1f1e8 and 1f1e6
    seq = [Common.KC_0 for _ in range(max(len(codepoint), 4))]

    for idx, codepoint_fragment in enumerate(reversed(codepoint)):
        seq[-(idx + 1)] = lookup_kc_with_cache(codepoint_fragment)

    return seq


def unicode_string_sequence(unistring):
    '''
    Allows sending things like (╯°□°）╯︵ ┻━┻ directly, without
    manual conversion to Unicode codepoints.
    '''
    return unicode_codepoint_sequence([
        hex(get_wide_ordinal(s))[2:]
        for s in unistring
    ])


def unicode_codepoint_sequence(codepoints):
    kc_seqs = (
        generate_codepoint_keysym_seq(codepoint)
        for codepoint in codepoints
    )

    kc_macros = [
        simple_key_sequence(kc_seq)
        for kc_seq in kc_seqs
    ]

    def _unicode_sequence(state):
        if state.unicode_mode == UnicodeModes.IBUS:
            yield from _ibus_unicode_sequence(kc_macros, state)
        elif state.unicode_mode == UnicodeModes.RALT:
            yield from _ralt_unicode_sequence(kc_macros, state)
        elif state.unicode_mode == UnicodeModes.WINC:
            yield from _winc_unicode_sequence(kc_macros, state)

    return Macro(keydown=_unicode_sequence)


def _ralt_unicode_sequence(kc_macros, state):
    for kc_macro in kc_macros:
        yield RALT_DOWN_NO_RELEASE
        yield hid_report_event
        yield from kc_macro.keydown(state)
        yield RALT_UP_NO_PRESS
        yield hid_report_event


def _ibus_unicode_sequence(kc_macros, state):
    for kc_macro in kc_macros:
        yield IBUS_KEY_DOWN
        yield hid_report_event
        yield IBUS_KEY_UP
        yield hid_report_event
        yield from kc_macro.keydown(state)
        yield ENTER_DOWN
        yield hid_report_event
        yield ENTER_UP
        yield hid_report_event


def _winc_unicode_sequence(kc_macros, state):
    '''
    Send unicode sequence using WinCompose:

    http://wincompose.info/
    https://github.com/SamHocevar/wincompose
    '''
    for kc_macro in kc_macros:
        yield RALT_DOWN
        yield hid_report_event
        yield RALT_UP
        yield hid_report_event
        yield U_DOWN
        yield hid_report_event
        yield U_UP
        yield hid_report_event
        yield from kc_macro.keydown(state)
