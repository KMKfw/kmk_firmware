from kmk.consts import UnicodeMode
from kmk.keycodes import KC, Macro
from kmk.macros.simple import simple_key_sequence
from kmk.types import AttrDict
from kmk.util import get_wide_ordinal

IBUS_KEY_COMBO = KC.LCTRL(KC.LSHIFT(KC.U))
RALT_KEY = KC.RALT
U_KEY = KC.U
ENTER_KEY = KC.ENTER
RALT_DOWN_NO_RELEASE = KC.RALT(no_release=True)
RALT_UP_NO_PRESS = KC.RALT(no_press=True)


def compile_unicode_string_sequences(string_table):
    for k, v in string_table.items():
        string_table[k] = unicode_string_sequence(v)

    return AttrDict(string_table)


def unicode_string_sequence(unistring):
    '''
    Allows sending things like (╯°□°）╯︵ ┻━┻ directly, without
    manual conversion to Unicode codepoints.
    '''
    return unicode_codepoint_sequence([
        hex(get_wide_ordinal(s))[2:]
        for s in unistring
    ])


def generate_codepoint_keysym_seq(codepoint, expected_length=4):
    # To make MacOS and Windows happy, always try to send
    # sequences that are of length 4 at a minimum
    # On Linux systems, we can happily send longer strings.
    # They will almost certainly break on MacOS and Windows,
    # but this is a documentation problem more than anything.
    # Not sure how to send emojis on Mac/Windows like that,
    # though, since (for example) the Canadian flag is assembled
    # from two five-character codepoints, 1f1e8 and 1f1e6
    #
    # As a bonus, this function can be pretty useful for
    # leader dictionary keys as strings.
    seq = [KC.N0 for _ in range(max(len(codepoint), expected_length))]

    for idx, codepoint_fragment in enumerate(reversed(codepoint)):
        seq[-(idx + 1)] = KC.get(codepoint_fragment)

    return seq


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
        if state.unicode_mode == UnicodeMode.IBUS:
            yield from _ibus_unicode_sequence(kc_macros, state)
        elif state.unicode_mode == UnicodeMode.RALT:
            yield from _ralt_unicode_sequence(kc_macros, state)
        elif state.unicode_mode == UnicodeMode.WINC:
            yield from _winc_unicode_sequence(kc_macros, state)

    return Macro(keydown=_unicode_sequence)


def _ralt_unicode_sequence(kc_macros, state):
    for kc_macro in kc_macros:
        yield RALT_DOWN_NO_RELEASE
        yield from kc_macro.keydown(state)
        yield RALT_UP_NO_PRESS


def _ibus_unicode_sequence(kc_macros, state):
    for kc_macro in kc_macros:
        yield IBUS_KEY_COMBO
        yield from kc_macro.keydown(state)
        yield ENTER_KEY


def _winc_unicode_sequence(kc_macros, state):
    '''
    Send unicode sequence using WinCompose:

    http://wincompose.info/
    https://github.com/SamHocevar/wincompose
    '''
    for kc_macro in kc_macros:
        yield RALT_KEY
        yield U_KEY
        yield from kc_macro.keydown(state)
