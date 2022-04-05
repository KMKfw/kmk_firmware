import gc

from kmk.consts import UnicodeMode
from kmk.handlers.stock import passthrough
from kmk.keys import KC, make_key
from kmk.types import AttrDict, KeySequenceMeta


def get_wide_ordinal(char):
    if len(char) != 2:
        return ord(char)

    return 0x10000 + (ord(char[0]) - 0xD800) * 0x400 + (ord(char[1]) - 0xDC00)


def sequence_press_handler(key, keyboard, KC, *args, **kwargs):
    oldkeys_pressed = keyboard.keys_pressed
    keyboard.keys_pressed = set()

    for ikey in key.meta.seq:
        if not getattr(ikey, 'no_press', None):
            keyboard.process_key(ikey, True)
            keyboard._send_hid()
        if not getattr(ikey, 'no_release', None):
            keyboard.process_key(ikey, False)
            keyboard._send_hid()

    keyboard.keys_pressed = oldkeys_pressed

    return keyboard


def simple_key_sequence(seq):
    return make_key(
        meta=KeySequenceMeta(seq),
        on_press=sequence_press_handler,
        on_release=passthrough,
    )


def send_string(message):
    seq = []

    for char in message:
        kc = getattr(KC, char.upper())

        if char.isupper():
            kc = KC.LSHIFT(kc)

        seq.append(kc)

    return simple_key_sequence(seq)


IBUS_KEY_COMBO = simple_key_sequence((KC.LCTRL(KC.LSHIFT(KC.U)),))
RALT_KEY = simple_key_sequence((KC.RALT,))
U_KEY = simple_key_sequence((KC.U,))
ENTER_KEY = simple_key_sequence((KC.ENTER,))
RALT_DOWN_NO_RELEASE = simple_key_sequence((KC.RALT(no_release=True),))
RALT_UP_NO_PRESS = simple_key_sequence((KC.RALT(no_press=True),))


def compile_unicode_string_sequences(string_table):
    '''
    Destructively convert ("compile") unicode strings into key sequences. This
    will, for RAM saving reasons, empty the input dictionary and trigger
    garbage collection.
    '''
    target = AttrDict()

    for k, v in string_table.items():
        target[k] = unicode_string_sequence(v)

    # now loop through and kill the input dictionary to save RAM
    for k in target.keys():
        del string_table[k]

    gc.collect()

    return target


def unicode_string_sequence(unistring):
    '''
    Allows sending things like (╯°□°）╯︵ ┻━┻ directly, without
    manual conversion to Unicode codepoints.
    '''
    return unicode_codepoint_sequence([hex(get_wide_ordinal(s))[2:] for s in unistring])


def generate_codepoint_keysym_seq(codepoint, expected_length=4):
    # To make MacOS and Windows happy, always try to send
    # sequences that are of length 4 at a minimum
    # On Linux systems, we can happily send longer strings.
    # They will almost certainly break on MacOS and Windows,
    # but this is a documentation problem more than anything.
    # Not sure how to send emojis on Mac/Windows like that,
    # though, since (for example) the Canadian flag is assembled
    # from two five-character codepoints, 1f1e8 and 1f1e6
    seq = [KC.N0 for _ in range(max(len(codepoint), expected_length))]

    for idx, codepoint_fragment in enumerate(reversed(codepoint)):
        seq[-(idx + 1)] = KC.__getattr__(codepoint_fragment.upper())

    return seq


def unicode_codepoint_sequence(codepoints):
    kc_seqs = (generate_codepoint_keysym_seq(codepoint) for codepoint in codepoints)

    kc_macros = [simple_key_sequence(kc_seq) for kc_seq in kc_seqs]

    def _unicode_sequence(key, keyboard, *args, **kwargs):
        if keyboard.unicode_mode == UnicodeMode.IBUS:
            keyboard.process_key(
                simple_key_sequence(_ibus_unicode_sequence(kc_macros, keyboard)), True
            )
        elif keyboard.unicode_mode == UnicodeMode.RALT:
            keyboard.process_key(
                simple_key_sequence(_ralt_unicode_sequence(kc_macros, keyboard)), True
            )
        elif keyboard.unicode_mode == UnicodeMode.WINC:
            keyboard.process_key(
                simple_key_sequence(_winc_unicode_sequence(kc_macros, keyboard)), True
            )

    return make_key(on_press=_unicode_sequence)


def _ralt_unicode_sequence(kc_macros, keyboard):
    for kc_macro in kc_macros:
        yield RALT_DOWN_NO_RELEASE
        yield kc_macro
        yield RALT_UP_NO_PRESS


def _ibus_unicode_sequence(kc_macros, keyboard):
    for kc_macro in kc_macros:
        yield IBUS_KEY_COMBO
        yield kc_macro
        yield ENTER_KEY


def _winc_unicode_sequence(kc_macros, keyboard):
    '''
    Send unicode sequence using WinCompose:

    http://wincompose.info/
    https://github.com/SamHocevar/wincompose
    '''
    for kc_macro in kc_macros:
        yield RALT_KEY
        yield U_KEY
        yield kc_macro
        yield ENTER_KEY
