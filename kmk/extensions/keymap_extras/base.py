from kmk.keys import KC


class KeyMapConverter:
    '''Class to allow easy definition of alternative layout'''

    def __getattr__(self, key):
        try:
            return self.MAPPING[key]
        except KeyError:
            return getattr(KC, key)
