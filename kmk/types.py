class AttrDict(dict):
    '''
    Primitive support for accessing dictionary entries in dot notation.
    Mostly for user-facing stuff (allows for `k.KC_ESC` rather than
    `k['KC_ESC']`, which gets a bit obnoxious).

    This is read-only on purpose.
    '''
    def __getattr__(self, key):
        return self[key]


class Anything:
    '''
    A stub class which will repr as a provided name
    '''
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Anything<{}>'.format(self.name)


class Passthrough:
    def __getattr__(self, attr):
        return Anything(attr)


class LayerKeyMeta:
    def __init__(self, layer, kc=None):
        self.layer = layer
        self.kc = kc


class ModTapKeyMeta:
    def __init__(self, mod1=None, mod2=None, mod3=None, mod4=None, kc=None):
        self.mod1 = mod1
        self.mod2 = mod2
        self.mod3 = mod3
        self.mod4 = mod4
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
