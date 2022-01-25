class AttrDict(dict):
    '''
    Primitive support for accessing dictionary entries in dot notation.
    Mostly for user-facing stuff (allows for `k.KC_ESC` rather than
    `k['KC_ESC']`, which gets a bit obnoxious).

    This is read-only on purpose.
    '''

    def __getattr__(self, key):
        return self[key]


class LayerKeyMeta:
    def __init__(self, layer, kc=None, tap_time=None):
        self.layer = layer
        self.kc = kc
        self.tap_time = tap_time


class ModTapKeyMeta:
    def __init__(self, kc=None, mods=None, prefer_hold=True, tap_time=None):
        self.prefer_hold = prefer_hold
        self.kc = kc
        self.mods = mods
        self.tap_time = tap_time


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
