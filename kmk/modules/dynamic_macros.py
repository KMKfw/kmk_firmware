from micropython import const
from kmk.modules import Module
from kmk.keys import make_argumented_key, KC

from supervisor import ticks_ms
from kmk.kmktime import ticks_diff, check_deadline


class DMMeta:
    def __init__(self, macro_select=None):
        self.macro_select = macro_select


class MacroStatus:
    STOPPED = const(0)
    RECORDING = const(1)
    PLAYING = const(2)
    SET_REPEPITIONS = const(3)
    SET_INTERVAL = const(4)


# Keycodes for number keys
_numbers = range(KC.N1.code, KC.N0.code + 1)


class Macro:
    def __init__(self):
        self.repetitions = 1
        self.interval = 0
        self.macro_data = [(set(), 0), (set(), 0), (set(), 0)]


class DynamicMacros(Module):
    def __init__(
        self, slots=1, timeout=60000, key_interval=0, use_recorded_speed=False
    ):
        self.macros = [Macro() for i in range(slots)]
        self.current_slot = self.macros[0]
        self.status = MacroStatus.STOPPED

        self.index = 0
        self.start_time = 0
        self.current_repetition = 0
        self.last_config_frame = set()

        self.timeout = timeout
        self.key_interval = key_interval
        self.use_recorded_speed = use_recorded_speed

        # Create keycodes
        make_argumented_key(
            validator=DMMeta, names=("RECORD_MACRO",), on_press=self._record_macro
        )

        make_argumented_key(
            validator=DMMeta, names=("PLAY_MACRO",), on_press=self._play_macro
        )

        make_argumented_key(
            validator=DMMeta,
            names=(
                "SET_MACRO",
                "STOP_MACRO",
            ),
            on_press=self._stop_macro,
        )

        make_argumented_key(
            validator=DMMeta,
            names=("SET_MACRO_REPETITIONS",),
            on_press=self._set_macro_repetitions,
        )

        make_argumented_key(
            validator=DMMeta,
            names=("SET_MACRO_INTERVAL",),
            on_press=self._set_macro_interval,
        )

    def _record_macro(self, key, keyboard, *args, **kwargs):
        self._stop_macro(key, keyboard)
        self.status = MacroStatus.RECORDING
        self.start_time = ticks_ms()
        self.current_slot.macro_data = [(set(), 0)]
        self.index = 0

    def _play_macro(self, key, keyboard, *args, **kwargs):
        self._stop_macro(key, keyboard)
        self.status = MacroStatus.PLAYING
        self.start_time = ticks_ms()
        self.index = 0
        self.current_repetition = 0

    def _stop_macro(self, key, keyboard, *args, **kwargs):
        if self.status == MacroStatus.RECORDING:
            self.stop_recording()
        elif self.status == MacroStatus.SET_INTERVAL:
            self.stop_config()
        self.status = MacroStatus.STOPPED

        # Change macros here because stop is always called
        if key.meta.macro_select is not None:
            self.current_slot = self.macros[key.meta.macro_select]

    # Configure repeat settings
    def _set_macro_repetitions(self, key, keyboard, *args, **kwargs):
        self._stop_macro(key, keyboard)
        self.status = MacroStatus.SET_REPEPITIONS
        self.last_config_frame = set()
        self.current_slot.repetitions = 0
        self.start_time = ticks_ms()

    def _set_macro_interval(self, key, keyboard, *args, **kwargs):
        self._stop_macro(key, keyboard)
        self.status = MacroStatus.SET_INTERVAL
        self.last_config_frame = set()
        self.current_slot.interval = 0
        self.start_time = ticks_ms()

    # Add the current keypress state to the macro
    def record_frame(self, keys_pressed):
        if self.current_slot.macro_data[self.index][0] != keys_pressed:
            self.index += 1

            # Recorded speed
            if self.use_recorded_speed:
                self.current_slot.macro_data.append(
                    (keys_pressed.copy(), ticks_diff(ticks_ms(), self.start_time))
                )

            # Constant speed
            else:
                self.current_slot.macro_data.append(
                    (keys_pressed.copy(), self.index * self.key_interval)
                )

        if not check_deadline(ticks_ms(), self.start_time, self.timeout):
            self.stop_recording()

    # Add the ending frames to the macro
    def stop_recording(self):
        # Clear the remaining keys
        self.current_slot.macro_data.append(
            (set(), self.current_slot.macro_data[-1][1] + 20)
        )

        # Wait for the specified interval
        self.current_slot.macro_data.append(
            (
                set(),
                self.current_slot.macro_data[-1][1] + self.current_slot.interval * 1000,
            )
        )

        self.status = MacroStatus.STOPPED

    def play_frame(self, keyboard):
        # Send the keypresses at this point in the macro
        if not check_deadline(
            ticks_ms(), self.start_time, self.current_slot.macro_data[self.index][1]
        ):
            if self.index:
                for key in self.current_slot.macro_data[self.index - 1][0].difference(
                    self.current_slot.macro_data[self.index][0]
                ):
                    keyboard.remove_key(key)
                for key in self.current_slot.macro_data[self.index][0].difference(
                    self.current_slot.macro_data[self.index - 1][0]
                ):
                    keyboard.add_key(key)

            self.index += 1
            if self.index >= len(self.current_slot.macro_data):  # Reached the end
                self.current_repetition += 1
                if self.current_repetition == self.current_slot.repetitions:
                    self.status = MacroStatus.STOPPED
                else:
                    self.index = 0
                    self.start_time = ticks_ms()

    # Configuration for repeating macros
    def config_mode(self, keyboard):
        for key in keyboard.keys_pressed.difference(self.last_config_frame):
            if key.code in _numbers:
                if self.status == MacroStatus.SET_REPEPITIONS:
                    self.current_slot.repetitions = (
                        self.current_slot.repetitions * 10
                        + ((key.code - KC.N1.code + 1) % 10)
                    )
                elif self.status == MacroStatus.SET_INTERVAL:
                    self.current_slot.interval = self.current_slot.interval * 10 + (
                        (key.code - KC.N1.code + 1) % 10
                    )

            elif key.code == KC.ENTER.code:
                self.stop_config()

        self.last_config_frame = keyboard.keys_pressed.copy()
        keyboard.hid_pending = False  # Disable typing

        if not check_deadline(ticks_ms(), self.start_time, self.timeout):
            self.stop_config()

    # Finish configuring repetitions
    def stop_config(self):
        self.current_slot.macro_data[-1] = (
            self.current_slot.macro_data[-1][0],
            self.current_slot.macro_data[-2][1] + self.current_slot.interval * 1000,
        )
        self.current_slot.repetitions = max(self.current_slot.repetitions, 1)
        self.status = MacroStatus.STOPPED

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

        elif self.status == MacroStatus.RECORDING:
            self.record_frame(keyboard.keys_pressed)

        elif self.status == MacroStatus.PLAYING:
            self.play_frame(keyboard)

        elif (
            self.status == MacroStatus.SET_REPEPITIONS
            or self.status == MacroStatus.SET_INTERVAL
        ):
            self.config_mode(keyboard)

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return
