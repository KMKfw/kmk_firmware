class Keymap:
    def __init__(self, map):
        self.map = map
        self.state = [
            [False for _ in row]
            for row in self.map
        ]

    def parse(self, matrix):
        for ridx, row in enumerate(matrix):
            for cidx, col in enumerate(row):
                if col != self.state[ridx][cidx]:
                    print('{}: {}'.format(
                        'KEYDOWN' if col else 'KEYUP',
                        self.map[ridx][cidx],
                    ))

        self.state = matrix
