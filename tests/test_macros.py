import unittest

from kmk.keys import KC
from kmk.modules.macros import (
    Delay,
    Macros,
    Press,
    Release,
    Tap,
    UnicodeModeIBus,
    UnicodeModeMacOS,
    UnicodeModeWinC,
)
from tests.keyboard_test import KeyboardTest


class TestMacro(unittest.TestCase):
    def setUp(self):
        self.macros = Macros()
        self.kb = KeyboardTest(
            [self.macros],
            [
                [
                    KC.MACRO(Press(KC.A), Release(KC.A)),
                    KC.MACRO(Press(KC.A), Press(KC.B), Release(KC.A), Release(KC.B)),
                    KC.MACRO(Tap(KC.A), Tap(KC.A)),
                    KC.MACRO(Tap(KC.A), Delay(10), Tap(KC.B)),
                    KC.Y,
                    KC.MACRO('Foo1'),
                    KC.MACRO(Press(KC.LCTL), 'Foo1', Release(KC.LCTL)),
                    KC.MACRO('🍺!'),
                    KC.MACRO(on_press='p'),
                    KC.MACRO(on_hold='h'),
                    KC.MACRO(on_release='r'),
                    KC.MACRO(on_press='p', on_hold='h', on_release='r'),
                    KC.MACRO('bar', blocking=False),
                    KC.MACRO(on_press='q', on_hold='i', on_release='s', blocking=False),
                ]
            ],
            debug_enabled=False,
        )
        self.hold = self.kb.loop_delay_ms * 15

    def test_0(self):
        self.kb.test(
            '',
            [(0, True), (0, False)],
            [{KC.A}, {}],
        )

    def test_1(self):
        self.kb.test(
            '',
            [(1, True), (1, False)],
            [{KC.A}, {KC.A, KC.B}, {KC.B}, {}],
        )

    def test_2(self):
        self.kb.test(
            '',
            [(2, True), (2, False)],
            [{KC.A}, {}, {KC.A}, {}],
        )

    def test_3(self):
        self.kb.test(
            '',
            [(3, True), (3, False)],
            [{KC.A}, {}, {KC.B}, {}],
        )

    def test_4(self):
        self.kb.test(
            '',
            [(3, True), (3, False), (4, True), (4, False)],
            [{KC.A}, {}, {KC.B}, {}, {KC.Y}, {}],
        )

    def test_5(self):
        self.kb.test(
            '',
            [(5, True), (5, False)],
            [{KC.LSFT, KC.F}, {}, {KC.O}, {}, {KC.O}, {}, {KC.N1}, {}],
        )

    def test_6(self):
        self.kb.test(
            '',
            [(6, True), (6, False)],
            [
                {KC.LCTL},
                {KC.LCTL, KC.LSFT, KC.F},
                {KC.LCTL},
                {KC.LCTL, KC.O},
                {KC.LCTL},
                {KC.LCTL, KC.O},
                {KC.LCTL},
                {KC.LCTL, KC.N1},
                {KC.LCTL},
                {},
            ],
        )

    def test_7_ibus(self):
        self.kb.test(
            '',
            [(7, True), (7, False)],
            [
                {KC.LCTL, KC.LSFT, KC.U},
                {},
                {KC.N1},
                {},
                {KC.F},
                {},
                {KC.N3},
                {},
                {KC.N7},
                {},
                {KC.A},
                {},
                {KC.ENTER},
                {},
                {KC.LSFT, KC.N1},
                {},
            ],
        )

    def test_7_ibus_explicit(self):
        self.macros.unicode_mode = UnicodeModeIBus
        self.kb.test(
            '',
            [(7, True), (7, False)],
            [
                {KC.LCTL, KC.LSFT, KC.U},
                {},
                {KC.N1},
                {},
                {KC.F},
                {},
                {KC.N3},
                {},
                {KC.N7},
                {},
                {KC.A},
                {},
                {KC.ENTER},
                {},
                {KC.LSFT, KC.N1},
                {},
            ],
        )

    def test_7_ralt(self):
        self.macros.unicode_mode = UnicodeModeMacOS
        self.kb.test(
            '',
            [(7, True), (7, False)],
            [
                {KC.LALT},
                {KC.LALT, KC.N1},
                {KC.LALT},
                {KC.LALT, KC.F},
                {KC.LALT},
                {KC.LALT, KC.N3},
                {KC.LALT},
                {KC.LALT, KC.N7},
                {KC.LALT},
                {KC.LALT, KC.A},
                {KC.LALT},
                {},
                {KC.LSFT, KC.N1},
                {},
            ],
        )

    def test_7_winc(self):
        self.macros.unicode_mode = UnicodeModeWinC
        self.kb.test(
            '',
            [(7, True), (7, False)],
            [
                {KC.RALT, KC.U},
                {},
                {KC.N1},
                {},
                {KC.F},
                {},
                {KC.N3},
                {},
                {KC.N7},
                {},
                {KC.A},
                {},
                {KC.ENTER},
                {},
                {KC.LSFT, KC.N1},
                {},
            ],
        )

    def test_8(self):
        self.kb.test(
            '',
            [(8, True), (8, False)],
            [{KC.P}, {}],
        )

    def test_9(self):
        self.kb.test(
            '',
            [(9, True), self.hold, (9, False)],
            [{KC.H}, {}, {KC.H}, {}],
        )

    def test_10(self):
        self.kb.test(
            '',
            [(10, True), (10, False)],
            [{KC.R}, {}],
        )

    def test_11_0(self):
        self.kb.test(
            '',
            [(11, True), 2 * self.hold, (11, False)],
            [{KC.P}, {}, {KC.H}, {}, {KC.H}, {}, {KC.R}, {}],
        )

    def test_11_1(self):
        self.kb.test(
            '',
            [(11, True), self.hold, (11, False), (11, True), (11, False)],
            [{KC.P}, {}, {KC.H}, {}, {KC.R}, {}, {KC.P}, {}, {KC.R}, {}],
        )

    def test_11_2(self):
        self.kb.test(
            '',
            [(11, True), (11, False), (11, True), (11, False)],
            [{KC.P}, {}, {KC.R}, {}, {KC.P}, {}, {KC.R}, {}],
        )

    def test_11_3(self):
        self.kb.test(
            '',
            [(4, True), (11, True), (4, False), self.hold, (11, False)],
            [
                {KC.Y},
                {KC.P, KC.Y},
                {KC.Y},
                {KC.H, KC.Y},
                {KC.Y},
                {KC.R, KC.Y},
                {KC.Y},
                {},
            ],
        )

    def test_12_0(self):
        self.kb.test(
            '',
            [(12, True), (12, False), (4, True), (4, False)],
            [{KC.B}, {KC.B, KC.Y}, {KC.B}, {}, {KC.A}, {}, {KC.R}, {}],
        )

    def test_12_1(self):
        self.kb.test(
            '',
            [(12, True), (12, False), (12, True), (12, False)],
            [{KC.B}, {}, {KC.A}, {}, {KC.R}, {}, {KC.B}, {}, {KC.A}, {}, {KC.R}, {}],
        )

    def test_13_0(self):
        self.kb.test(
            '',
            [(13, True), (13, False), (11, True), (11, False)],
            [{KC.Q}, {KC.P, KC.Q}, {KC.P}, {}, {KC.S}, {KC.S, KC.R}, {KC.R}, {}],
        )

    def test_13_1(self):
        self.kb.test(
            '',
            [(13, True), (11, True), (13, False), (11, False)],
            [{KC.Q}, {KC.P, KC.Q}, {KC.P}, {}, {KC.S}, {KC.S, KC.R}, {KC.R}, {}],
        )

    def test_13_2(self):
        self.kb.test(
            '',
            [(13, True), (11, True), self.hold, (11, False), (13, False)],
            [
                {KC.Q},
                {KC.P, KC.Q},
                {KC.P},
                {},
                {KC.I},
                {KC.I, KC.H},
                {KC.H},
                {},
                {KC.S},
                {KC.S, KC.R},
                {KC.R},
                {},
            ],
        )

    def test_13_3(self):
        self.kb.test(
            '',
            [(11, True), (11, False), (13, True), (13, False)],
            [{KC.P}, {}, {KC.R}, {}, {KC.Q}, {}, {KC.S}, {}],
        )

    def test_13_4(self):
        self.kb.test(
            '',
            [(11, True), (13, True), (11, False), (13, False)],
            [{KC.P}, {}, {KC.R}, {}, {KC.Q}, {}, {KC.S}, {}],
        )

    def test_13_5(self):
        self.kb.test(
            '',
            [(4, True), (13, True), (4, False), (13, False)],
            [{KC.Y}, {KC.Q, KC.Y}, {KC.Q}, {}, {KC.S}, {}],
        )


class TestUnicodeModeKeys(unittest.TestCase):
    def setUp(self):
        self.macros = Macros()
        self.kb = KeyboardTest(
            [self.macros],
            [
                [
                    KC.UC_MODE_IBUS,
                    KC.UC_MODE_MACOS,
                    KC.UC_MODE_WINC,
                ]
            ],
            debug_enabled=False,
        )

    def test_ibus(self):
        self.kb.test('', [(0, True), (0, False)], [{}])
        self.assertEqual(self.macros.unicode_mode, UnicodeModeIBus)

    def test_mac(self):
        self.kb.test('', [(1, True), (1, False)], [{}])
        self.assertEqual(self.macros.unicode_mode, UnicodeModeMacOS)

    def test_winc(self):
        self.kb.test('', [(2, True), (2, False)], [{}])
        self.assertEqual(self.macros.unicode_mode, UnicodeModeWinC)


if __name__ == '__main__':
    unittest.main()
