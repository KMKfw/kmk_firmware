import unittest

from kmk.keys import KC, Key, ModifierKey
from tests.keyboard_test import KeyboardTest


class TestKmkKeys(unittest.TestCase):
    def test_basic_kmk_keyboard(self):
        keyboard = KeyboardTest(
            [],
            [
                [
                    KC.HASH,
                    KC.RALT(KC.HASH),
                    KC.RALT(KC.LSFT)(KC.N3),
                    KC.RALT(KC.LSFT),
                    KC.RALT,
                ]
            ],
        )
        keyboard.test(
            'Shifted key',
            [(0, True), (0, False)],
            [
                {
                    KC.N3,
                    KC.LSFT,
                },
                {},
            ],
        )
        keyboard.test(
            'Shift+AltGr+key',
            [(1, True), (1, False)],
            [
                {
                    KC.N3,
                    KC.LSFT,
                    KC.RALT,
                },
                {},
            ],
        )
        keyboard.test(
            'Shift+AltGr+key, alternate chaining',
            [(2, True), (2, False)],
            [
                {
                    KC.N3,
                    KC.LSFT,
                    KC.RALT,
                },
                {},
            ],
        )
        keyboard.test(
            'Shift+AltGr',
            [(3, True), (3, False)],
            [
                {
                    KC.LSFT,
                    KC.RALT,
                },
                {},
            ],
        )
        keyboard.test(
            'AltGr',
            [(4, True), (4, False)],
            [
                {
                    KC.RALT,
                },
                {},
            ],
        )

        assert isinstance(KC.RGUI(no_press=True), ModifierKey)
        assert isinstance(KC.RALT(KC.RGUI), ModifierKey)
        assert isinstance(KC.Q(no_press=True), Key)
        assert not isinstance(KC.Q(no_press=True), ModifierKey)
        assert isinstance(KC.RALT(KC.Q), Key)
        assert not isinstance(KC.RALT(KC.Q), ModifierKey)


if __name__ == '__main__':
    unittest.main()
