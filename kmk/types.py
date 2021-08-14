from kmk.consts import UnicodeMode
from kmk.keys import KeyAttrDict
from typing import List, Optional


class AttrDict(dict):
    '''
    Primitive support for accessing dictionary entries in dot notation.
    Mostly for user-facing stuff (allows for `k.KC_ESC` rather than
    `k['KC_ESC']`, which gets a bit obnoxious).

    This is read-only on purpose.
    '''

    def __getattr__(self, key: str) -> str:
        return self[key]


class LayerKeyMeta:
    def __init__(self, layer: int, kc: Optional[KeyAttrDict] = None) -> None:
        self.layer: int = layer
        self.kc: Optional[KeyAttrDict] = kc


class ModTapKeyMeta:
    def __init__(self, kc: Optional[KeyAttrDict] = None, mods: Optional[List[KeyAttrDict]] = None):
        self.mods: Optional[List[KeyAttrDict]]  = mods
        self.kc: Optional[KeyAttrDict] = kc


class KeySequenceMeta:
    def __init__(self, seq: List[KeyAttrDict]):
        self.seq: List[KeyAttrDict] = seq


class KeySeqSleepMeta:
    def __init__(self, ms: float):
        self.ms: float = ms


class UnicodeModeKeyMeta:
    def __init__(self, mode: UnicodeMode):
        self.mode = mode


class TapDanceKeyMeta:
    def __init__(self, codes):
        self.codes = codes
