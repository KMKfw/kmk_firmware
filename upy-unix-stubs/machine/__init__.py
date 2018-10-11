class Anything:
    '''
    A stub class which will repr as a provided name
    '''
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        return self

    def __repr__(self):
        return 'Anything<{}>'.format(self.name)

    @property
    def value(self):
        return None


class Passthrough:
    def __getattr__(self, attr):
        return Anything(attr)


class Pin:
    board = Passthrough()

    def __call__(self, *args, **kwargs):
        return self.board

    def __getattr__(self, attr):
        return getattr(self.board, attr)
