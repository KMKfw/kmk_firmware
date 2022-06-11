from supervisor import ticks_ms

from kmk.consts import KMK_RELEASE, UnicodeMode
from kmk.hid import BLEHID, USBHID, AbstractHID, HIDModes
from kmk.keys import KC
from kmk.kmktime import ticks_add, ticks_diff
from kmk.scanners.keypad import MatrixScanner


class Sandbox:
    matrix_update = None
    secondary_matrix_update = None
    active_layers = None


class KMKKeyboard:
    #####
    # User-configurable
    debug_enabled = False

    keymap = []
    coord_mapping = None

    row_pins = None
    col_pins = None
    diode_orientation = None
    matrix = None
    uart_buffer = []

    unicode_mode = UnicodeMode.NOOP

    modules = []
    extensions = []
    sandbox = Sandbox()

    #####
    # Internal State
    keys_pressed = set()
    _coordkeys_pressed = {}
    hid_type = HIDModes.USB
    secondary_hid_type = None
    _hid_helper = None
    _hid_send_enabled = False
    hid_pending = False
    matrix_update = None
    secondary_matrix_update = None
    matrix_update_queue = []
    _matrix_modify = None
    state_changed = False
    _old_timeouts_len = None
    _new_timeouts_len = None
    _trigger_powersave_enable = False
    _trigger_powersave_disable = False
    i2c_deinit_count = 0
    _go_args = None
    _processing_timeouts = False

    # this should almost always be PREpended to, replaces
    # former use of reversed_active_layers which had pointless
    # overhead (the underlying list was never used anyway)
    active_layers = [0]

    _timeouts = {}

    # on some M4 setups (such as klardotsh/klarank_feather_m4, CircuitPython
    # 6.0rc1) this runs out of RAM every cycle and takes down the board. no
    # real known fix yet other than turning off debug, but M4s have always been
    # tight on RAM so....
    def __repr__(self):
        return ''.join(
            [
                'KMKKeyboard(\n',
                f'  debug_enabled={self.debug_enabled}, ',
                f'diode_orientation={self.diode_orientation}, ',
                f'matrix={self.matrix},\n',
                f'  unicode_mode={self.unicode_mode}, ',
                f'_hid_helper={self._hid_helper},\n',
                f'  keys_pressed={self.keys_pressed},\n',
                f'  _coordkeys_pressed={self._coordkeys_pressed},\n',
                f'  hid_pending={self.hid_pending}, ',
                f'active_layers={self.active_layers}, ',
                f'_timeouts={self._timeouts}\n',
                ')',
            ]
        )

    def _print_debug_cycle(self, init=False):
        if self.debug_enabled:
            if init:
                print(f'KMKInit(release={KMK_RELEASE})')
            print(self)

    def _send_hid(self):
        if self._hid_send_enabled:
            hid_report = self._hid_helper.create_report(self.keys_pressed)
            try:
                hid_report.send()
            except KeyError as e:
                if self.debug_enabled:
                    print(f'HidNotFound(HIDReportType={e})')
        self.hid_pending = False

    def _handle_matrix_report(self, update=None):
        if update is not None:
            self._on_matrix_changed(update)
            self.state_changed = True

    def _find_key_in_map(self, int_coord):
        try:
            idx = self.coord_mapping.index(int_coord)
        except ValueError:
            if self.debug_enabled:
                print(f'CoordMappingNotFound(ic={int_coord})')

            return None

        for layer in self.active_layers:
            try:
                layer_key = self.keymap[layer][idx]
            except IndexError:
                layer_key = None
                if self.debug_enabled:
                    print(f'KeymapIndexError(idx={idx}, layer={layer})')

            if not layer_key or layer_key == KC.TRNS:
                continue

            return layer_key

    def _on_matrix_changed(self, kevent):
        int_coord = kevent.key_number
        is_pressed = kevent.pressed
        if self.debug_enabled:
            print(f'\nMatrixChange(ic={int_coord}, pressed={is_pressed})')

        key = None
        if not is_pressed:
            try:
                key = self._coordkeys_pressed[int_coord]
            except KeyError:
                if self.debug_enabled:
                    print(f'KeyNotPressed(ic={int_coord})')

        if key is None:
            key = self._find_key_in_map(int_coord)

            if key is None:
                if self.debug_enabled:
                    print(f'MatrixUndefinedCoordinate(ic={int_coord})')
                return self

        if self.debug_enabled:
            print(f'KeyResolution(key={key})')

        self.pre_process_key(key, is_pressed, int_coord)

    def pre_process_key(self, key, is_pressed, int_coord=None):
        for module in self.modules:
            try:
                key = module.process_key(self, key, is_pressed, int_coord)
                if key is None:
                    break
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to run process_key function in module: ', err, module)

        if int_coord is not None:
            if is_pressed:
                self._coordkeys_pressed[int_coord] = key
            else:
                try:
                    del self._coordkeys_pressed[int_coord]
                except KeyError:
                    if self.debug_enabled:
                        print(f'ReleaseKeyError(ic={int_coord})')

        if key:
            self.process_key(key, is_pressed, int_coord)

        return self

    def process_key(self, key, is_pressed, coord_int=None):
        if is_pressed:
            key.on_press(self, coord_int)
        else:
            key.on_release(self, coord_int)

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

    def set_timeout(self, after_ticks, callback):
        # We allow passing False as an implicit "run this on the next process timeouts cycle"
        if after_ticks is False:
            after_ticks = 0

        if after_ticks == 0 and self._processing_timeouts:
            after_ticks += 1

        timeout_key = ticks_add(ticks_ms(), after_ticks)

        if timeout_key not in self._timeouts:
            self._timeouts[timeout_key] = []

        idx = len(self._timeouts[timeout_key])
        self._timeouts[timeout_key].append(callback)

        return (timeout_key, idx)

    def cancel_timeout(self, timeout_key):
        try:
            self._timeouts[timeout_key[0]][timeout_key[1]] = None
        except (KeyError, IndexError):
            if self.debug_enabled:
                print(f'no such timeout: {timeout_key}')

    def _process_timeouts(self):
        if not self._timeouts:
            return self

        # Copy timeout keys to a temporary list to allow sorting.
        # Prevent net timeouts set during handling from running on the current
        # cycle by setting a flag `_processing_timeouts`.
        current_time = ticks_ms()
        timeout_keys = []
        self._processing_timeouts = True

        for k in self._timeouts.keys():
            if ticks_diff(k, current_time) <= 0:
                timeout_keys.append(k)

        for k in sorted(timeout_keys):
            for callback in self._timeouts[k]:
                if callback:
                    callback()
            del self._timeouts[k]

        self._processing_timeouts = False

        return self

    def _init_sanity_check(self):
        '''
        Ensure the provided configuration is *probably* bootable
        '''
        assert self.keymap, 'must define a keymap with at least one row'
        assert (
            self.hid_type in HIDModes.ALL_MODES
        ), 'hid_type must be a value from kmk.consts.HIDModes'
        if not self.matrix:
            assert self.row_pins, 'no GPIO pins defined for matrix rows'
            assert self.col_pins, 'no GPIO pins defined for matrix columns'
            assert (
                self.diode_orientation is not None
            ), 'diode orientation must be defined'

        return self

    def _init_coord_mapping(self):
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
            cm = []
            for m in self.matrix:
                cm.extend(m.coord_mapping)
            self.coord_mapping = tuple(cm)

    def _init_hid(self):
        if self.hid_type == HIDModes.NOOP:
            self._hid_helper = AbstractHID
        elif self.hid_type == HIDModes.USB:
            self._hid_helper = USBHID
        elif self.hid_type == HIDModes.BLE:
            self._hid_helper = BLEHID
        else:
            self._hid_helper = AbstractHID
        self._hid_helper = self._hid_helper(**self._go_args)
        self._hid_send_enabled = True

    def _init_matrix(self):
        if self.matrix is None:
            if self.debug_enabled:
                print('Initialising default matrix scanner.')
            self.matrix = MatrixScanner(
                column_pins=self.col_pins,
                row_pins=self.row_pins,
                columns_to_anodes=self.diode_orientation,
            )
        else:
            if self.debug_enabled:
                print('Matrix scanner already set, not overwriting.')

        try:
            self.matrix = tuple(iter(self.matrix))
            offset = 0
            for matrix in self.matrix:
                matrix.offset = offset
                offset += matrix.key_count
        except TypeError:
            self.matrix = (self.matrix,)

        return self

    def before_matrix_scan(self):
        for module in self.modules:
            try:
                module.before_matrix_scan(self)
            except Exception as err:
                if self.debug_enabled:
                    print(
                        'Failed to run before matrix scan function in module: ',
                        err,
                        module,
                    )

        for ext in self.extensions:
            try:
                ext.before_matrix_scan(self.sandbox)
            except Exception as err:
                if self.debug_enabled:
                    print(
                        'Failed to run before matrix scan function in extension: ',
                        err,
                        ext,
                    )

    def after_matrix_scan(self):
        for module in self.modules:
            try:
                module.after_matrix_scan(self)
            except Exception as err:
                if self.debug_enabled:
                    print(
                        'Failed to run after matrix scan function in module: ',
                        err,
                        module,
                    )

        for ext in self.extensions:
            try:
                ext.after_matrix_scan(self.sandbox)
            except Exception as err:
                if self.debug_enabled:
                    print(
                        'Failed to run after matrix scan function in extension: ',
                        err,
                        ext,
                    )

    def before_hid_send(self):
        for module in self.modules:
            try:
                module.before_hid_send(self)
            except Exception as err:
                if self.debug_enabled:
                    print(
                        'Failed to run before hid send function in module: ',
                        err,
                        module,
                    )

        for ext in self.extensions:
            try:
                ext.before_hid_send(self.sandbox)
            except Exception as err:
                if self.debug_enabled:
                    print(
                        'Failed to run before hid send function in extension: ',
                        err,
                        ext,
                    )

    def after_hid_send(self):
        for module in self.modules:
            try:
                module.after_hid_send(self)
            except Exception as err:
                if self.debug_enabled:
                    print(
                        'Failed to run after hid send function in module: ', err, module
                    )

        for ext in self.extensions:
            try:
                ext.after_hid_send(self.sandbox)
            except Exception as err:
                if self.debug_enabled:
                    print(
                        'Failed to run after hid send function in extension: ', err, ext
                    )

    def powersave_enable(self):
        for module in self.modules:
            try:
                module.on_powersave_enable(self)
            except Exception as err:
                if self.debug_enabled:
                    print(
                        'Failed to run on powersave enable function in module: ',
                        err,
                        module,
                    )

        for ext in self.extensions:
            try:
                ext.on_powersave_enable(self.sandbox)
            except Exception as err:
                if self.debug_enabled:
                    print(
                        'Failed to run on powersave enable function in extension: ',
                        err,
                        ext,
                    )

    def powersave_disable(self):
        for module in self.modules:
            try:
                module.on_powersave_disable(self)
            except Exception as err:
                if self.debug_enabled:
                    print(
                        'Failed to run on powersave disable function in module: ',
                        err,
                        module,
                    )
        for ext in self.extensions:
            try:
                ext.on_powersave_disable(self.sandbox)
            except Exception as err:
                if self.debug_enabled:
                    print(
                        'Failed to run on powersave disable function in extension: ',
                        err,
                        ext,
                    )

    def go(self, hid_type=HIDModes.USB, secondary_hid_type=None, **kwargs):
        self._init(hid_type=hid_type, secondary_hid_type=secondary_hid_type, **kwargs)
        while True:
            self._main_loop()

    def _init(self, hid_type=HIDModes.USB, secondary_hid_type=None, **kwargs):
        self._go_args = kwargs
        self.hid_type = hid_type
        self.secondary_hid_type = secondary_hid_type

        self._init_sanity_check()
        self._init_hid()
        self._init_matrix()
        self._init_coord_mapping()

        for module in self.modules:
            try:
                module.during_bootup(self)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to load module', err, module)
                print()
        for ext in self.extensions:
            try:
                ext.during_bootup(self)
            except Exception as err:
                if self.debug_enabled:
                    print('Failed to load extension', err, ext)

        self._print_debug_cycle(init=True)

    def _main_loop(self):
        self.state_changed = False
        self.sandbox.active_layers = self.active_layers.copy()

        self.before_matrix_scan()

        for matrix in self.matrix:
            update = matrix.scan_for_changes()
            if update:
                self.matrix_update = update
                break
        self.sandbox.secondary_matrix_update = self.secondary_matrix_update

        self.after_matrix_scan()

        if self.secondary_matrix_update:
            self.matrix_update_queue.append(self.secondary_matrix_update)
            self.secondary_matrix_update = None

        if self.matrix_update:
            self.matrix_update_queue.append(self.matrix_update)
            self.matrix_update = None

        # only handle one key per cycle.
        if self.matrix_update_queue:
            self._handle_matrix_report(self.matrix_update_queue.pop(0))

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
