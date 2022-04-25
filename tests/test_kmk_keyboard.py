import unittest

from kmk.keys import KC
from tests.keyboard_test import KeyboardTest


class TestKmkKeyboard(unittest.TestCase):
    def test_basic_kmk_keyboard(self):
        keyboard = KeyboardTest([], [[KC.N1, KC.N2, KC.N3, KC.N4]])

        keyboard.test('Simple key press', [(0, True), (0, False)], [{KC.N1}, {}])

    def test_basic_kmk_keyboard_replace_string_primary_name(self):
        keyboard = KeyboardTest([], [['1', '2', '3', '4']])

        keyboard.test('Simple key press', [(0, True), (0, False)], [{KC.N1}, {}])

    def test_basic_kmk_keyboard_replace_string_secondary_name(self):
        keyboard = KeyboardTest([], [['N1', 'N2', 'N3', 'N4']])

        keyboard.test('Simple key press', [(0, True), (0, False)], [{KC.N1}, {}])

    def test_basic_kmk_keyboard_unknown_replacement_string(self):
        with self.assertRaises(ValueError):
            KeyboardTest([], [['UNKNOWN1', 'UNKNOWN2', 'UNKNOWN3', 'UNKNOWN4']])


if __name__ == '__main__':
    unittest.main()
