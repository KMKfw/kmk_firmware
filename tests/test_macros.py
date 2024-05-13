import unittest

from kmk.keys import KC
from kmk.modules.macros import (
    Delay,
    Macros,
    Press,
    Release,
    Tap,
    UnicodeModeIBus,
    UnicodeModeMac,
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
                ]
            ],
            debug_enabled=True,
        )

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
        self.macros.unicode_mode = UnicodeModeMac
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

    def test_8_winc(self):
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


if __name__ == '__main__':
    unittest.main()
