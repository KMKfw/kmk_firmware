import unittest

from kmk.keys import KC
from tests.keyboard_test import KeyboardTest


class TestKmkKeyboard(unittest.TestCase):
    def test_basic_kmk_keyboard(self):
        keyboard = KeyboardTest([], [[KC.N1, KC.N2, KC.N3, KC.N4]])

        keyboard.test('Simple key press', [(0, True), (0, False)], [{KC.N1}, {}])


if __name__ == '__main__':
    unittest.main()
