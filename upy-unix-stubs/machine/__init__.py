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


class Pin:
    board = Passthrough()
