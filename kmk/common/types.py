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
