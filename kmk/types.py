from typing import List, Optional, Tuple

from kmk.keys import Key


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
    def __init__(self, layer: int, kc: Optional[Key] = None) -> None:
        self.layer: int = layer
        self.kc: Optional[Key] = kc


class ModTapKeyMeta:
    def __init__(self, kc: Optional[Key] = None, mods: Optional[List[Key]] = None) -> None:
        self.mods: Optional[List[Key]] = mods
        self.kc: Optional[Key] = kc


class KeySequenceMeta:
    def __init__(self, seq: List[Key]):
        self.seq: List[Key] = seq


class KeySeqSleepMeta:
    def __init__(self, ms: float):
        self.ms: float = ms


class UnicodeModeKeyMeta:
    def __init__(self, mode: int):
        self.mode: int = mode


class TapDanceKeyMeta:
    def __init__(self, codes: Tuple[Key, ...]):
        self.codes: Tuple[Key, ...] = codes
