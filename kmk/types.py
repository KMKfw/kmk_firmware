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
    def __init__(self, layer, kc=None):
        self.layer = layer
        self.kc = kc


class ModTapKeyMeta:
    def __init__(self, kc=None, mods=None):
        self.mods = mods
        self.kc = kc


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
