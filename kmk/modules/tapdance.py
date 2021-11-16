from kmk.key_validators import tap_dance_key_validator
from kmk.keys import make_argumented_key
from kmk.modules import Module
from kmk.types import TapDanceKeyMeta


class TapDance(Module):
    # User-configurable
    tap_time = 300

    # Internal State
    _tapping = False
    _tap_dance_counts = {}
    _tap_timeout = None
    _tap_side_effects = {}

    def __init__(self):
        make_argumented_key(
            validator=tap_dance_key_validator,
            names=('TAP_DANCE', 'TD'),
            on_press=self.td_pressed,
            on_release=self.td_released,
        )

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def td_pressed(self, key, keyboard, *args, **kwargs):
        if not isinstance(key.meta, TapDanceKeyMeta):
            # If we get here, key is not a TapDanceKey and thus
            # the user kept typing elsewhere (presumably).  End ALL of the
            # currently outstanding tap dance runs.
            for k, v in self._tap_dance_counts.items():
                if v:
                    self._end_tap_dance(k)

            return self

        if (
            key not in self._tap_dance_counts
            or not self._tap_dance_counts[key]
        ):
            self._tap_dance_counts[key] = 1
            self._tapping = True
        else:
            keyboard.cancel_timeout(self._tap_timeout)
            self._tap_dance_counts[key] += 1

        if key not in self._tap_side_effects:
            self._tap_side_effects[key] = None

        self._tap_timeout = keyboard.set_timeout(
            self.tap_time, lambda: self._end_tap_dance(keyboard, key, hold=True)
        )
        return self

    def td_released(self, key, keyboard, *args, **kwargs):
        if not isinstance(key.meta, TapDanceKeyMeta):
            return self

        has_side_effects = self._tap_side_effects[key] is not None
        hit_max_defined_taps = self._tap_dance_counts[key] == len(
            key.meta.codes
        )

        if has_side_effects or hit_max_defined_taps:
            self._end_tap_dance(keyboard, key)

        keyboard.cancel_timeout(self._tap_timeout)
        self._tap_timeout = keyboard.set_timeout(
            self.tap_time, lambda: self._end_tap_dance(keyboard, key)
        )

        return self

    def _end_tap_dance(self, keyboard, key, hold=False):
        v = self._tap_dance_counts[key] - 1

        if v < 0:
            return self

        if key in keyboard.keys_pressed:
            key_to_press = key.meta.codes[v]
            keyboard.add_key(key_to_press)
            self._tap_side_effects[key] = key_to_press
        elif self._tap_side_effects[key]:
            keyboard.remove_key(self._tap_side_effects[key])
            self._tap_side_effects[key] = None
            self._cleanup_tap_dance(key)
        elif hold is False:
            if key.meta.codes[v] in keyboard.keys_pressed:
                keyboard.remove_key(key.meta.codes[v])
            else:
                keyboard.tap_key(key.meta.codes[v])
            self._cleanup_tap_dance(key)
        else:
            keyboard.add_key(key.meta.codes[v])

        keyboard.hid_pending = True

        return self

    def _cleanup_tap_dance(self, key):
        self._tap_dance_counts[key] = 0
        self._tapping = any(count > 0 for count in self._tap_dance_counts.values())
        return self
