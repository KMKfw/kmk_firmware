import math

from kmk.event_defs import (hid_report_event, keycode_down_event,
                            keycode_up_event)
from kmk.keycodes import Media
from kmk.rotary_encoder import RotaryEncoder

VAL_FALSE = False + 1
VAL_NONE = True + 2
VAL_TRUE = True + 1
VOL_UP_PRESS = keycode_down_event(Media.KC_AUDIO_VOL_UP)
VOL_UP_RELEASE = keycode_up_event(Media.KC_AUDIO_VOL_UP)
VOL_DOWN_PRESS = keycode_down_event(Media.KC_AUDIO_VOL_DOWN)
VOL_DOWN_RELEASE = keycode_up_event(Media.KC_AUDIO_VOL_DOWN)


class RotaryEncoderMacro:
    def __init__(self, pos_pin, neg_pin, slop_history=1, slop_threshold=1):
        self.encoder = RotaryEncoder(pos_pin, neg_pin)
        self.max_history = slop_history
        self.history = bytearray(slop_history)
        self.history_idx = 0
        self.history_threshold = math.floor(slop_threshold * slop_history)

    def scan(self):
        # Anti-slop logic
        self.history[self.history_idx] = 0

        reading = self.encoder.direction()
        self.history[self.history_idx] = VAL_NONE if reading is None else reading + 1

        self.history_idx += 1

        if self.history_idx >= self.max_history:
            self.history_idx = 0

        nones = 0
        trues = 0
        falses = 0

        for val in self.history:
            if val == VAL_NONE:
                nones += 1
            elif val == VAL_TRUE:
                trues += 1
            elif val == VAL_FALSE:
                falses += 1

        if nones >= self.history_threshold:
            return None

        if trues >= self.history_threshold:
            return self.on_increase()

        if falses >= self.history_threshold:
            return self.on_decrease()

    def on_decrease(self):
        pass

    def on_increase(self):
        pass


class VolumeRotaryEncoder(RotaryEncoderMacro):
    def on_decrease(self):
        yield VOL_DOWN_PRESS
        yield hid_report_event
        yield VOL_DOWN_RELEASE
        yield hid_report_event

    def on_increase(self):
        yield VOL_UP_PRESS
        yield hid_report_event
        yield VOL_UP_RELEASE
        yield hid_report_event
