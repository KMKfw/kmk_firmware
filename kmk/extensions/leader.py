import gc

from kmk.extensions import Extension, InvalidExtensionEnvironment
from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.keys import KC, make_key


class LeaderMode:
    TIMEOUT = 0
    TIMEOUT_ACTIVE = 1
    ENTER = 2
    ENTER_ACTIVE = 3


class Leader(Extension):
    def __init__(self, mode=LeaderMode.TIMEOUT, timeout=1000, sequences=None):
        if sequences is None:
            raise InvalidExtensionEnvironment(
                'sequences must be a dictionary, not None'
            )

        self._mode = mode
        self._timeout = timeout
        self._sequences = self._compile_sequences(sequences)

        self._leader_pending = None
        self._assembly_last_len = 0
        self._sequence_assembly = []

        make_key(
            names=('LEADER', 'LEAD'),
            on_press=self._key_leader_pressed,
            on_release=handler_passthrough,
        )

        gc.collect()

    def after_matrix_scan(self, keyboard_state, *args):
        if self._mode % 2 == 1:
            keys_pressed = keyboard_state._keys_pressed

            if self._assembly_last_len and self._sequence_assembly:
                history_set = set(self._sequence_assembly)

                keys_pressed = keys_pressed - history_set

            self._assembly_last_len = len(keyboard_state._keys_pressed)

            for key in keys_pressed:
                if self._mode == LeaderMode.ENTER_ACTIVE and key == KC.ENT:
                    self._handle_leader_sequence(keyboard_state)
                    break
                elif key == KC.ESC or key == KC.GESC:
                    # Clean self and turn leader mode off.
                    self._exit_leader_mode(keyboard_state)
                    break
                elif key == KC.LEAD:
                    break
                else:
                    # Add key if not needing to escape
                    # This needs replaced later with a proper debounce
                    self._sequence_assembly.append(key)

            keyboard_state._hid_pending = False

    def _compile_sequences(self, sequences):
        gc.collect()

        for k, v in sequences.items():
            if not isinstance(k, tuple):
                new_key = tuple(KC[c] for c in k)
                sequences[new_key] = v

        for k, v in sequences.items():
            if not isinstance(k, tuple):
                del sequences[k]

        gc.collect()

        return sequences

    def _handle_leader_sequence(self, keyboard_state):
        lmh = tuple(self._sequence_assembly)
        # Will get caught in infinite processing loops if we don't
        # exit leader mode before processing the target key
        self._exit_leader_mode(keyboard_state)

        if lmh in self._sequences:
            # Stack depth exceeded if try to use add_key here with a unicode sequence
            keyboard_state._process_key(self._sequences[lmh], True)

            keyboard_state._set_timeout(
                False, lambda: keyboard_state._remove_key(self._sequences[lmh])
            )

    def _exit_leader_mode(self, keyboard_state):
        self._sequence_assembly.clear()
        self._mode -= 1
        self._assembly_last_len = 0
        keyboard_state._keys_pressed.clear()

    def _key_leader_pressed(self, key, keyboard_state, *args, **kwargs):
        if self._mode % 2 == 0:
            keyboard_state._keys_pressed.discard(key)
            # All leader modes are one number higher when activating
            self._mode += 1

            if self._mode == LeaderMode.TIMEOUT_ACTIVE:
                keyboard_state._set_timeout(
                    self._timeout, lambda: self._handle_leader_sequence(keyboard_state)
                )
