from kmk.consts import LeaderMode
from kmk.keycodes import (FIRST_KMK_INTERNAL_KEYCODE, Keycodes, RawKeycodes,
                          TapDanceKeycode)
from kmk.kmktime import sleep_ms, ticks_diff, ticks_ms
from kmk.util import intify_coordinate

GESC_TRIGGERS = {
    Keycodes.Modifiers.KC_LSHIFT, Keycodes.Modifiers.KC_RSHIFT,
    Keycodes.Modifiers.KC_LGUI, Keycodes.Modifiers.KC_RGUI,
}


class InternalState:
    keys_pressed = set()
    coord_keys_pressed = {}
    macros_pending = []
    leader_pending = None
    leader_last_len = 0
    hid_pending = False
    leader_mode_history = []
    active_layers = [0]
    reversed_active_layers = list(reversed(active_layers))
    start_time = {
        'lt': None,
        'tg': None,
        'tt': None,
        'lm': None,
        'leader': None,
    }
    timeouts = {}
    tapping = False
    tap_dance_counts = {}
    tap_side_effects = {}

    def __init__(self, config):
        self.config = config
        self.internal_key_handlers = {
            RawKeycodes.KC_DF: self._layer_df,
            RawKeycodes.KC_MO: self._layer_mo,
            RawKeycodes.KC_LM: self._layer_lm,
            RawKeycodes.KC_LT: self._layer_lt,
            RawKeycodes.KC_TG: self._layer_tg,
            RawKeycodes.KC_TO: self._layer_to,
            RawKeycodes.KC_TT: self._layer_tt,
            Keycodes.KMK.KC_GESC.code: self._kc_gesc,
            RawKeycodes.KC_UC_MODE: self._kc_uc_mode,
            RawKeycodes.KC_MACRO: self._kc_macro,
            Keycodes.KMK.KC_LEAD.code: self._kc_lead,
            Keycodes.KMK.KC_NO.code: self._kc_no,
            Keycodes.KMK.KC_DEBUG.code: self._kc_debug_mode,
            RawKeycodes.KC_TAP_DANCE: self._kc_tap_dance,
        }

    def __repr__(self):
        return 'InternalState({})'.format(self._to_dict())

    def _to_dict(self):
        ret = {
            'keys_pressed': self.keys_pressed,
            'active_layers': self.active_layers,
            'leader_mode_history': self.leader_mode_history,
            'leader_mode': self.config.leader_mode,
            'start_time': self.start_time,
            'tapping': self.tapping,
            'tap_dance_counts': self.tap_dance_counts,
            'timeouts': self.timeouts,
        }

        return ret

    def _find_key_in_map(self, row, col):
        # Later-added layers have priority. Sift through the layers
        # in reverse order until we find a valid keycode object
        for layer in self.reversed_active_layers:
            layer_key = self.config.keymap[layer][row][col]

            if not layer_key or layer_key == Keycodes.KMK.KC_TRNS:
                continue

            if self.config.debug_enabled:
                print('Resolved key: {}'.format(layer_key))

            return layer_key

    def set_timeout(self, after_ticks, callback):
        if after_ticks is False:
            # We allow passing False as an implicit "run this on the next process timeouts cycle"
            timeout_key = ticks_ms()
        else:
            timeout_key = ticks_ms() + after_ticks

        self.timeouts[timeout_key] = callback
        return self

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
            print('Matrix changed (col, row, pressed?): {}, {}, {}'.format(
                col, row, is_pressed,
            ))

        int_coord = intify_coordinate(row, col)
        kc_changed = self._find_key_in_map(row, col)

        if kc_changed is None:
            print('No key accessible for col, row: {}, {}'.format(row, col))
            return self

        if self.tapping and not isinstance(kc_changed, TapDanceKeycode):
            self._process_tap_dance(kc_changed, is_pressed)
        else:
            if is_pressed:
                self.coord_keys_pressed[int_coord] = kc_changed
                self.add_key(kc_changed)
            else:
                self.remove_key(kc_changed)
                self.keys_pressed.discard(self.coord_keys_pressed.get(int_coord, None))
                self.coord_keys_pressed[int_coord] = None

            if self.config.leader_mode % 2 == 1:
                self._process_leader_mode()

        return self

    def remove_key(self, keycode):
        self.keys_pressed.discard(keycode)

        if keycode.code >= FIRST_KMK_INTERNAL_KEYCODE:
            self._process_internal_key_event(keycode, False)
        else:
            self.hid_pending = True

        return self

    def add_key(self, keycode):
        # TODO Make this itself a macro keycode with a keyup handler
        #      rather than handling this inline here. Gross.
        if keycode.code == Keycodes.KMK.KC_MACRO_SLEEP_MS:
            sleep_ms(keycode.ms)
        else:
            self.keys_pressed.add(keycode)

            if keycode.code >= FIRST_KMK_INTERNAL_KEYCODE:
                self._process_internal_key_event(keycode, True)
            else:
                self.hid_pending = True
        return self

    def tap_key(self, keycode):
        self.add_key(keycode)
        # On the next cycle, we'll remove the key. This is way more clean than
        # the `pending_keys` implementation that we used to rely on in
        # firmware.py
        self.set_timeout(False, lambda: self.remove_key(keycode))

        return self

    def resolve_hid(self):
        self.hid_pending = False
        return self

    def resolve_macro(self):
        if self.config.debug_enabled:
            print('Macro complete!')

        self.macros_pending.pop()
        return self

    def _process_internal_key_event(self, changed_key, is_pressed):
        # Since the key objects can be chained into new objects
        # with, for example, no_press set, always check against
        # the underlying code rather than comparing Keycode
        # objects

        return self.internal_key_handlers[changed_key.code](
            changed_key, is_pressed,
        )

    def _layer_df(self, changed_key, is_pressed):
        """Switches the default layer"""
        if is_pressed:
            self.active_layers[0] = changed_key.layer
            self.reversed_active_layers = list(reversed(self.active_layers))

        return self

    def _layer_mo(self, changed_key, is_pressed):
        """Momentarily activates layer, switches off when you let go"""
        if is_pressed:
            self.active_layers.append(changed_key.layer)
        else:
            self.active_layers = [
                layer for layer in self.active_layers
                if layer != changed_key.layer
            ]

        self.reversed_active_layers = list(reversed(self.active_layers))

        return self

    def _layer_lm(self, changed_key, is_pressed):
        """As MO(layer) but with mod active"""
        self.hid_pending = True

        if is_pressed:
            # Sets the timer start and acts like MO otherwise
            self.start_time['lm'] = ticks_ms()
            self.keys_pressed.add(changed_key.kc)
        else:
            self.keys_pressed.discard(changed_key.kc)
            self.start_time['lm'] = None

        return self._layer_mo(changed_key, is_pressed)

    def _layer_lt(self, changed_key, is_pressed):
        """Momentarily activates layer if held, sends kc if tapped"""
        if is_pressed:
            # Sets the timer start and acts like MO otherwise
            self.start_time['lt'] = ticks_ms()
            self._layer_mo(changed_key, is_pressed)
        else:
            # On keyup, check timer, and press key if needed.
            if self.start_time['lt'] and (
                ticks_diff(ticks_ms(), self.start_time['lt']) < self.config.tap_time
            ):
                self.hid_pending = True
                self.tap_key(changed_key.kc)

            self._layer_mo(changed_key, is_pressed)
            self.start_time['lt'] = None
        return self

    def _layer_tg(self, changed_key, is_pressed):
        """Toggles the layer (enables it if not active, and vise versa)"""
        if is_pressed:
            if changed_key.layer in self.active_layers:
                self.active_layers = [
                    layer for layer in self.active_layers
                    if layer != changed_key.layer
                ]
            else:
                self.active_layers.append(changed_key.layer)

            self.reversed_active_layers = list(reversed(self.active_layers))

        return self

    def _layer_to(self, changed_key, is_pressed):
        """Activates layer and deactivates all other layers"""
        if is_pressed:
            self.active_layers = [changed_key.layer]
            self.reversed_active_layers = list(reversed(self.active_layers))

        return self

    def _layer_tt(self, changed_key, is_pressed):
        """Momentarily activates layer if held, toggles it if tapped repeatedly"""
        # TODO Make this work with tap dance to function more correctly, but technically works.
        if is_pressed:
            if self.start_time['tt'] is None:
                # Sets the timer start and acts like MO otherwise
                self.start_time['tt'] = ticks_ms()
                return self._layer_mo(changed_key, is_pressed)
            elif ticks_diff(ticks_ms(), self.start_time['tt']) < self.config.tap_time:
                self.start_time['tt'] = None
                return self.tg(changed_key, is_pressed)
        elif (
            self.start_time['tt'] is None or
            ticks_diff(ticks_ms(), self.start_time['tt']) >= self.config.tap_time
        ):
            # On first press, works like MO. On second press, does nothing unless let up within
            # time window, then acts like TG.
            self.start_time['tt'] = None
            return self._layer_mo(changed_key, is_pressed)

        return self

    def _kc_uc_mode(self, changed_key, is_pressed):
        if is_pressed:
            self.config.unicode_mode = changed_key.mode

        return self

    def _kc_macro(self, changed_key, is_pressed):
        if is_pressed:
            if changed_key.keyup:
                self.macros_pending.append(changed_key.keyup)
        else:
            if changed_key.keydown:
                self.macros_pending.append(changed_key.keydown)

        return self

    def _kc_lead(self, changed_key, is_pressed):
        if is_pressed:
            self._begin_leader_mode()

        return self

    def _kc_gesc(self, changed_key, is_pressed):
        self.hid_pending = True

        if is_pressed:
            if GESC_TRIGGERS.intersection(self.keys_pressed):
                # if Shift is held, KC_GRAVE will become KC_TILDE on OS level
                self.keys_pressed.add(Keycodes.Common.KC_GRAVE)
                return self

            # else return KC_ESC
            self.keys_pressed.add(Keycodes.Common.KC_ESCAPE)
            return self

        self.keys_pressed.discard(Keycodes.Common.KC_ESCAPE)
        self.keys_pressed.discard(Keycodes.Common.KC_GRAVE)
        return self

    def _kc_no(self, changed_key, is_pressed):
        return self

    def _kc_debug_mode(self, changed_key, is_pressed):
        if is_pressed:
            if self.config.debug_enabled:
                print('Disabling debug mode, bye!')
            else:
                print('Enabling debug mode. Welcome to the jungle.')

            self.config.debug_enabled = not self.config.debug_enabled

        return self

    def _kc_tap_dance(self, changed_key, is_pressed):
        return self._process_tap_dance(changed_key, is_pressed)

    def _process_tap_dance(self, changed_key, is_pressed):
        if is_pressed:
            if not isinstance(changed_key, TapDanceKeycode):
                # If we get here, changed_key is not a TapDanceKeycode and thus
                # the user kept typing elsewhere (presumably).  End ALL of the
                # currently outstanding tap dance runs.
                for k, v in self.tap_dance_counts.items():
                    if v:
                        self._end_tap_dance(k)

                return self

            if (
                changed_key not in self.tap_dance_counts or
                not self.tap_dance_counts[changed_key]
            ):
                self.tap_dance_counts[changed_key] = 1
                self.set_timeout(self.config.tap_time, lambda: self._end_tap_dance(changed_key))
                self.tapping = True
            else:
                self.tap_dance_counts[changed_key] += 1

            if changed_key not in self.tap_side_effects:
                self.tap_side_effects[changed_key] = None
        else:
            if (
                self.tap_side_effects[changed_key] is not None or
                self.tap_dance_counts[changed_key] == len(changed_key.codes)
            ):
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
            self.keys_pressed.discard(Keycodes.KMK.KC_LEAD)
            # All leader modes are one number higher when activating
            self.config.leader_mode += 1

            if self.config.leader_mode == LeaderMode.TIMEOUT_ACTIVE:
                self.set_timeout(self.config.leader_timeout, self._handle_leader_sequence)

        return self

    def _handle_leader_sequence(self):
        lmh = tuple(self.leader_mode_history)

        if lmh in self.config.leader_dictionary:
            self.macros_pending.append(self.config.leader_dictionary[lmh].keydown)

        return self._exit_leader_mode()

    def _process_leader_mode(self):
        keys_pressed = self.keys_pressed

        if self.leader_last_len and self.leader_mode_history:
            history_set = set(self.leader_mode_history)

            keys_pressed = keys_pressed - history_set

        self.leader_last_len = len(self.keys_pressed)

        for key in keys_pressed:
            if (
                self.config.leader_mode == LeaderMode.ENTER_ACTIVE and
                key == Keycodes.Common.KC_ENT
            ):
                self._handle_leader_sequence()
                break
            elif key == Keycodes.Common.KC_ESC or key == Keycodes.KMK.KC_GESC:
                # Clean self and turn leader mode off.
                self._exit_leader_mode()
                break
            elif key == Keycodes.KMK.KC_LEAD:
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
