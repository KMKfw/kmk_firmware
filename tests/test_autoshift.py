import unittest

from kmk.keys import KC
from kmk.modules.autoshift import Autoshift
from tests.keyboard_test import KeyboardTest

tap_time = 3 * KeyboardTest.loop_delay_ms
t_after = 4 * KeyboardTest.loop_delay_ms


class TestAutoshift(unittest.TestCase):
    def setUp(self):
        self.kb = KeyboardTest(
            [Autoshift(tap_time=tap_time)],
            [
                [
                    KC.A,
                    KC.N1,
                    KC.HASH,
                    KC.NO,
                ]
            ],
            debug_enabled=False,
        )

    def test_tap_alpha(self):
        self.kb.test(
            '',
            [(0, True), (0, False)],
            [{KC.A}, {}],
        )

    def test_hold_alpha(self):
        self.kb.test(
            '',
            [(0, True), t_after, (0, False)],
            [{KC.A, KC.LSHIFT}, {}],
        )

    def test_hold_num(self):
        self.kb.test(
            '',
            [(1, True), t_after, (1, False)],
            [{KC.N1}, {}],
        )

    def test_hold_alpha_tap_num_within(self):
        self.kb.test(
            '',
            [(0, True), (1, True), t_after, (1, False), (0, False)],
            [{KC.A}, {KC.A, KC.N1}, {KC.A}, {}],
        )

    def test_hold_alpha_tap_num_after(self):
        self.kb.test(
            '',
            [(0, True), t_after, (1, True), (1, False), (0, False)],
            [{KC.A, KC.LSHIFT}, {KC.A, KC.N1}, {KC.A}, {}],
        )

    def test_hold_num_hold_alpha(self):
        self.kb.test(
            '',
            [(1, True), (0, True), t_after, (0, False), (1, False)],
            [{KC.N1}, {KC.N1, KC.A, KC.LSHIFT}, {KC.N1}, {}],
        )

    def test_roll_num_hold_alpha(self):
        self.kb.test(
            '',
            [(1, True), (0, True), (1, False), t_after, (0, False)],
            [{KC.N1}, {}, {KC.A, KC.LSHIFT}, {}],
        )

    def test_hold_shifted_hold_alpha(self):
        self.kb.test(
            '',
            [(2, True), (0, True), t_after, (2, False), (0, False)],
            [{KC.LSHIFT, KC.N3}, {KC.LSHIFT, KC.N3, KC.A}, {KC.A}, {}],
        )

    def test_hold_internal(self):
        self.kb.test(
            '',
            [(3, True), t_after, (3, False)],
            [],
        )


if __name__ == '__main__':
    unittest.main()
