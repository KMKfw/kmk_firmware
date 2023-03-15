import unittest

from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.tapdance import TapDance
from tests.keyboard_test import KeyboardTest


class TestTapDance(unittest.TestCase):
    def setUp(self):
        self.t_within = 2 * KeyboardTest.loop_delay_ms
        self.t_after = 10 * KeyboardTest.loop_delay_ms
        tap_time = (self.t_after + self.t_within) // 4 * 3

        TapDance.tap_time = tap_time

        self.keyboard = KeyboardTest(
            [Layers(), HoldTap(), TapDance()],
            [
                [
                    KC.TD(KC.N0, KC.N1),
                    KC.TD(
                        KC.HT(KC.N1, KC.A),
                        KC.HT(KC.N2, KC.B, tap_time=2 * tap_time),
                    ),
                    KC.TD(KC.HT(KC.X, KC.Y), KC.X, tap_time=0),
                    KC.TD(KC.LT(1, KC.N3), KC.X, tap_time=0),
                    KC.N4,
                ],
                [KC.N9, KC.N8, KC.N7, KC.N6, KC.N5],
            ],
            debug_enabled=False,
        )

    def test_normal_key(self):
        keyboard = self.keyboard
        t_within = self.t_within

        keyboard.test('Tap x1', [(0, True), (0, False)], [{KC.N0}, {}])

        keyboard.test(
            'Tap x2',
            [(0, True), (0, False), t_within, (0, True), (0, False)],
            [{KC.N1}, {}],
        )

        keyboard.test(
            'Tap x3',
            [
                (0, True),
                (0, False),
                (0, True),
                (0, False),
                (0, True),
                (0, False),
            ],
            [{KC.N1}, {}, {KC.N0}, {}],
        )

        keyboard.test(
            'Tap x1 interrupted',
            [(0, True), (4, True), (4, False), (0, False)],
            [{KC.N0}, {KC.N0, KC.N4}, {KC.N0}, {}],
        )

        keyboard.test(
            'Tap x1 interrupted',
            [(0, True), (4, True), (0, False), (4, False)],
            [{KC.N0}, {KC.N0, KC.N4}, {KC.N4}, {}],
        )

        keyboard.test(
            'Tap x1 interrupted',
            [(0, True), (0, False), (4, True), (4, False)],
            [{KC.N0}, {}, {KC.N4}, {}],
        )

        keyboard.test(
            'Tap x2, interrupted',
            [
                (0, True),
                (0, False),
                t_within,
                (0, True),
                (4, True),
                (0, False),
                (4, False),
            ],
            [{KC.N1}, {KC.N1, KC.N4}, {KC.N4}, {}],
        )

    def test_holdtap(self):
        keyboard = self.keyboard
        t_within = self.t_within
        t_after = self.t_after

        keyboard.test('Tap x1', [(1, True), (1, False)], [{KC.N1}, {}])

        keyboard.test(
            'Tap x2',
            [(1, True), (1, False), t_within, (1, True), (1, False)],
            [{KC.N2}, {}],
        )

        keyboard.test('Hold', [(1, True), t_after, (1, False)], [{KC.A}, {}])

        keyboard.test(
            'Tap-Hold',
            [(1, True), (1, False), t_within, (1, True), 2 * t_after, (1, False)],
            [{KC.B}, {}],
        )

        keyboard.test(
            'Tap-Hold interrupted',
            [
                (1, True),
                (1, False),
                t_within,
                (1, True),
                t_within,
                (4, True),
                (4, False),
                (1, False),
            ],
            [{KC.B}, {KC.B, KC.N4}, {KC.B}, {}],
        )

    def test_multi_tapdance(self):
        keyboard = self.keyboard
        t_within = self.t_within
        t_after = self.t_after

        keyboard.test(
            '',
            [(0, True), (0, False), t_within, (1, True), (1, False)],
            [{KC.N0}, {}, {KC.N1}, {}],
        )

        keyboard.test(
            '',
            [
                (0, True),
                (0, False),
                (0, True),
                (2, True),
                (2, False),
                t_after,
                (0, False),
            ],
            [{KC.N1}, {KC.N1, KC.X}, {KC.N1}, {}],
        )

        keyboard.test(
            '',
            [
                (2, True),
                (2, False),
                (2, True),
                (0, True),
                (0, False),
                t_after,
                (2, False),
            ],
            [{KC.X}, {KC.X, KC.N0}, {KC.X}, {}],
        )

    def test_layer(self):
        keyboard = self.keyboard
        t_within = self.t_within
        t_after = self.t_after

        keyboard.test(
            '',
            [(3, True), (3, False), t_within, (1, True), (1, False)],
            [{KC.N3}, {}, {KC.N1}, {}],
        )

        keyboard.test(
            '', [(3, True), t_after, (1, True), (1, False), (3, False)], [{KC.N8}, {}]
        )

        keyboard.test(
            '', [(3, True), t_after, (1, True), (3, False), (1, False)], [{KC.N8}, {}]
        )

        keyboard.test(
            '',
            [
                (1, True),
                (3, True),
                t_after,
                (1, False),
                (4, True),
                (4, False),
                (3, False),
                (1, False),
            ],
            [{KC.A}, {}, {KC.N5}, {}],
        )

    def test_holdtap_repeat(self):
        keyboard = self.keyboard
        t_after = self.t_after

        keyboard.test(
            'HoldTap repeat',
            [
                (2, True),
                (2, False),
                (2, True),
                t_after,
                (4, True),
                (2, False),
                (4, False),
            ],
            [{KC.X}, {KC.X, KC.N4}, {KC.N4}, {}],
        )


if __name__ == '__main__':
    unittest.main()
