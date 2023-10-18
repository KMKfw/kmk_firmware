try:
    from typing import Callable, Optional
except ImportError:
    pass

from collections import namedtuple
from keypad import Event as KeyEvent

from kmk.consts import UnicodeMode
from kmk.hid import BLEHID, USBHID, AbstractHID, HIDModes
from kmk.keys import KC, Key
from kmk.modules import Module
from kmk.scanners.keypad import MatrixScanner
from kmk.scheduler import Task, cancel_task, create_task, get_due_task
from kmk.utils import Debug

debug = Debug('kmk.keyboard')

KeyBufferFrame = namedtuple(
    'KeyBufferFrame', ('key', 'is_pressed', 'int_coord', 'index')
)


def debug_error(module, message: str, error: Exception):
    if debug.enabled:
        debug(
            message, ': ', error.__class__.__name__, ': ', error, name=module.__module__
        )


class Sandbox:
    matrix_update = None
    secondary_matrix_update = None
    active_layers = None


class KMKKeyboard:
    #####
    # User-configurable
    keymap = []
    coord_mapping = None

    row_pins = None
    col_pins = None
    diode_orientation = None
    matrix = None

    unicode_mode = UnicodeMode.NOOP

    modules = []
    extensions = []
    sandbox = Sandbox()

    #####
    # Internal State
    keys_pressed = set()
    axes = set()
    _coordkeys_pressed = {}
    hid_type = HIDModes.USB
    secondary_hid_type = None
    _hid_helper = None
    _hid_send_enabled = False
    hid_pending = False
    matrix_update = None
    secondary_matrix_update = None
    matrix_update_queue = []
    _trigger_powersave_enable = False
    _trigger_powersave_disable = False
    _go_args = None
    _processing_timeouts = False
    _resume_buffer = []
    _resume_buffer_x = []

    # this should almost always be PREpended to, replaces
    # former use of reversed_active_layers which had pointless
    # overhead (the underlying list was never used anyway)
    active_layers = [0]

    _timeouts = {}

    def __repr__(self) -> str:
        return self.__class__.__name__

    def _send_hid(self) -> None:
        if not self._hid_send_enabled:
            return

        if debug.enabled:
            if self.keys_pressed:
                debug('keys_pressed=', self.keys_pressed)
            if self.axes:
                debug('axes=', self.axes)

        self._hid_helper.create_report(self.keys_pressed, self.axes)
        try:
            self._hid_helper.send()
        except Exception as err:
            debug_error(self._hid_helper, 'send', err)

        self.hid_pending = False

        for axis in self.axes:
            axis.move(self, 0)

    def _handle_matrix_report(self, kevent: KeyEvent) -> None:
        if kevent is not None:
            self._on_matrix_changed(kevent)

    def _find_key_in_map(self, int_coord: int) -> Key:
        try:
            idx = self.coord_mapping.index(int_coord)
        except ValueError:
            if debug.enabled:
                debug('no such int_coord: ', int_coord)

            return None

        for layer in self.active_layers:
            try:
                key = self.keymap[layer][idx]
            except IndexError:
                key = None
                if debug.enabled:
                    debug('keymap IndexError: idx=', idx, ' layer=', layer)

            if not key or key == KC.TRNS:
                continue

            return key

    def _on_matrix_changed(self, kevent: KeyEvent) -> None:
        int_coord = kevent.key_number
        is_pressed = kevent.pressed

        key = None
        if not is_pressed:
            try:
                key = self._coordkeys_pressed[int_coord]
            except KeyError:
                if debug.enabled:
                    debug('release w/o press: ', int_coord)

        if key is None:
            key = self._find_key_in_map(int_coord)

        if key is None:
            return

        if debug.enabled:
            debug(kevent, ': ', key)

        self.pre_process_key(key, is_pressed, int_coord)

    def _process_resume_buffer(self):
        '''
        Resume the processing of buffered, delayed, deferred, etc. key events
        emitted by modules.

        We use a copy of the `_resume_buffer` as a working buffer. The working
        buffer holds all key events in the correct order for processing. If
        during processing new events are pushed to the `_resume_buffer`, they
        are prepended to the working buffer (which may not be emptied), in
        order to preserve key event order.
        We also double-buffer `_resume_buffer` with `_resume_buffer_x`, only
        copying the reference to hopefully safe some time on allocations.
        '''

        buffer, self._resume_buffer = self._resume_buffer, self._resume_buffer_x

        while buffer:
            ksf = buffer.pop(0)
            key = ksf.key

            # Handle any unaccounted-for layer shifts by looking up the key resolution again.
            if ksf.int_coord is not None:
                key = self._find_key_in_map(ksf.int_coord)

            # Resume the processing of the key event and update the HID report
            # when applicable.
            self.pre_process_key(key, ksf.is_pressed, ksf.int_coord, ksf.index)

            if self.hid_pending:
                self._send_hid()
                self.hid_pending = False

            # Any newly buffered key events must be prepended to the working
            # buffer.
            if self._resume_buffer:
                self._resume_buffer.extend(buffer)
                buffer.clear()
                buffer, self._resume_buffer = self._resume_buffer, buffer

        self._resume_buffer_x = buffer

    @property
    def debug_enabled(self) -> bool:
        return debug.enabled

    @debug_enabled.setter
    def debug_enabled(self, enabled: bool):
        debug.enabled = enabled

    def pre_process_key(
        self,
        key: Key,
        is_pressed: bool,
        int_coord: Optional[int] = None,
        index: int = 0,
    ) -> None:
        for module in self.modules[index:]:
            try:
                key = module.process_key(self, key, is_pressed, int_coord)
                if key is None:
                    break
            except Exception as err:
                debug_error(module, 'process_key', err)

        if int_coord is not None:
            if is_pressed:
                self._coordkeys_pressed[int_coord] = key
            else:
                try:
                    del self._coordkeys_pressed[int_coord]
                except KeyError:
                    if debug.enabled:
                        debug('release w/o press:', int_coord)
            if debug.enabled:
                debug('coordkeys_pressed=', self._coordkeys_pressed)

        if key:
            self.process_key(key, is_pressed, int_coord)

    def process_key(
        self, key: Key, is_pressed: bool, int_coord: Optional[int] = None
    ) -> None:
        if is_pressed:
            key.on_press(self, int_coord)
        else:
            key.on_release(self, int_coord)

    def resume_process_key(
        self,
        module: Module,
        key: Key,
        is_pressed: bool,
        int_coord: Optional[int] = None,
        reprocess: Optional[bool] = False,
    ) -> None:
        index = self.modules.index(module) + (0 if reprocess else 1)
        ksf = KeyBufferFrame(
            key=key, is_pressed=is_pressed, int_coord=int_coord, index=index
        )
        self._resume_buffer.append(ksf)

    def remove_key(self, keycode: Key) -> None:
        self.keys_pressed.discard(keycode)
        self.process_key(keycode, False)

    def add_key(self, keycode: Key) -> None:
        self.keys_pressed.add(keycode)
        self.process_key(keycode, True)

    def tap_key(self, keycode: Key) -> None:
        self.add_key(keycode)
        # On the next cycle, we'll remove the key.
        self.set_timeout(0, lambda: self.remove_key(keycode))

    def set_timeout(self, after_ticks: int, callback: Callable[[None], None]) -> [Task]:
        return create_task(callback, after_ms=after_ticks)

    def cancel_timeout(self, timeout_key: int) -> None:
        cancel_task(timeout_key)

    def _process_timeouts(self) -> None:
        for task in get_due_task():
            task()

    def _init_sanity_check(self) -> None:
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
            cm = []
            for m in self.matrix:
                cm.extend(m.coord_mapping)
            self.coord_mapping = tuple(cm)

    def _init_hid(self) -> None:
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

        if debug.enabled:
            debug('hid=', self._hid_helper)

    def _deinit_hid(self) -> None:
        self._hid_helper.clear_all()
        self._hid_helper.send()

    def _init_matrix(self) -> None:
        if self.matrix is None:
            self.matrix = MatrixScanner(
                column_pins=self.col_pins,
                row_pins=self.row_pins,
                columns_to_anodes=self.diode_orientation,
            )

        try:
            self.matrix = tuple(iter(self.matrix))
            offset = 0
            for matrix in self.matrix:
                matrix.offset = offset
                offset += matrix.key_count
        except TypeError:
            self.matrix = (self.matrix,)

        if debug.enabled:
            debug('matrix=', [_.__class__.__name__ for _ in self.matrix])

    def during_bootup(self) -> None:
        # Modules and extensions that fail `during_bootup` get removed from
        # their respective lists. This serves as a self-check mechanism; any
        # modules or extensions that initialize peripherals or data structures
        # should do that in `during_bootup`.
        for idx, module in enumerate(self.modules):
            try:
                module.during_bootup(self)
            except Exception as err:
                debug_error(module, 'during_bootup', err)
                self.modules[idx] = None

        self.modules[:] = [_ for _ in self.modules if _]

        if debug.enabled:
            debug('modules=', [_.__class__.__name__ for _ in self.modules])

        for idx, ext in enumerate(self.extensions):
            try:
                ext.during_bootup(self)
            except Exception as err:
                debug_error(ext, 'during_bootup', err)
                self.extensions[idx] = None

        self.modules[:] = [_ for _ in self.modules if _]

        if debug.enabled:
            debug('extensions=', [_.__class__.__name__ for _ in self.extensions])

    def before_matrix_scan(self) -> None:
        for module in self.modules:
            try:
                module.before_matrix_scan(self)
            except Exception as err:
                debug_error(module, 'before_matrix_scan', err)

        for ext in self.extensions:
            try:
                ext.before_matrix_scan(self.sandbox)
            except Exception as err:
                debug_error(ext, 'before_matrix_scan', err)

    def after_matrix_scan(self) -> None:
        for module in self.modules:
            try:
                module.after_matrix_scan(self)
            except Exception as err:
                debug_error(module, 'after_matrix_scan', err)

        for ext in self.extensions:
            try:
                ext.after_matrix_scan(self.sandbox)
            except Exception as err:
                debug_error(ext, 'after_matrix_scan', err)

    def before_hid_send(self) -> None:
        for module in self.modules:
            try:
                module.before_hid_send(self)
            except Exception as err:
                debug_error(module, 'before_hid_send', err)

        for ext in self.extensions:
            try:
                ext.before_hid_send(self.sandbox)
            except Exception as err:
                debug_error(ext, 'before_hid_send', err)

    def after_hid_send(self) -> None:
        for module in self.modules:
            try:
                module.after_hid_send(self)
            except Exception as err:
                debug_error(module, 'after_hid_send', err)

        for ext in self.extensions:
            try:
                ext.after_hid_send(self.sandbox)
            except Exception as err:
                debug_error(ext, 'after_hid_send', err)

    def powersave_enable(self) -> None:
        for module in self.modules:
            try:
                module.on_powersave_enable(self)
            except Exception as err:
                debug_error(module, 'powersave_enable', err)

        for ext in self.extensions:
            try:
                ext.on_powersave_enable(self.sandbox)
            except Exception as err:
                debug_error(ext, 'powersave_enable', err)

    def powersave_disable(self) -> None:
        for module in self.modules:
            try:
                module.on_powersave_disable(self)
            except Exception as err:
                debug_error(module, 'powersave_disable', err)

        for ext in self.extensions:
            try:
                ext.on_powersave_disable(self.sandbox)
            except Exception as err:
                debug_error(ext, 'powersave_disable', err)

    def deinit(self) -> None:
        for module in self.modules:
            try:
                module.deinit(self)
            except Exception as err:
                debug_error(module, 'deinit', err)

        for ext in self.extensions:
            try:
                ext.deinit(self.sandbox)
            except Exception as err:
                debug_error(ext, 'deinit', err)

    def go(self, hid_type=HIDModes.USB, secondary_hid_type=None, **kwargs) -> None:
        self._init(hid_type=hid_type, secondary_hid_type=secondary_hid_type, **kwargs)
        try:
            while True:
                self._main_loop()
        finally:
            debug('Unexpected error: cleaning up')
            self._deinit_hid()
            self.deinit()

    def _init(
        self,
        hid_type: HIDModes = HIDModes.USB,
        secondary_hid_type: Optional[HIDModes] = None,
        **kwargs,
    ) -> None:
        self._go_args = kwargs
        self.hid_type = hid_type
        self.secondary_hid_type = secondary_hid_type

        if debug.enabled:
            debug('Initialising ', self)
            debug('unicode_mode=', self.unicode_mode)

        self._init_hid()
        self._init_matrix()
        self._init_coord_mapping()
        self.during_bootup()

        if debug.enabled:
            import gc

            gc.collect()
            debug('mem_info used:', gc.mem_alloc(), ' free:', gc.mem_free())

    def _main_loop(self) -> None:
        self.sandbox.active_layers = self.active_layers.copy()

        self.before_matrix_scan()

        self._process_resume_buffer()

        for matrix in self.matrix:
            update = matrix.scan_for_changes()
            if update:
                self.matrix_update = update
                break
        self.sandbox.matrix_update = self.matrix_update
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

        self._process_timeouts()

        if self.hid_pending:
            self._send_hid()

        self.after_hid_send()

        if self._trigger_powersave_enable:
            self.powersave_enable()

        if self._trigger_powersave_disable:
            self.powersave_disable()
