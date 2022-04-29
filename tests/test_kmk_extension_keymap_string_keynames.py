import unittest

from kmk.extensions.keymap_string_keynames import keymap_string_keynames
from kmk.keys import KC
from tests.keyboard_test import KeyboardTest


class Test_extension_keymap_string_keynames(unittest.TestCase):
    def test_basic_kmk_keyboard_replace_string_primary_name(self):
        keyboard = KeyboardTest(
            [], [['1', '2', '3', '4']], extensions={keymap_string_keynames()}
        )

        keyboard.test('Simple key press', [(0, True), (0, False)], [{KC.N1}, {}])

    def test_basic_kmk_keyboard_replace_string_secondary_name(self):
        keyboard = KeyboardTest(
            [], [['N1', 'N2', 'N3', 'N4']], extensions={keymap_string_keynames()}
        )

        keyboard.test('Simple key press', [(0, True), (0, False)], [{KC.N1}, {}])


if __name__ == '__main__':
    unittest.main()
