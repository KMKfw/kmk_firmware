from kmk.common.consts import UnicodeModes
from kmk.common.event_defs import (hid_report_event, keycode_down_event,
                                   keycode_up_event)
from kmk.common.keycodes import Common, Modifiers
from kmk.common.macros import KMKMacro
from kmk.common.macros.simple import simple_key_sequence

IBUS_KEY_COMBO = Modifiers.KC_LCTRL(Modifiers.KC_LSHIFT(Common.KC_U))


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
        seq[-(idx + 1)] = getattr(Common, 'KC_{}'.format(codepoint_fragment.upper()))

    return seq


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
