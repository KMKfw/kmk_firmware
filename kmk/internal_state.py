from kmk.consts import LeaderMode
from kmk.keys import KC
from kmk.kmktime import ticks_ms
from kmk.matrix import intify_coordinate
from kmk.types import TapDanceKeyMeta


class InternalState:
    keys_pressed = set()
    coord_keys_pressed = {}
    leader_pending = None
    leader_last_len = 0
    hid_pending = False
    leader_mode_history = []

    # this should almost always be PREpended to, replaces
    # former use of reversed_active_layers which had pointless
    # overhead (the underlying list was never used anyway)
    active_layers = [0]

    start_time = {'lt': None, 'tg': None, 'tt': None, 'lm': None, 'leader': None}
    timeouts = {}
    tapping = False
    tap_dance_counts = {}
    tap_side_effects = {}

    def __init__(self, config):
        self.config = config

    def __repr__(self):
        return (
            'InternalState('
            'keys_pressed={} '
            'coord_keys_pressed={} '
            'leader_pending={} '
            'leader_last_len={} '
            'hid_pending={} '
            'leader_mode_history={} '
            'active_layers={} '
            'start_time={} '
            'timeouts={} '
            'tapping={} '
            'tap_dance_counts={} '
            'tap_side_effects={}'
            ')'
        ).format(
            self.keys_pressed,
            self.coord_keys_pressed,
            self.leader_pending,
            self.leader_last_len,
            self.hid_pending,
            self.leader_mode_history,
            self.active_layers,
            self.start_time,
            self.timeouts,
            self.tapping,
            self.tap_dance_counts,
            self.tap_side_effects,
        )

    def _find_key_in_map(self, row, col):
        ic = intify_coordinate(row, col)

        try:
            idx = self.config.coord_mapping.index(ic)
        except ValueError:
            if self.config.debug_enabled:
                print(
                    'CoordMappingNotFound(ic={}, row={}, col={})'.format(ic, row, col)
                )

            return None

        for layer in self.active_layers:
            layer_key = self.config.keymap[layer][idx]

            if not layer_key or layer_key == KC.TRNS:
                continue

            if self.config.debug_enabled:
                print('KeyResolution(key={})'.format(layer_key))

            return layer_key

    def set_timeout(self, after_ticks, callback):
        if after_ticks is False:
            # We allow passing False as an implicit "run this on the next process timeouts cycle"
            timeout_key = ticks_ms()
        else:
            timeout_key = ticks_ms() + after_ticks

        while timeout_key in self.timeouts:
            timeout_key += 1

        self.timeouts[timeout_key] = callback
        return timeout_key

    def cancel_timeout(self, timeout_key):
        if timeout_key in self.timeouts:
            del self.timeouts[timeout_key]

    def process_timeouts(self):
        if not self.timeouts:
            return self

        current_time = ticks_ms()

        # cast this to a tuple to ensure that if a callback itself sets
        # timeouts, we do not handle them on the current cycle
        timeouts = tuple(self.timeouts.items())

        for k, v in timeouts:
            if k <= current_time:
                v()
                del self.timeouts[k]

        return self

    def matrix_changed(self, row, col, is_pressed):
        if self.config.debug_enabled:
            print('MatrixChange(col={} row={} pressed={})'.format(col, row, is_pressed))

        int_coord = intify_coordinate(row, col)
        kc_changed = self._find_key_in_map(row, col)

        if kc_changed is None:
            print('MatrixUndefinedCoordinate(col={} row={})'.format(col, row))
            return self

        return self.process_key(kc_changed, is_pressed, int_coord, (row, col))

    def process_key(self, key, is_pressed, coord_int=None, coord_raw=None):
        if self.tapping and not isinstance(key.meta, TapDanceKeyMeta):
            self._process_tap_dance(key, is_pressed)
        else:
            if is_pressed:
                key._on_press(self, coord_int, coord_raw)
            else:
                key._on_release(self, coord_int, coord_raw)

            if self.config.leader_mode % 2 == 1:
                self._process_leader_mode()

        return self

    def remove_key(self, keycode):
        self.keys_pressed.discard(keycode)
        return self.process_key(keycode, False)

    def add_key(self, keycode):
        self.keys_pressed.add(keycode)
        return self.process_key(keycode, True)

    def tap_key(self, keycode):
        self.add_key(keycode)
        # On the next cycle, we'll remove the key.
        self.set_timeout(False, lambda: self.remove_key(keycode))

        return self

    def resolve_hid(self):
        self.hid_pending = False
        return self

    def _process_tap_dance(self, changed_key, is_pressed):
        if is_pressed:
            if not isinstance(changed_key.meta, TapDanceKeyMeta):
                # If we get here, changed_key is not a TapDanceKey and thus
                # the user kept typing elsewhere (presumably).  End ALL of the
                # currently outstanding tap dance runs.
                for k, v in self.tap_dance_counts.items():
                    if v:
                        self._end_tap_dance(k)

                return self

            if (
                changed_key not in self.tap_dance_counts
                or not self.tap_dance_counts[changed_key]
            ):
                self.tap_dance_counts[changed_key] = 1
                self.set_timeout(
                    self.config.tap_time, lambda: self._end_tap_dance(changed_key)
                )
                self.tapping = True
            else:
                self.tap_dance_counts[changed_key] += 1

            if changed_key not in self.tap_side_effects:
                self.tap_side_effects[changed_key] = None
        else:
            has_side_effects = self.tap_side_effects[changed_key] is not None
            hit_max_defined_taps = self.tap_dance_counts[changed_key] == len(
                changed_key.codes
            )

            if has_side_effects or hit_max_defined_taps:
                self._end_tap_dance(changed_key)

        return self

    def _end_tap_dance(self, td_key):
        v = self.tap_dance_counts[td_key] - 1

        if v >= 0:
            if td_key in self.keys_pressed:
                key_to_press = td_key.codes[v]
                self.add_key(key_to_press)
                self.tap_side_effects[td_key] = key_to_press
                self.hid_pending = True
            else:
                if self.tap_side_effects[td_key]:
                    self.remove_key(self.tap_side_effects[td_key])
                    self.tap_side_effects[td_key] = None
                    self.hid_pending = True
                    self._cleanup_tap_dance(td_key)
                else:
                    self.tap_key(td_key.codes[v])
                    self._cleanup_tap_dance(td_key)

        return self

    def _cleanup_tap_dance(self, td_key):
        self.tap_dance_counts[td_key] = 0
        self.tapping = any(count > 0 for count in self.tap_dance_counts.values())
        return self

    def _begin_leader_mode(self):
        if self.config.leader_mode % 2 == 0:
            self.keys_pressed.discard(KC.LEAD)
            # All leader modes are one number higher when activating
            self.config.leader_mode += 1

            if self.config.leader_mode == LeaderMode.TIMEOUT_ACTIVE:
                self.set_timeout(
                    self.config.leader_timeout, self._handle_leader_sequence
                )

        return self

    def _handle_leader_sequence(self):
        lmh = tuple(self.leader_mode_history)
        # Will get caught in infinite processing loops if we don't
        # exit leader mode before processing the target key
        self._exit_leader_mode()

        if lmh in self.config.leader_dictionary:
            # Stack depth exceeded if try to use add_key here with a unicode sequence
            self.process_key(self.config.leader_dictionary[lmh], True)

            self.set_timeout(
                False, lambda: self.remove_key(self.config.leader_dictionary[lmh])
            )

        return self

    def _process_leader_mode(self):
        keys_pressed = self.keys_pressed

        if self.leader_last_len and self.leader_mode_history:
            history_set = set(self.leader_mode_history)

            keys_pressed = keys_pressed - history_set

        self.leader_last_len = len(self.keys_pressed)

        for key in keys_pressed:
            if self.config.leader_mode == LeaderMode.ENTER_ACTIVE and key == KC.ENT:
                self._handle_leader_sequence()
                break
            elif key == KC.ESC or key == KC.GESC:
                # Clean self and turn leader mode off.
                self._exit_leader_mode()
                break
            elif key == KC.LEAD:
                break
            else:
                # Add key if not needing to escape
                # This needs replaced later with a proper debounce
                self.leader_mode_history.append(key)

        self.hid_pending = False
        return self

    def _exit_leader_mode(self):
        self.leader_mode_history.clear()
        self.config.leader_mode -= 1
        self.leader_last_len = 0
        self.keys_pressed.clear()
        return self
