from micropython import const
from supervisor import ticks_ms

from collections import namedtuple

from kmk.keys import KC, make_argumented_key
from kmk.kmktime import check_deadline, ticks_diff
from kmk.modules import Module


class DSMeta:
    def __init__(self, sequence_select=None):
        self.sequence_select = sequence_select


class SequenceStatus:
    STOPPED = const(0)
    RECORDING = const(1)
    PLAYING = const(2)
    SET_REPEPITIONS = const(3)
    SET_INTERVAL = const(4)


# Keycodes for number keys
_numbers = range(KC.N1.code, KC.N0.code + 1)

SequenceFrame = namedtuple('SequenceFrame', ['keys_pressed', 'timestamp'])


class Sequence:
    def __init__(self):
        self.repetitions = 1
        self.interval = 0
        self.sequence_data = [SequenceFrame(set(), 0) for i in range(3)]


class DynamicSequences(Module):
    def __init__(
        self, slots=1, timeout=60000, key_interval=0, use_recorded_speed=False
    ):
        self.sequences = [Sequence() for i in range(slots)]
        self.current_slot = self.sequences[0]
        self.status = SequenceStatus.STOPPED

        self.index = 0
        self.start_time = 0
        self.current_repetition = 0
        self.last_config_frame = set()

        self.timeout = timeout
        self.key_interval = key_interval
        self.use_recorded_speed = use_recorded_speed

        # Create keycodes
        make_argumented_key(
            validator=DSMeta, names=('RECORD_SEQUENCE',), on_press=self._record_sequence
        )

        make_argumented_key(
            validator=DSMeta, names=('PLAY_SEQUENCE',), on_press=self._play_sequence
        )

        make_argumented_key(
            validator=DSMeta,
            names=(
                'SET_SEQUENCE',
                'STOP_SEQUENCE',
            ),
            on_press=self._stop_sequence,
        )

        make_argumented_key(
            validator=DSMeta,
            names=('SET_SEQUENCE_REPETITIONS',),
            on_press=self._set_sequence_repetitions,
        )

        make_argumented_key(
            validator=DSMeta,
            names=('SET_SEQUENCE_INTERVAL',),
            on_press=self._set_sequence_interval,
        )

    def _record_sequence(self, key, keyboard, *args, **kwargs):
        self._stop_sequence(key, keyboard)
        self.status = SequenceStatus.RECORDING
        self.start_time = ticks_ms()
        self.current_slot.sequence_data = [SequenceFrame(set(), 0)]
        self.index = 0

    def _play_sequence(self, key, keyboard, *args, **kwargs):
        self._stop_sequence(key, keyboard)
        self.status = SequenceStatus.PLAYING
        self.start_time = ticks_ms()
        self.index = 0
        self.current_repetition = 0

    def _stop_sequence(self, key, keyboard, *args, **kwargs):
        if self.status == SequenceStatus.RECORDING:
            self.stop_recording()
        elif self.status == SequenceStatus.SET_INTERVAL:
            self.stop_config()
        self.status = SequenceStatus.STOPPED

        # Change sequences here because stop is always called
        if key.meta.sequence_select is not None:
            self.current_slot = self.sequences[key.meta.sequence_select]

    # Configure repeat settings
    def _set_sequence_repetitions(self, key, keyboard, *args, **kwargs):
        self._stop_sequence(key, keyboard)
        self.status = SequenceStatus.SET_REPEPITIONS
        self.last_config_frame = set()
        self.current_slot.repetitions = 0
        self.start_time = ticks_ms()

    def _set_sequence_interval(self, key, keyboard, *args, **kwargs):
        self._stop_sequence(key, keyboard)
        self.status = SequenceStatus.SET_INTERVAL
        self.last_config_frame = set()
        self.current_slot.interval = 0
        self.start_time = ticks_ms()

    # Add the current keypress state to the sequence
    def record_frame(self, keys_pressed):
        if self.current_slot.sequence_data[self.index].keys_pressed != keys_pressed:
            self.index += 1

            # Recorded speed
            if self.use_recorded_speed:
                self.current_slot.sequence_data.append(
                    SequenceFrame(
                        keys_pressed.copy(), ticks_diff(ticks_ms(), self.start_time)
                    )
                )

            # Constant speed
            else:
                self.current_slot.sequence_data.append(
                    SequenceFrame(keys_pressed.copy(), self.index * self.key_interval)
                )

        if not check_deadline(ticks_ms(), self.start_time, self.timeout):
            self.stop_recording()

    # Add the ending frames to the sequence
    def stop_recording(self):
        # Clear the remaining keys
        self.current_slot.sequence_data.append(
            SequenceFrame(set(), self.current_slot.sequence_data[-1].timestamp + 20)
        )

        # Wait for the specified interval
        prev_timestamp = self.current_slot.sequence_data[-1].timestamp
        self.current_slot.sequence_data.append(
            SequenceFrame(
                set(),
                prev_timestamp + self.current_slot.interval * 1000,
            )
        )

        self.status = SequenceStatus.STOPPED

    def play_frame(self, keyboard):
        # Send the keypresses at this point in the sequence
        if not check_deadline(
            ticks_ms(),
            self.start_time,
            self.current_slot.sequence_data[self.index].timestamp,
        ):
            if self.index:
                prev = self.current_slot.sequence_data[self.index - 1].keys_pressed
                cur = self.current_slot.sequence_data[self.index].keys_pressed

                for key in prev.difference(cur):
                    keyboard.remove_key(key)
                for key in cur.difference(prev):
                    keyboard.add_key(key)

            self.index += 1
            if self.index >= len(self.current_slot.sequence_data):  # Reached the end
                self.current_repetition += 1
                if self.current_repetition == self.current_slot.repetitions:
                    self.status = SequenceStatus.STOPPED
                else:
                    self.index = 0
                    self.start_time = ticks_ms()

    # Configuration for repeating sequences
    def config_mode(self, keyboard):
        for key in keyboard.keys_pressed.difference(self.last_config_frame):
            if key.code in _numbers:
                digit = (key.code - KC.N1.code + 1) % 10
                if self.status == SequenceStatus.SET_REPEPITIONS:
                    self.current_slot.repetitions = (
                        self.current_slot.repetitions * 10 + digit
                    )
                elif self.status == SequenceStatus.SET_INTERVAL:
                    self.current_slot.interval = self.current_slot.interval * 10 + digit

            elif key.code == KC.ENTER.code:
                self.stop_config()

        self.last_config_frame = keyboard.keys_pressed.copy()
        keyboard.hid_pending = False  # Disable typing

        if not check_deadline(ticks_ms(), self.start_time, self.timeout):
            self.stop_config()

    # Finish configuring repetitions
    def stop_config(self):
        self.current_slot.sequence_data[-1] = SequenceFrame(
            self.current_slot.sequence_data[-1].keys_pressed,
            self.current_slot.sequence_data[-2].timestamp
            + self.current_slot.interval * 1000,
        )
        self.current_slot.repetitions = max(self.current_slot.repetitions, 1)
        self.status = SequenceStatus.STOPPED

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):

        if not self.status:
            return

        elif self.status == SequenceStatus.RECORDING:
            self.record_frame(keyboard.keys_pressed)

        elif self.status == SequenceStatus.PLAYING:
            self.play_frame(keyboard)

        elif (
            self.status == SequenceStatus.SET_REPEPITIONS
            or self.status == SequenceStatus.SET_INTERVAL
        ):
            self.config_mode(keyboard)

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return
