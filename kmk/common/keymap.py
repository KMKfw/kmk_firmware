from kmk.common.event_defs import key_down_event, key_up_event


class Keymap:
    def __init__(self, map):
        self.map = map

    def parse(self, matrix, store):
        state = store.get_state()

        for ridx, row in enumerate(matrix):
            for cidx, col in enumerate(row):
                if col != state.matrix[ridx][cidx]:
                    if col:
                        store.dispatch(key_down_event(
                            row=ridx,
                            col=cidx,
                            keycode=self.map[ridx][cidx],
                        ))
                    else:
                        store.dispatch(key_up_event(
                            row=ridx,
                            col=cidx,
                            keycode=self.map[ridx][cidx],
                        ))
