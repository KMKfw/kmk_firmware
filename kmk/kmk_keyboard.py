from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

from kmk.consts import KMK_RELEASE, UnicodeMode
from kmk.hid import AbstractHID, BLEHID, USBHID, HIDModes
from kmk.keys import KC, Key, KeyAttrDict
from kmk.kmktime import ticks_ms
from kmk.matrix import MatrixScanner, intify_coordinate
from kmk.types import TapDanceKeyMeta


class Sandbox:
    matrix_update: Optional[bytearray] = None
    secondary_matrix_update: Optional[bytearray] = None
    active_layers: Optional[List[int]] = None


class KMKKeyboard:
    #####
    # User-configurable
    debug_enabled: bool = False

    keymap: List[KeyAttrDict] = []
    coord_mapping: Optional[List[int]] = None

    row_pins: Optional[Tuple[Any, ...]] = None
    col_pins: Optional[Tuple[Any, ...]] = None
    diode_orientation: Optional[int] = None
    matrix: Optional[MatrixScanner] = None
    matrix_scanner: Type[MatrixScanner] = MatrixScanner
    uart_buffer: List[Any] = []

    unicode_mode: int = UnicodeMode.NOOP
    tap_time: int = 300

    modules: List[Type[Any]] = []
    extensions: List[Type[Any]] = []
    sandbox: Sandbox = Sandbox()

    #####
    # Internal State
    keys_pressed: Set[Key] = set()
    _coordkeys_pressed: Dict[Any, Any] = {}
    hid_type: int = HIDModes.USB
    secondary_hid_type: Optional[int] = None
    _hid_helper: Optional[Union[Type[AbstractHID], Type[BLEHID], Type[USBHID]]] = None
    hid_pending: bool = False
    state_layer_key: Optional[Key] = None
    matrix_update: Optional[Union[bytearray, None]] = None
    secondary_matrix_update: Optional[Union[bytearray, None]] = None
    _matrix_modify: Optional[Any] = None
    state_changed: bool = False
    _old_timeouts_len: Optional[int] = None
    _new_timeouts_len: Optional[int] = None
    _trigger_powersave_enable: bool = False
    _trigger_powersave_disable: bool = False
    i2c_deinit_count: int = 0

    # this should almost always be PREpended to, replaces
    # former use of reversed_active_layers which had pointless
    # overhead (the underlying list was never used anyway)
    active_layers: List[int] = [0]

    _timeouts: Dict[float, Callable[[], Key]] = {}
    _tapping: bool = False
    _tap_dance_counts: Dict[Union[Key, TapDanceKeyMeta], Union[int, None]] = {}
    _tap_side_effects: Dict[Union[Key, TapDanceKeyMeta], Union[Key, None]] = {}

    # on some M4 setups (such as klardotsh/klarank_feather_m4, CircuitPython
    # 6.0rc1) this runs out of RAM every cycle and takes down the board. no
    # real known fix yet other than turning off debug, but M4s have always been
    # tight on RAM so....
    def __repr__(self) -> str:
        return (
            'KMKKeyboard('
            'debug_enabled={} '
            'diode_orientation={} '
            'matrix_scanner={} '
            'unicode_mode={} '
            'tap_time={} '
            '_hid_helper={} '
            'keys_pressed={} '
            'coordkeys_pressed={} '
            'hid_pending={} '
            'active_layers={} '
            'timeouts={} '
            'tapping={} '
            'tap_dance_counts={} '
            'tap_side_effects={}'
            ')'
        ).format(
            self.debug_enabled,
            self.diode_orientation,
            self.matrix_scanner,
            self.unicode_mode,
            self.tap_time,
            self._hid_helper,
            # internal state
            self.keys_pressed,
            self._coordkeys_pressed,
            self.hid_pending,
            self.active_layers,
            self._timeouts,
            self._tapping,
            self._tap_dance_counts,
            self._tap_side_effects,
        )

    def _print_debug_cycle(self, init: bool = False) -> None:
        if self.debug_enabled:
            if init:
                print('KMKInit(release={})'.format(KMK_RELEASE))
            print(self)

    def _send_hid(self) -> None:
        self._hid_helper.create_report(self.keys_pressed).send()
        self.hid_pending = False

    def _handle_matrix_report(self, update: bytearray = None) -> None:
        if update is not None:
            self._on_matrix_changed(update[0], update[1], update[2])
            self.state_changed = True

    def _find_key_in_map(self, int_coord: int, row: int, col: int) -> Union[Key, None]:
        self.state_layer_key = None
        try:
            idx = self.coord_mapping.index(int_coord)
        except ValueError:
            if self.debug_enabled:
                print(
                    'CoordMappingNotFound(ic={}, row={}, col={})'.format(
                        int_coord, row, col
                    )
                )

            return None

        for layer in self.active_layers:
            self.state_layer_key = self.keymap[layer][idx]

            if not self.state_layer_key or self.state_layer_key == KC.TRNS:
                continue

            if self.debug_enabled:
                print('KeyResolution(key={})'.format(self.state_layer_key))

            return self.state_layer_key

    def _on_matrix_changed(self, row: int, col: int, is_pressed: int) -> KMKKeyboard:
        if self.debug_enabled:
            print('MatrixChange(col={} row={} pressed={})'.format(col, row, is_pressed))

        int_coord = intify_coordinate(row, col)
        kc_changed = self._find_key_in_map(int_coord, row, col)

        if kc_changed is None:
            print('MatrixUndefinedCoordinate(col={} row={})'.format(col, row))
            return self

        return self.process_key(kc_changed, is_pressed, int_coord, (row, col))

    def process_key(self, key: Union[Key, TapDanceKeyMeta], is_pressed: int, coord_int: Optional[int] = None, coord_raw: Tuple[int, int] = None) -> KMKKeyboard:
        if self._tapping and not isinstance(key.meta, TapDanceKeyMeta):
            self._process_tap_dance(key, is_pressed)
        else:
            if is_pressed:
                key.on_press(self, coord_int, coord_raw)
            else:
                key.on_release(self, coord_int, coord_raw)

        return self

    def remove_key(self, keycode: Key) -> KMKKeyboard:
        self.keys_pressed.discard(keycode)
        return self.process_key(keycode, False)

    def add_key(self, keycode: Key) -> KMKKeyboard:
        self.keys_pressed.add(keycode)
        return self.process_key(keycode, True)

    def tap_key(self, keycode: Key) -> KMKKeyboard:
        self.add_key(keycode)
        # On the next cycle, we'll remove the key.
        self.set_timeout(False, lambda: self.remove_key(keycode))

        return self

    def _process_tap_dance(self, changed_key: Union[Key, TapDanceKeyMeta], is_pressed: int) -> KMKKeyboard:
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
                self.set_timeout(
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

    def _end_tap_dance(self, td_key: Union[Key, TapDanceKeyMeta]) -> KMKKeyboard:
        v = self._tap_dance_counts[td_key] - 1

        if v >= 0:
            if td_key in self.keys_pressed:
                key_to_press = td_key.codes[v]
                self.add_key(key_to_press)
                self._tap_side_effects[td_key] = key_to_press
                self.hid_pending = True
            else:
                if self._tap_side_effects[td_key]:
                    self.remove_key(self._tap_side_effects[td_key])
                    self._tap_side_effects[td_key] = None
                    self.hid_pending = True
                    self._cleanup_tap_dance(td_key)
                else:
                    self.tap_key(td_key.codes[v])
                    self._cleanup_tap_dance(td_key)

        return self

    def _cleanup_tap_dance(self, td_key: Union[Key, TapDanceKeyMeta]) -> KMKKeyboard:
        self._tap_dance_counts[td_key] = 0
        self._tapping = any(count > 0 for count in self._tap_dance_counts.values())
        return self

    def set_timeout(self, after_ticks: float, callback: Callable[[], Key]) -> float:
        if after_ticks is False:
            # We allow passing False as an implicit "run this on the next process timeouts cycle"
            timeout_key = ticks_ms()
        else:
            timeout_key = ticks_ms() + after_ticks

        while timeout_key in self._timeouts:
            timeout_key += 1

        self._timeouts[timeout_key] = callback
        return timeout_key

    def _cancel_timeout(self, timeout_key: float) -> None:
        if timeout_key in self._timeouts:
            del self._timeouts[timeout_key]

    def _process_timeouts(self) -> KMKKeyboard:
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

    def _init_sanity_check(self) -> KMKKeyboard:
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

    def _init_coord_mapping(self) -> None:
        '''
        Attempt to sanely guess a coord_mapping if one is not provided. No-op
        if `kmk.extensions.split.Split` is used, it provides equivalent
        functionality in `on_bootup`

        To save RAM on boards that don't use Split, we don't import Split
        and do an isinstance check, but instead do string detection
        '''
        if any(x.__class__.__module__ == 'kmk.modules.split' for x in self.modules):
            return

        if not self.coord_mapping:
            self.coord_mapping = []

            rows_to_calc = len(self.row_pins)
            cols_to_calc = len(self.col_pins)

            for ridx in range(rows_to_calc):
                for cidx in range(cols_to_calc):
                    self.coord_mapping.append(intify_coordinate(ridx, cidx))

    def _init_hid(self) -> None:
        if self.hid_type == HIDModes.NOOP:
            self._hid_helper = AbstractHID
        elif self.hid_type == HIDModes.USB:
            self._hid_helper = USBHID
        elif self.hid_type == HIDModes.BLE:
            self._hid_helper = BLEHID
        else:
            self._hid_helper = AbstractHID
        self._hid_helper = self._hid_helper()

    def _init_matrix(self) -> KMKKeyboard:
        self.matrix = MatrixScanner(
            cols=self.col_pins,
            rows=self.row_pins,
            diode_orientation=self.diode_orientation,
            rollover_cols_every_rows=getattr(self, 'rollover_cols_every_rows', None),
        )

        return self

    def before_matrix_scan(self) -> None:
        for module in self.modules:
            try:
                module.before_matrix_scan(self)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to run pre matrix function in module: ', err, module)

        for ext in self.extensions:
            try:
                ext.before_matrix_scan(self.sandbox)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to run pre matrix function in extension: ', err, ext)

    def after_matrix_scan(self) -> None:
        for module in self.modules:
            try:
                module.after_matrix_scan(self)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to run post matrix function in module: ', err, module)

        for ext in self.extensions:
            try:
                ext.after_matrix_scan(self.sandbox)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to run post matrix function in extension: ', err, ext)

    def before_hid_send(self) -> None:
        for module in self.modules:
            try:
                module.before_hid_send(self)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to run pre hid function in module: ', err, module)

        for ext in self.extensions:
            try:
                ext.before_hid_send(self.sandbox)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to run pre hid function in extension: ', err, ext)

    def after_hid_send(self) -> None:
        for module in self.modules:
            try:
                module.after_hid_send(self)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to run post hid function in module: ', err, module)

        for ext in self.extensions:
            try:
                ext.after_hid_send(self.sandbox)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to run post hid function in extension: ', err, ext)

    def powersave_enable(self) -> None:
        for module in self.modules:
            try:
                module.on_powersave_enable(self)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to run post hid function in module: ', err, module)

        for ext in self.extensions:
            try:
                ext.on_powersave_enable(self.sandbox)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to run post hid function in extension: ', err, ext)

    def powersave_disable(self) -> None:
        for module in self.modules:
            try:
                module.on_powersave_disable(self)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to run post hid function in module: ', err, module)
        for ext in self.extensions:
            try:
                ext.on_powersave_disable(self.sandbox)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to run post hid function in extension: ', err, ext)

    def go(self, hid_type: int = HIDModes.USB, secondary_hid_type: Optional[int] = None, **kwargs: Dict[Any, Any]) -> None:
        self.hid_type = hid_type
        self.secondary_hid_type = secondary_hid_type

        self._init_sanity_check()
        self._init_coord_mapping()
        self._init_hid()

        for module in self.modules:
            try:
                module.during_bootup(self)
            except Exception:
                if self.debug_enabled:
                    print('Failed to load module', module)
        for ext in self.extensions:
            try:
                ext.during_bootup(self)
            except Exception:
                if self.debug_enabled:
                    print('Failed to load extention', ext)

        self._init_matrix()

        self._print_debug_cycle(init=True)

        while True:
            self.state_changed = False
            self.sandbox.active_layers = self.active_layers.copy()

            self.before_matrix_scan()

            self.matrix_update = (
                self.sandbox.matrix_update
            ) = self.matrix.scan_for_changes()
            self.sandbox.secondary_matrix_update = self.secondary_matrix_update

            self.after_matrix_scan()

            self._handle_matrix_report(self.secondary_matrix_update)
            self.secondary_matrix_update = None
            self._handle_matrix_report(self.matrix_update)
            self.matrix_update = None

            self.before_hid_send()

            if self.hid_pending:
                self._send_hid()

            self._old_timeouts_len = len(self._timeouts)
            self._process_timeouts()
            self._new_timeouts_len = len(self._timeouts)

            if self._old_timeouts_len != self._new_timeouts_len:
                self.state_changed = True
                if self.hid_pending:
                    self._send_hid()

            self.after_hid_send()

            if self._trigger_powersave_enable:
                self.powersave_enable()

            if self._trigger_powersave_disable:
                self.powersave_disable()

            if self.state_changed:
                self._print_debug_cycle()
