from kmk.common.event_defs import key_down_event, key_up_event


class Keymap:
    def __init__(self, map):
        self.map = map
        self.state = [
            [False for _ in row]
            for row in self.map
        ]

    def parse(self, matrix, store):
        for ridx, row in enumerate(matrix):
            for cidx, col in enumerate(row):
                if col != self.state[ridx][cidx]:
                    if col:
                        store.dispatch(key_down_event(self.map[ridx][cidx]))
                    else:
                        store.dispatch(key_up_event(self.map[ridx][cidx]))

        self.state = matrix
