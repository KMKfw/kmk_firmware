import time
from unittest.mock import Mock, patch

from kmk.hid import HIDModes
from kmk.keys import KC, ModifierKey
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.scanners.digitalio import MatrixScanner


class DigitalInOut(Mock):
    value = False


def code2name(code):
    for name in KC:
        try:
            if KC[name].code == code:
                return name
        except AttributeError:
            pass
    return code


class KeyboardTest:
    loop_delay_ms = 2

    def __init__(
        self,
        modules,
        keymap,
        keyboard_debug_enabled=False,
        debug_enabled=False,
        extensions={},
    ):
        self.debug_enabled = debug_enabled

        self.keyboard = KMKKeyboard()
        self.keyboard.debug_enabled = keyboard_debug_enabled

        self.keyboard.modules = modules
        self.keyboard.extensions = extensions

        self.pins = tuple(DigitalInOut() for k in keymap[0])

        self.keyboard.col_pins = (DigitalInOut(),)
        self.keyboard.row_pins = self.pins
        self.keyboard.diode_orientation = DiodeOrientation.COL2ROW
        self.keyboard.matrix = MatrixScanner(
            cols=self.keyboard.col_pins,
            rows=self.keyboard.row_pins,
            diode_orientation=self.keyboard.diode_orientation,
        )
        self.keyboard.keymap = keymap

        self.keyboard._init(hid_type=HIDModes.NOOP)

    @patch('kmk.hid.AbstractHID.hid_send')
    def test(self, testname, key_events, assert_reports, hid_send):
        if self.debug_enabled:
            print(testname)

        # setup report recording
        hid_reports = []
        hid_send.side_effect = lambda report: hid_reports.append(report[1:])

        # inject key switch events
        self.keyboard._main_loop()
        for e in key_events:
            if isinstance(e, int):
                starttime_ms = time.time_ns() // 1_000_000
                while time.time_ns() // 1_000_000 - starttime_ms < e:
                    self.do_main_loop()
            else:
                key_pos = e[0]
                is_pressed = e[1]
                self.pins[key_pos].value = is_pressed
                self.do_main_loop()

        # wait up to 10s for delayed actions to resolve, if there are any
        timeout = time.time_ns() + 10 * 1_000_000_000
        while timeout > time.time_ns():
            self.do_main_loop()
            if not self.keyboard._timeouts and not self.keyboard._resume_buffer:
                break
        assert timeout > time.time_ns(), 'infinite loop detected'

        matching = True
        for i in range(max(len(hid_reports), len(assert_reports))):
            # prepare the generated report codes
            try:
                hid_report = hid_reports[i]
            except IndexError:
                report_mods = None
                report_keys = [None]
            else:
                report_mods = hid_report[0]
                report_keys = {code for code in hid_report[2:] if code != 0}

            # prepare the desired report codes
            try:
                hid_assert = assert_reports[i]
            except IndexError:
                assert_mods = None
                assert_keys = [None]
            else:
                assert_mods = 0
                assert_keys = set()
                for k in hid_assert:
                    if isinstance(k, ModifierKey):
                        assert_mods |= k.code
                    else:
                        assert_keys.add(k.code)

            # accumulate assertion for late evalution, -- makes for a more
            # helpfull debug output.
            matching = matching and report_mods == assert_mods
            matching = matching and report_keys == assert_keys

            if self.debug_enabled:
                report_keys_names = {code2name(c) for c in report_keys}
                assert_keys_names = {code2name(c) for c in assert_keys}
                print(
                    f'assert '
                    f'mods: {report_mods} == {assert_mods} '
                    f'keys: {report_keys_names} == {assert_keys_names} '
                )

        assert matching, "reports don't match up"

    def do_main_loop(self):
        self.keyboard._main_loop()
        time.sleep(self.loop_delay_ms / 1000)
