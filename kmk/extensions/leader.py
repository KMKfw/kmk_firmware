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

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard, matrix_update):
        if self._mode % 2 == 1:
            keys_pressed = keyboard.keys_pressed

            if self._assembly_last_len and self._sequence_assembly:
                history_set = set(self._sequence_assembly)

                keys_pressed = keys_pressed - history_set

            self._assembly_last_len = len(keyboard.keys_pressed)

            for key in keys_pressed:
                if self._mode == LeaderMode.ENTER_ACTIVE and key == KC.ENT:
                    self._handle_leader_sequence(keyboard)
                elif key in (KC.ESC, KC.GESC):
                    # Clean self and turn leader mode off.
                    self._exit_leader_mode(keyboard)
                    break
                elif key == KC.LEAD:
                    break
                else:
                    # Add key if not needing to escape
                    # This needs replaced later with a proper debounce
                    self._sequence_assembly.append(key)

            keyboard.hid_pending = False

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    @staticmethod
    def _compile_sequences(sequences):

        for k, v in sequences.items():
            if not isinstance(k, tuple):
                new_key = tuple(KC[c] for c in k)
                sequences[new_key] = v

        for k, v in sequences.items():
            if not isinstance(k, tuple):
                del sequences[k]

        return sequences

    def _handle_leader_sequence(self, keyboard):
        lmh = tuple(self._sequence_assembly)
        # Will get caught in infinite processing loops if we don't
        # exit leader mode before processing the target key
        self._exit_leader_mode(keyboard)

        if lmh in self._sequences:
            # Stack depth exceeded if try to use add_key here with a unicode sequence
            keyboard.process_key(self._sequences[lmh], True)

            keyboard.set_timeout(
                False, lambda: keyboard.remove_key(self._sequences[lmh])
            )

    def _exit_leader_mode(self, keyboard):
        self._sequence_assembly.clear()
        self._mode -= 1
        self._assembly_last_len = 0
        keyboard.keys_pressed.clear()

    def _key_leader_pressed(self, key, keyboard):
        if self._mode % 2 == 0:
            keyboard.keys_pressed.discard(key)
            # All leader modes are one number higher when activating
            self._mode += 1

            if self._mode == LeaderMode.TIMEOUT_ACTIVE:
                keyboard.set_timeout(
                    self._timeout, lambda: self._handle_leader_sequence(keyboard)
                )
