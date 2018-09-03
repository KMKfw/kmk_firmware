KEY_UP_EVENT = 'KEY_UP'
KEY_DOWN_EVENT = 'KEY_DOWN'


def key_up_event(keycode):
    return {
        'type': KEY_UP_EVENT,
        'keycode': keycode,
    }


def key_down_event(keycode):
    return {
        'type': KEY_DOWN_EVENT,
        'keycode': keycode,
    }


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
