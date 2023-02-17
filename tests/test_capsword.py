import unittest

from kmk.keys import KC
from kmk.modules.capsword import CapsWord
from tests.keyboard_test import KeyboardTest

# TODO: Add tests for custom and default ignored keys, custom and default timeouts


class TestCapsWord(unittest.TestCase):
    def setUp(self):
        self.kb = KeyboardTest(
            [CapsWord()],
            [
                [KC.CW, KC.A, KC.Z, KC.N1, KC.N0, KC.SPC],
            ],
            debug_enabled=False,
        )

    def test_capsword(self):
        self.kb.test(
            'CapsWord',
            [
                (1, True),
                (1, False),
                (0, True),
                (0, False),
                (1, True),
                (1, False),
                (2, True),
                (2, False),
                (3, True),
                (3, False),
                (4, True),
                (4, False),
                (1, True),
                (1, False),
                (5, True),
                (5, False),
                (1, True),
                (1, False),
            ],
            [
                {KC.A},
                {},
                {KC.LSFT, KC.A},
                {},
                {KC.LSFT, KC.Z},
                {},
                {KC.N1},
                {},
                {KC.N0},
                {},
                {KC.LSFT, KC.A},
                {},
                {KC.SPC},
                {},
                {KC.A},
                {},
            ],
        )


if __name__ == '__main__':
    unittest.main()
