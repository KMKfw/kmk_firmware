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
    def __init__(self, kc=None, prefer_hold=True, tap_interrupted=False, tap_time=None):
        self.kc = kc
        self.prefer_hold = prefer_hold
        self.tap_interrupted = tap_interrupted
        self.tap_time = tap_time


class LayerKeyMeta(HoldTapKeyMeta):
    def __init__(self, layer, **kwargs):
        super().__init__(**kwargs)
        self.layer = layer


class ModTapKeyMeta(HoldTapKeyMeta):
    def __init__(self, kc=None, mods=None, **kwargs):
        super().__init__(kc=kc, **kwargs)
        self.mods = mods


class KeySequenceMeta:
    def __init__(self, seq):
        self.seq = seq


class KeySeqSleepMeta:
    def __init__(self, ms):
        self.ms = ms


class UnicodeModeKeyMeta:
    def __init__(self, mode):
        self.mode = mode


class TapDanceKeyMeta:
    def __init__(self, codes):
        self.codes = codes
