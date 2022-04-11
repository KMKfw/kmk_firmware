import unittest

from kmk.keys import KC
from kmk.modules.cg_swap import CgSwap
from kmk.modules.modtap import ModTap
from tests.keyboard_test import KeyboardTest


class TestCgSwap(unittest.TestCase):
    def test_basic_kmk_keyboard(self):
        keyboard = KeyboardTest(
            [CgSwap(), ModTap()],
            [
                [
                    KC.CG_SWAP,
                    KC.CG_NORM,
                    KC.CG_TOGG,
                    KC.LCMD,
                    KC.LCTL,
                    KC.RGUI,
                    KC.RCTL,
                    KC.MT(KC.A, KC.LCTRL),
                ]
            ],
            debug_enabled=True,
        )

        keyboard.test(
            'cg swap behaviour with lgui and lctl',
            [
                (3, True),
                (3, False),
                (0, True),
                (0, False),
                (3, True),
                (3, False),
                (1, True),
                (1, False),
                (3, True),
                (3, False),
                (2, True),
                (2, False),
                (4, True),
                (4, False),
                (2, True),
                (2, False),
                (4, True),
                (4, False),
            ],
            [
                {KC.LGUI},
                {},
                {KC.LCTL},
                {},
                {KC.LGUI},
                {},
                {KC.LGUI},
                {},
                {KC.LCTL},
                {},
            ],
        )

        keyboard.test(
            'cg swap behaviour with rgui and rctl',
            [
                (5, True),
                (5, False),
                (0, True),
                (0, False),
                (5, True),
                (5, False),
                (1, True),
                (1, False),
                (5, True),
                (5, False),
                (2, True),
                (2, False),
                (6, True),
                (6, False),
                (2, True),
                (2, False),
                (6, True),
                (6, False),
            ],
            [
                {KC.RGUI},
                {},
                {KC.RCTL},
                {},
                {KC.RGUI},
                {},
                {KC.RGUI},
                {},
                {KC.RCTL},
                {},
            ],
        )

        keyboard.test(
            'cg swap behaviour modtap',
            [
                (7, True),
                350,
                (7, False),
                (0, True),
                (0, False),
                (7, True),
                350,
                (7, False),
                (2, True),
                (2, False),
                (7, True),
                350,
                (7, False),
            ],
            [
                {KC.LCTL},
                {},
                {KC.LGUI},
                {},
                {KC.LCTL},
                {},
            ],
        )


if __name__ == '__main__':
    unittest.main()
