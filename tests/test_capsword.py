import unittest

from kmk.keys import KC
from kmk.modules.capsword import CapsWord
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from tests.keyboard_test import KeyboardTest


class TestCapsWord(unittest.TestCase):
    def test_basic_kmk_keyboard(self):
        keyboard = KeyboardTest(
            [CapsWord(1000), Layers(), ModTap()],
            [
                [
                    KC.CW,
                    KC.B,
                    KC.C,
                    KC.COMMA,
                    KC.UNDS,
                    KC.MO(1),
                    KC.MT(KC.COMMA, KC.LCTRL),
                ],
                [KC.A, KC.B, KC.D, KC.N4, KC.N5, KC.A, KC.B],
                [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.A, KC.B],
            ],
            debug_enabled=False,
        )

        keyboard.test(
            'basic capsword behaviour',
            [
                (0, True),
                (0, False),
                (1, True),
                (1, False),
                (0, True),
                (0, False),
                (1, True),
                (1, False),
            ],
            [
                {KC.LSFT, KC.B},
                {},
                {KC.B},
                {},
            ],
        )

        keyboard.test(
            'capsword timeout behaviour1',
            [
                (0, True),
                (0, False),
                1020,
                (1, True),
                (1, False),
            ],
            [
                {KC.B},
                {},
            ],
        )

        keyboard.test(
            'capsword timeout behaviour2',
            [
                (0, True),
                (0, False),
                (1, True),
                (1, False),
                980,
                (2, True),
                (2, False),
                (2, True),
                (2, False),
                1010,
                (2, True),
                (2, False),
            ],
            [
                {KC.LSFT, KC.B},
                {},
                {KC.LSFT, KC.C},
                {},
                {KC.LSFT, KC.C},
                {},
                {KC.C},
                {},
            ],
        )

        keyboard.test(
            'capsword with ignore keys',
            [
                (0, True),
                (0, False),
                (4, True),
                (4, False),
                (1, True),
                (1, False),
                (3, True),
                (3, False),
                (2, True),
                (2, False),
                (0, True),
                (0, False),
                (2, True),
                (2, False),
                (0, True),
                (0, False),
            ],
            [
                {KC.LSFT, KC.MINS},
                {},
                {KC.LSFT, KC.B},
                {},
                {KC.COMMA},
                {},
                {KC.C},
                {},
                {KC.LSFT, KC.C},
                {},
            ],
        )

        keyboard.test(
            'capsword with rollover keys',
            [
                (0, True),
                (0, False),
                (4, True),
                (1, True),
                (4, False),
                (1, False),
                (3, True),
                (3, False),
                (2, True),
                (2, False),
                (0, True),
                (0, False),
                (2, True),
                (2, False),
                (0, True),
                (0, False),
            ],
            [
                {KC.LSFT, KC.UNDS},
                {KC.LSFT, KC.B, KC.UNDS},
                {KC.LSFT, KC.B},
                {},
                {KC.COMMA},
                {},
                {KC.C},
                {},
                {KC.LSFT, KC.C},
                {},
            ],
        )

        keyboard.test(
            'capsword with mod tap ',
            [
                (0, True),
                (0, False),
                (6, True),
                350,
                (6, False),
                (2, True),
                (2, False),
                (6, True),
                (6, False),
                200,
                (2, True),
                (2, False),
                (0, True),
                (0, False),
            ],
            [
                {KC.LCTL},
                {},
                {KC.LSFT, KC.C},
                {},
                {KC.COMMA},
                {},
                {KC.LSFT, KC.C},
                {},
            ],
        )

        keyboard.test(
            'capsword with layer tap ',
            [
                (0, True),
                (0, False),
                (5, True),
                350,
                (2, True),
                (2, False),
                (5, False),
                (2, True),
                (2, False),
                (0, True),
                (0, False),
                (2, True),
                (2, False),
            ],
            [
                {KC.LSFT, KC.D},
                {},
                {KC.LSFT, KC.C},
                {},
                {KC.C},
                {},
            ],
        )


if __name__ == '__main__':
    unittest.main()
