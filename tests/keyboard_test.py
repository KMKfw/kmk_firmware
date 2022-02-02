import random
import time
from functools import reduce
from unittest.mock import Mock, patch

from kmk.hid import HIDModes
from kmk.keys import ModifierKey
from kmk.kmk_keyboard import KMKKeyboard
from kmk.matrix import DiodeOrientation


class DigitalInOut(Mock):
    value = False


class KeyboardTest:
    def __init__(
        self, modules, keymap, keyboard_debug_enabled=False, debug_enabled=False
    ):
        self.debug_enabled = debug_enabled

        self.keyboard = KMKKeyboard()
        self.keyboard.debug_enabled = keyboard_debug_enabled

        self.keyboard.modules = modules

        self.pins = tuple(DigitalInOut() for k in keymap[0])

        self.keyboard.col_pins = (DigitalInOut(),)
        self.keyboard.row_pins = self.pins
        self.keyboard.diode_orientation = DiodeOrientation.COL2ROW
        self.keyboard.keymap = keymap

        self.keyboard._init(hid_type=HIDModes.NOOP)

    @patch('kmk.hid.AbstractHID.hid_send')
    def test(self, testname, key_events, assert_hid_reports, hid_send):
        if self.debug_enabled:
            print(testname, key_events, assert_hid_reports)

        hid_send_call_arg_list = []
        hid_send.side_effect = lambda hid_report: hid_send_call_arg_list.append(
            hid_report[1:]
        )

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

        if self.debug_enabled:
            for hid_report in hid_send_call_arg_list:
                print(hid_report)

        assert len(hid_send_call_arg_list) >= len(assert_hid_reports)

        for i, hid_report in enumerate(
            hid_send_call_arg_list[-len(assert_hid_reports) :]
        ):
            hid_report_keys = {code for code in hid_report[2:] if code != 0}
            assert_keys = {
                k.code for k in assert_hid_reports[i] if not isinstance(k, ModifierKey)
            }
            if self.debug_enabled:
                print(
                    'assert keys:',
                    hid_report_keys == assert_keys,
                    hid_report_keys,
                    assert_keys,
                )
            assert hid_report_keys == assert_keys

            hid_report_modifiers = hid_report[0]
            assert_modifiers = reduce(
                lambda mod, all_mods: all_mods | mod,
                {k.code for k in assert_hid_reports[i] if isinstance(k, ModifierKey)},
                0,
            )
            if self.debug_enabled:
                print(
                    'assert mods:',
                    hid_report_modifiers == assert_modifiers,
                    hid_report_modifiers,
                    assert_modifiers,
                )
            assert hid_report_modifiers == assert_modifiers

    def do_main_loop(self):
        for i in range(random.randint(5, 50)):
            self.keyboard._main_loop()
