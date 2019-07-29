# There's a chance doing preload RAM hacks this late will cause recursion
# errors, but we'll see. I'd rather do it here than require everyone copy-paste
# a line into their keymaps.
import kmk.preload_imports  # isort:skip # NOQA

import gc

from kmk import rgb
from kmk.consts import KMK_RELEASE, UnicodeMode
from kmk.hid import BLEHID, USBHID, AbstractHID, HIDModes
from kmk.keys import KC
from kmk.kmktime import ticks_ms
from kmk.matrix import MatrixScanner, intify_coordinate
from kmk.types import TapDanceKeyMeta


class KMKKeyboard:
    #####
    # User-configurable
    debug_enabled = False

    keymap = None
    coord_mapping = None

    row_pins = None
    col_pins = None
    diode_orientation = None
    matrix_scanner = MatrixScanner
    uart_buffer = []

    unicode_mode = UnicodeMode.NOOP
    tap_time = 300

    # RGB config
    rgb_pixel_pin = None
    rgb_config = rgb.rgb_config

    #####
    # Internal State
    _keys_pressed = set()
    _coord_keys_pressed = {}
    _hid_pending = False

    # this should almost always be PREpended to, replaces
    # former use of reversed_active_layers which had pointless
    # overhead (the underlying list was never used anyway)
    _active_layers = [0]

    _start_time = {'lt': None, 'tg': None, 'tt': None, 'lm': None}
    _timeouts = {}
    _tapping = False
    _tap_dance_counts = {}
    _tap_side_effects = {}

    def __repr__(self):
        return (
            'KMKKeyboard('
            'debug_enabled={} '
            'keymap=truncated '
            'coord_mapping=truncated '
            'row_pins=truncated '
            'col_pins=truncated '
            'diode_orientation={} '
            'matrix_scanner={} '
            'unicode_mode={} '
            'tap_time={} '
            'hid_helper={} '
            'keys_pressed={} '
            'coord_keys_pressed={} '
            'hid_pending={} '
            'active_layers={} '
            'start_time={} '
            'timeouts={} '
            'tapping={} '
            'tap_dance_counts={} '
            'tap_side_effects={}'
            ')'
        ).format(
            self.debug_enabled,
            # self.keymap,
            # self.coord_mapping,
            # self.row_pins,
            # self.col_pins,
            self.diode_orientation,
            self.matrix_scanner,
            self.unicode_mode,
            self.tap_time,
            self.hid_helper.__name__,
            # internal state
            self._keys_pressed,
            self._coord_keys_pressed,
            self._hid_pending,
            self._active_layers,
            self._start_time,
            self._timeouts,
            self._tapping,
            self._tap_dance_counts,
            self._tap_side_effects,
        )

    def _print_debug_cycle(self, init=False):
        pre_alloc = gc.mem_alloc()
        pre_free = gc.mem_free()

        if self.debug_enabled:
            if init:
                print('KMKInit(release={})'.format(KMK_RELEASE))

            print(self)
            print(self)
            print(
                'GCStats(pre_alloc={} pre_free={} alloc={} free={})'.format(
                    pre_alloc, pre_free, gc.mem_alloc(), gc.mem_free()
                )
            )

    def _send_hid(self):
        self._hid_helper_inst.create_report(self._keys_pressed).send()
        self._hid_pending = False

    def _handle_matrix_report(self, update=None):
        if update is not None:
            self._on_matrix_changed(update[0], update[1], update[2])
            self.state_changed = True

    def _receive_from_initiator(self):
        if self.uart is not None and self.uart.in_waiting > 0 or self.uart_buffer:
            if self.uart.in_waiting >= 60:
                # This is a dirty hack to prevent crashes in unrealistic cases
                import microcontroller

                microcontroller.reset()

            while self._uart.in_waiting >= 3:
                self.uart_buffer.append(self._uart.read(3))
            if self.uart_buffer:
                update = bytearray(self.uart_buffer.pop(0))

                # Built in debug mode switch
                if update == b'DEB':
                    print(self._uart.readline())
                    return None
                return update

        return None

    def _send_debug(self, message):
        '''
        Prepends DEB and appends a newline to allow debug messages to
        be detected and handled differently than typical keypresses.
        :param message: Debug message
        '''
        if self._uart is not None:
            self._uart.write('DEB')
            self._uart.write(message, '\n')

    #####
    # SPLICE: INTERNAL STATE
    # FIXME CLEAN THIS
    #####

    def _find_key_in_map(self, row, col):
        ic = intify_coordinate(row, col)

        try:
            idx = self.coord_mapping.index(ic)
        except ValueError:
            if self.debug_enabled:
                print(
                    'CoordMappingNotFound(ic={}, row={}, col={})'.format(ic, row, col)
                )

            return None

        for layer in self._active_layers:
            layer_key = self.keymap[layer][idx]

            if not layer_key or layer_key == KC.TRNS:
                continue

            if self.debug_enabled:
                print('KeyResolution(key={})'.format(layer_key))

            return layer_key

    def _on_matrix_changed(self, row, col, is_pressed):
        if self.debug_enabled:
            print('MatrixChange(col={} row={} pressed={})'.format(col, row, is_pressed))

        int_coord = intify_coordinate(row, col)
        kc_changed = self._find_key_in_map(row, col)

        if kc_changed is None:
            print('MatrixUndefinedCoordinate(col={} row={})'.format(col, row))
            return self

        return self._process_key(kc_changed, is_pressed, int_coord, (row, col))

    def _process_key(self, key, is_pressed, coord_int=None, coord_raw=None):
        if self._tapping and not isinstance(key.meta, TapDanceKeyMeta):
            self._process_tap_dance(key, is_pressed)
        else:
            if is_pressed:
                key._on_press(self, coord_int, coord_raw)
            else:
                key._on_release(self, coord_int, coord_raw)

        return self

    def _remove_key(self, keycode):
        self._keys_pressed.discard(keycode)
        return self._process_key(keycode, False)

    def _add_key(self, keycode):
        self._keys_pressed.add(keycode)
        return self._process_key(keycode, True)

    def _tap_key(self, keycode):
        self._add_key(keycode)
        # On the next cycle, we'll remove the key.
        self._set_timeout(False, lambda: self._remove_key(keycode))

        return self

    def _process_tap_dance(self, changed_key, is_pressed):
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
                self._set_timeout(
                    self.tap_time, lambda: self._end_tap_dance(changed_key)
                )
                self._tapping = True
            else:
                self._tap_dance_counts[changed_key] += 1

            if changed_key not in self._tap_side_effects:
                self._tap_side_effects[changed_key] = None
        else:
            has_side_effects = self._tap_side_effects[changed_key] is not None
            hit_max_defined_taps = self._tap_dance_counts[changed_key] == len(
                changed_key.codes
            )

            if has_side_effects or hit_max_defined_taps:
                self._end_tap_dance(changed_key)

        return self

    def _end_tap_dance(self, td_key):
        v = self._tap_dance_counts[td_key] - 1

        if v >= 0:
            if td_key in self._keys_pressed:
                key_to_press = td_key.codes[v]
                self._add_key(key_to_press)
                self._tap_side_effects[td_key] = key_to_press
                self._hid_pending = True
            else:
                if self._tap_side_effects[td_key]:
                    self._remove_key(self._tap_side_effects[td_key])
                    self._tap_side_effects[td_key] = None
                    self._hid_pending = True
                    self._cleanup_tap_dance(td_key)
                else:
                    self._tap_key(td_key.codes[v])
                    self._cleanup_tap_dance(td_key)

        return self

    def _cleanup_tap_dance(self, td_key):
        self._tap_dance_counts[td_key] = 0
        self._tapping = any(count > 0 for count in self._tap_dance_counts.values())
        return self

    def _set_timeout(self, after_ticks, callback):
        if after_ticks is False:
            # We allow passing False as an implicit "run this on the next process timeouts cycle"
            timeout_key = ticks_ms()
        else:
            timeout_key = ticks_ms() + after_ticks

        while timeout_key in self._timeouts:
            timeout_key += 1

        self._timeouts[timeout_key] = callback
        return timeout_key

    def _cancel_timeout(self, timeout_key):
        if timeout_key in self._timeouts:
            del self._timeouts[timeout_key]

    def _process_timeouts(self):
        if not self._timeouts:
            return self

        current_time = ticks_ms()

        # cast this to a tuple to ensure that if a callback itself sets
        # timeouts, we do not handle them on the current cycle
        timeouts = tuple(self._timeouts.items())

        for k, v in timeouts:
            if k <= current_time:
                v()
                del self._timeouts[k]

        return self

    #####
    # SPLICE END: INTERNAL STATE
    # TODO FIXME REMOVE THIS
    #####

    def _init_sanity_check(self):
        '''
        Ensure the provided configuration is *probably* bootable
        '''
        assert self.keymap, 'must define a keymap with at least one row'
        assert self.row_pins, 'no GPIO pins defined for matrix rows'
        assert self.col_pins, 'no GPIO pins defined for matrix columns'
        assert self.diode_orientation is not None, 'diode orientation must be defined'
        assert (
            self.hid_type in HIDModes.ALL_MODES
        ), 'hid_type must be a value from kmk.consts.HIDModes'

        return self

    def _init_coord_mapping(self):
        '''
        Attempt to sanely guess a coord_mapping if one is not provided. No-op
        if `kmk.extensions.split.Split` is used, it provides equivalent
        functionality in `on_bootup`

        To save RAM on boards that don't use Split, we don't import Split
        and do an isinstance check, but instead do string detection
        '''
        if any(
            x.__class__.__module__ == 'kmk.extensions.split' for x in self._extensions
        ):
            return

        if not self.coord_mapping:
            self.coord_mapping = []

            rows_to_calc = len(self.row_pins)
            cols_to_calc = len(self.col_pins)

            for ridx in range(rows_to_calc):
                for cidx in range(cols_to_calc):
                    self.coord_mapping.append(intify_coordinate(ridx, cidx))

    def _init_hid(self):
        if self.hid_type == HIDModes.NOOP:
            self.hid_helper = AbstractHID
        elif self.hid_type == HIDModes.USB:
            try:
                from kmk.hid import USBHID

                self.hid_helper = USBHID
            except ImportError:
                self.hid_helper = AbstractHID
                print('USB HID is unsupported ')
        elif self.hid_type == HIDModes.BLE:
            try:
                from kmk.ble import BLEHID

                self.hid_helper = BLEHID
            except ImportError:
                self.hid_helper = AbstractHID
                print('Bluetooth is unsupported ')

        self._hid_helper_inst = self.hid_helper(**kwargs)

    def _init_matrix(self):
        self.matrix = MatrixScanner(
            cols=self.col_pins,
            rows=self.row_pins,
            diode_orientation=self.diode_orientation,
            rollover_cols_every_rows=getattr(self, 'rollover_cols_every_rows', None),
        )

        return self

    def go(self, hid_type=HIDModes.USB, **kwargs):
        self._extensions = [] + getattr(self, 'extensions', [])

        try:
            del self.extensions
        except Exception:
            pass
        finally:
            gc.collect()

        self.hid_type = hid_type

        self._init_sanity_check()
        self._init_coord_mapping()
        self._init_hid()

        for ext in self._extensions:
            try:
                ext.during_bootup(self)
            except Exception:
                # TODO FIXME log the exceptions or something
                pass

        self._init_matrix()

        self._print_debug_cycle(init=True)

        while True:
            self.state_changed = False

            for ext in self._extensions:
                try:
                    self._handle_matrix_report(ext.before_matrix_scan(self))
                except Exception as e:
                    print(e)

            matrix_update = self.matrix.scan_for_changes()
            self._handle_matrix_report(matrix_update)

            for ext in self._extensions:
                try:
                    ext.after_matrix_scan(self, matrix_update)
                except Exception as e:
                    print(e)

            for ext in self._extensions:
                try:
                    ext.before_hid_send(self)
                except Exception:
                    # TODO FIXME log the exceptions or something
                    pass

            if self._hid_pending:
                self._send_hid()

            old_timeouts_len = len(self._timeouts)
            self._process_timeouts()
            new_timeouts_len = len(self._timeouts)

            if old_timeouts_len != new_timeouts_len:
                self.state_changed = True

                if self._hid_pending:
                    self._send_hid()

            for ext in self._extensions:
                try:
                    ext.after_hid_send(self)
                except Exception:
                    # TODO FIXME log the exceptions or something
                    pass

            if self.state_changed:
                self._print_debug_cycle()
