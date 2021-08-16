from typing import List, Optional, Tuple
from kmk.keys import Key
from kmk.types import (
    KeySeqSleepMeta,
    LayerKeyMeta,
    ModTapKeyMeta,
    TapDanceKeyMeta,
    UnicodeModeKeyMeta,
)


def key_seq_sleep_validator(ms: float) -> KeySeqSleepMeta:
    return KeySeqSleepMeta(ms)


def layer_key_validator(layer: int, kc: Key = None) -> LayerKeyMeta:
    '''
    Validates the syntax (but not semantics) of a layer key call.  We won't
    have access to the keymap here, so we can't verify much of anything useful
    here (like whether the target layer actually exists). The spirit of this
    existing is mostly that Python will catch extraneous args/kwargs and error
    out.
    '''
    return LayerKeyMeta(layer=layer, kc=kc)


def mod_tap_validator(kc: Key, mods: Optional[List[Key]] = None) -> ModTapKeyMeta:
    '''
    Validates that mod tap keys are correctly used
    '''
    return ModTapKeyMeta(kc=kc, mods=mods)


def tap_dance_key_validator(*codes: Key) -> TapDanceKeyMeta:
    return TapDanceKeyMeta(codes)


def unicode_mode_key_validator(mode: int) -> UnicodeModeKeyMeta:
    return UnicodeModeKeyMeta(mode)
