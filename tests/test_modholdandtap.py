import unittest

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modholdandtap import ModHoldAndTap
from tests.keyboard_test import KeyboardTest


class TestModHoldLayerTap(unittest.TestCase):
    def test_basic_kmk_keyboard(self):

        keyboard = KeyboardTest(
            [Layers(), ModHoldAndTap()],
            [
                [
                    KC.A,
                    KC.B,
                    KC.MO(1),
                    KC.LT(1, KC.C),
                    KC.MHAT(kc=KC.TAB, mod=KC.LCTL(KC.LSFT)),
                    KC.F,
                ],
                [
                    KC.MHAT(kc=KC.TAB, mod=KC.LGUI),
                    KC.MHAT(kc=KC.TAB, mod=KC.LSFT(KC.LGUI)),
                    KC.TRNS,
                    KC.B,
                    KC.N5,
                ],
                [KC.A, KC.B, KC.N3, KC.N4, KC.N5],
            ],
            debug_enabled=False,
        )

        keyboard.test(
            'basic test',
            [
                (4, True),
                (4, False),
                100,
                (4, True),
                200,
                (4, False),
                100,
                (1, True),
                (1, False),
            ],
            [
                {KC.B},
                {},
            ],
        )

        keyboard.test(
            'basic test with MO',
            [
                (1, True),
                (1, False),
                (2, True),
                200,
                (0, True),
                50,
                (0, False),
                50,
                (0, True),
                50,
                (0, False),
                (1, True),
                (1, False),
                50,
                (1, True),
                (1, False),
                (0, True),
                50,
                (0, False),
                (3, True),
                (3, False),
                (2, False),
                100,
                (4, True),
                (4, False),
                (1, True),
                (1, False),
            ],
            [
                {KC.B},
                {},
                {KC.LGUI, KC.TAB},
                {KC.LGUI},
                {KC.LGUI, KC.TAB},
                {KC.LGUI},
                {KC.LSFT, KC.LGUI, KC.TAB},
                {KC.LSFT, KC.LGUI},
                {KC.LSFT, KC.LGUI, KC.TAB},
                {KC.LSFT, KC.LGUI},
                {KC.LGUI, KC.TAB},
                {KC.LGUI},
                {KC.B},
                {},
                {KC.B},
                {},
            ],
        )


if __name__ == '__main__':
    unittest.main()
