import sys

from kmk.consts import TYPING_PLATFORMS

if sys.platform in TYPING_PLATFORMS:
    from typing import List, Optional, Tuple, Union

    # Avoid cyclical imports
    from kmk.keys import ConsumerKey, Key, ModifierKey


class AttrDict(dict):
    '''
    Primitive support for accessing dictionary entries in dot notation.
    Mostly for user-facing stuff (allows for `k.KC_ESC` rather than
    `k['KC_ESC']`, which gets a bit obnoxious).

    This is read-only on purpose.
    '''

    def __getattr__(self, key):
        # type: (str) -> Optional[Union[Key, ModifierKey, ConsumerKey]]
        return self[key]


class LayerKeyMeta:
    def __init__(self, layer, kc=None):
        # type: (int, Optional[Key]) -> None
        self.layer = layer  # type: int
        self.kc = kc  # type: Optional[Key]


class ModTapKeyMeta:
    def __init__(self, kc=None, mods=None):
        # type: (Optional[Key], Optional[List[Key]]) -> None
        self.mods = mods  # type: Optional[List[Key]]
        self.kc = kc  # type: Optional[Key]


class KeySequenceMeta:
    def __init__(self, seq):
        # type: (List[Key]) -> None
        self.seq = seq  # type: List[Key]


class KeySeqSleepMeta:
    def __init__(self, ms):
        # type: (float) -> None
        self.ms = ms  # type: float


class UnicodeModeKeyMeta:
    def __init__(self, mode):
        # type: (int) -> None
        self.mode = mode  # type: int


class TapDanceKeyMeta:
    def __init__(self, codes):
        # type: (Tuple[Key, ...]) -> None
        self.codes = codes  # type: Tuple[Key, ...]
