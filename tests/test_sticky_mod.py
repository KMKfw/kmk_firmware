import unittest

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.sticky_mod import StickyMod
from tests.keyboard_test import KeyboardTest


class TestStickyMod(unittest.TestCase):
    def test_basic_kmk_keyboard(self):

        keyboard = KeyboardTest(
            [Layers(), StickyMod()],
            [
                [
                    KC.A,
                    KC.B,
                    KC.MO(1),
                    KC.LT(1, KC.C),
                    KC.SM(kc=KC.TAB, mod=KC.LCTL(KC.LSFT)),
                    KC.F,
                ],
                [
                    KC.SM(kc=KC.TAB, mod=KC.LGUI),
                    KC.SM(kc=KC.TAB, mod=KC.LSFT(KC.LGUI)),
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
                (4, True),
                (4, False),
                (1, True),
                (1, False),
            ],
            [
                {KC.LSFT, KC.LCTL, KC.TAB},
                {KC.LSFT, KC.LCTL},
                {KC.LSFT, KC.LCTL, KC.TAB},
                {KC.LSFT, KC.LCTL},
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
                (0, True),
                (0, False),
                (0, True),
                (0, False),
                (1, True),
                (1, False),
                (1, True),
                (1, False),
                (0, True),
                (0, False),
                (3, True),
                (3, False),
                (2, False),
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
                {KC.LSFT, KC.LCTL, KC.TAB},
                {KC.LSFT, KC.LCTL},
                {KC.B},
                {},
            ],
        )


if __name__ == '__main__':
    unittest.main()
