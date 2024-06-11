import unittest

from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.key_repeat import KeyRepeat
from kmk.modules.layers import Layers
from tests.keyboard_test import KeyboardTest

t_within = 2 * KeyboardTest.loop_delay_ms
t_holdtap = 4 * KeyboardTest.loop_delay_ms
t_after = 6 * KeyboardTest.loop_delay_ms


class TestKeyRepeat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        KC.clear()

        key_repeat = KeyRepeat()

        holdtap = HoldTap()
        holdtap.tap_time = t_holdtap

        cls.keyboard = KeyboardTest(
            [Layers(), holdtap, key_repeat],
            [
                [
                    KC.REP,
                    KC.MO(1),
                    KC.HT(KC.T, KC.H),
                    KC.EXLM,
                ],
                [
                    KC.N0,
                    KC.N1,
                    KC.N2,
                    KC.N3,
                ],
            ],
            debug_enabled=False,
        )

    def test_key_repeat(self):
        self.keyboard.test(
            'repeat key on other layer twice',
            [
                (1, True),
                (2, True),
                (2, False),
                (1, False),
                (0, True),
                (0, False),
                (0, True),
                (0, False),
            ],
            [{KC.N2}, {}, {KC.N2}, {}, {KC.N2}, {}],
        )

        self.keyboard.test(
            'repeat key on holdtap tap',
            [(2, True), t_within, (2, False), (0, True), (0, False)],
            [{KC.T}, {}, {KC.T}, {}],
        )

        self.keyboard.test(
            'repeat key on holdtap hold',
            [(2, True), t_after, (2, False), (0, True), (0, False)],
            [{KC.H}, {}, {KC.H}, {}],
        )

        self.keyboard.test(
            'repeat key shifted',
            [(3, True), (3, False), (0, True), (0, False)],
            [{KC.LSFT, KC.N1}, {}, {KC.LSFT, KC.N1}, {}],
        )
