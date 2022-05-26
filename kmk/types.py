class AttrDict(dict):
    '''
    Primitive support for accessing dictionary entries in dot notation.
    Mostly for user-facing stuff (allows for `k.KC_ESC` rather than
    `k['KC_ESC']`, which gets a bit obnoxious).

    This is read-only on purpose.
    '''

    def __getattr__(self, key):
        return self[key]


class HoldTapKeyMeta:
    def __init__(
        self,
        tap,
        hold,
        prefer_hold=True,
        tap_interrupted=False,
        tap_time=None,
    ):
        self.tap = tap
        self.hold = hold
        self.prefer_hold = prefer_hold
        self.tap_interrupted = tap_interrupted
        self.tap_time = tap_time


class LayerKeyMeta:
    def __init__(self, layer, kc=None):
        self.layer = layer
        self.kc = kc


class ModTapKeyMeta(HoldTapKeyMeta):
    def __init__(self, kc=None, mods=None, **kwargs):
        super().__init__(tap=kc, hold=mods, **kwargs)


class KeySequenceMeta:
    def __init__(self, seq):
        self.seq = seq


class KeySeqSleepMeta:
    def __init__(self, ms):
        self.ms = ms


class UnicodeModeKeyMeta:
    def __init__(self, mode):
        self.mode = mode
