from kmk.consts import UnicodeModes
from kmk.keycodes import (Common, Macro, Modifiers,
                          generate_codepoint_keysym_seq)
from kmk.macros.simple import simple_key_sequence
from kmk.types import AttrDict
from kmk.util import get_wide_ordinal

IBUS_KEY_COMBO = Modifiers.KC_LCTRL(Modifiers.KC_LSHIFT(Common.KC_U))
RALT_KEY = Modifiers.KC_RALT
U_KEY = Common.KC_U
ENTER_KEY = Common.KC_ENTER
RALT_DOWN_NO_RELEASE = Modifiers.KC_RALT(no_release=True)
RALT_UP_NO_PRESS = Modifiers.KC_RALT(no_press=True)


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
