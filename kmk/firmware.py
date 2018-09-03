from kmk.common.keymap import KEY_DOWN_EVENT, KEY_UP_EVENT, Keymap

try:
    from kmk.circuitpython.matrix import MatrixScanner
except ImportError:
    from kmk.micropython.matrix import MatrixScanner


class ReduxStore:
    def __init__(self, reducer):
        self.reducer = reducer
        self.state = self.reducer()

    def dispatch(self, action):
        self.state = self.reducer(self.state, action)

    def get_state(self):
        return self.state


class InternalState:
    modifiers_pressed = frozenset()
    keys_pressed = frozenset()

    def __repr__(self):
        return 'InternalState(mods={}, keys={})'.format(
            self.modifiers_pressed,
            self.keys_pressed,
        )

    def copy(self, modifiers_pressed=None, keys_pressed=None):
        new_state = InternalState()

        if modifiers_pressed is None:
            new_state.modifiers_pressed = self.modifiers_pressed.copy()
        else:
            new_state.modifiers_pressed = modifiers_pressed

        if keys_pressed is None:
            new_state.keys_pressed = self.keys_pressed.copy()
        else:
            new_state.keys_pressed = keys_pressed

        return new_state


def reducer(state=None, action=None):
    if state is None:
        state = InternalState()

    if action is None:
        return state

    if action['type'] == KEY_UP_EVENT:
        new_state = state.copy(keys_pressed=frozenset(
            key for key in state.keys_pressed if key != action['keycode']
        ))

        print(new_state)

        return new_state

    if action['type'] == KEY_DOWN_EVENT:
        new_state = state.copy(keys_pressed=(
            state.keys_pressed | {action['keycode']}
        ))

        print(new_state)

        return new_state


class Firmware:
    def __init__(self, keymap, row_pins, col_pins, diode_orientation):
        self.raw_keymap = keymap
        self.keymap = Keymap(keymap)
        self.matrix = MatrixScanner(col_pins, row_pins, diode_orientation)
        self.store = ReduxStore(reducer)

    def go(self):
        while True:
            self.keymap.parse(self.matrix.raw_scan(), store=self.store)
