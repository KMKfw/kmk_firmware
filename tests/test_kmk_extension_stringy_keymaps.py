import unittest

from kmk.extensions.stringy_keymaps import StringyKeymaps
from kmk.keys import KC
from tests.keyboard_test import KeyboardTest


class Test_extension_stringy_keymaps(unittest.TestCase):
    def test_basic_kmk_keyboard_replace_string_primary_name(self):
        keyboard = KeyboardTest(
            [], [['1', '2', '3', '4']], extensions=[StringyKeymaps()]
        )

        keyboard.test('Simple key press', [(0, True), (0, False)], [{KC.N1}, {}])

    def test_basic_kmk_keyboard_replace_string_secondary_name(self):
        keyboard = KeyboardTest(
            [], [['N1', 'N2', 'N3', 'N4']], extensions=[StringyKeymaps()]
        )

        keyboard.test('Simple key press', [(0, True), (0, False)], [{KC.N1}, {}])


if __name__ == '__main__':
    unittest.main()
