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
        return self._process_tap_dance(keyboard, key, True)

    def td_released(self, key, keyboard, *args, **kwargs):
        return self._process_tap_dance(keyboard, key, False)

    def _process_tap_dance(self, keyboard, changed_key, is_pressed):
        if is_pressed:
            if not isinstance(changed_key.meta, TapDanceKeyMeta):
                # If we get here, changed_key is not a TapDanceKey and thus
                # the user kept typing elsewhere (presumably).  End ALL of the
                # currently outstanding tap dance runs.
                for k, v in self._tap_dance_counts.items():
                    if v:
                        self._end_tap_dance(k)

                return self

            if (
                changed_key not in self._tap_dance_counts
                or not self._tap_dance_counts[changed_key]
            ):
                self._tap_dance_counts[changed_key] = 1
                self._tapping = True
            else:
                keyboard.cancel_timeout(self._tap_timeout)
                self._tap_dance_counts[changed_key] += 1

            if changed_key not in self._tap_side_effects:
                self._tap_side_effects[changed_key] = None

            self._tap_timeout = keyboard.set_timeout(
                self.tap_time, lambda: self._end_tap_dance(keyboard, changed_key, hold=True)
            )
        else:
            if not isinstance(changed_key.meta, TapDanceKeyMeta):
                return self

            has_side_effects = self._tap_side_effects[changed_key] is not None
            hit_max_defined_taps = self._tap_dance_counts[changed_key] == len(
                changed_key.meta.codes
            )

            if has_side_effects or hit_max_defined_taps:
                self._end_tap_dance(keyboard, changed_key)

            keyboard.cancel_timeout(self._tap_timeout)
            self._tap_timeout = keyboard.set_timeout(
                self.tap_time, lambda: self._end_tap_dance(keyboard, changed_key)
            )

        return self

    def _end_tap_dance(self, keyboard, td_key, hold=False):
        v = self._tap_dance_counts[td_key] - 1

        if v < 0:
            return self

        if td_key in keyboard.keys_pressed:
            key_to_press = td_key.meta.codes[v]
            keyboard.add_key(key_to_press)
            self._tap_side_effects[td_key] = key_to_press
        elif self._tap_side_effects[td_key]:
            keyboard.remove_key(self._tap_side_effects[td_key])
            self._tap_side_effects[td_key] = None
            self._cleanup_tap_dance(td_key)
        elif hold is False:
            if td_key.meta.codes[v] in keyboard.keys_pressed:
                keyboard.remove_key(td_key.meta.codes[v])
            else:
                keyboard.tap_key(td_key.meta.codes[v])
            self._cleanup_tap_dance(td_key)
        else:
            keyboard.add_key(td_key.meta.codes[v])

        keyboard.hid_pending = True

        return self

    def _cleanup_tap_dance(self, td_key):
        self._tap_dance_counts[td_key] = 0
        self._tapping = any(count > 0 for count in self._tap_dance_counts.values())
        return self
