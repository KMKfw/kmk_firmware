from kmk.types import KeySeqSleepMeta, LayerKeyMeta, ModTapKeyMeta, UnicodeModeKeyMeta


def key_seq_sleep_validator(ms):
    return KeySeqSleepMeta(ms)


def layer_key_validator(layer):
    '''
    Validates the syntax (but not semantics) of a layer key call.  We won't
    have access to the keymap here, so we can't verify much of anything useful
    here (like whether the target layer actually exists). The spirit of this
    existing is mostly that Python will catch extraneous args/kwargs and error
    out.
    '''
    return LayerKeyMeta(layer)


def mod_tap_validator(
    kc, mods=None, prefer_hold=True, tap_interrupted=False, tap_time=None
):
    '''
    Validates that mod tap keys are correctly used
    '''
    return ModTapKeyMeta(
        kc=kc,
        mods=mods,
        prefer_hold=prefer_hold,
        tap_interrupted=tap_interrupted,
        tap_time=tap_time,
    )


def unicode_mode_key_validator(mode):
    return UnicodeModeKeyMeta(mode)
