import unittest

from kmk.keys import KC, Key, KeyboardKey, ModifiedKey, ModifierKey, make_key
from tests.keyboard_test import KeyboardTest


class TestKmkKeys(unittest.TestCase):
    def test_basic_kmk_keyboard(self):
        keyboard = KeyboardTest(
            [],
            [
                [
                    KC.NO,
                    KC.TRNS,
                ]
            ],
            debug_enabled=False,
        )

        keyboard.test(
            'No',
            [(0, True)],
            [{}],
        )
        self.assertEqual(keyboard.keyboard._coordkeys_pressed, {0: KC.NO})
        keyboard.test(
            'No',
            [(0, False)],
            [{}],
        )

        keyboard.test(
            'Transparent',
            [(1, True)],
            [{}],
        )
        self.assertEqual(keyboard.keyboard._coordkeys_pressed, {1: KC.TRNS})

        assert isinstance(KC.RGUI, ModifierKey)
        assert isinstance(KC.Q, Key)
        assert not isinstance(KC.Q, ModifierKey)

    def test_modified_keys(self):
        keyboard = KeyboardTest(
            [],
            [
                [
                    KC.N0,
                    KC.EXLM,
                    KC.RALT(KC.AT),
                    KC.RALT(KC.LSFT),
                    KC.RALT(KC.LSFT(KC.N4)),
                    KC.LSFT,
                    KC.N1,
                ]
            ],
            debug_enabled=False,
        )

        keyboard.test(
            'Shifted key',
            [(1, True), (1, False)],
            [{KC.LSFT, KC.N1}, {}],
        )

        keyboard.test(
            'Shifted key + key',
            [(1, True), (0, True), (0, False), (1, False)],
            [{KC.LSFT, KC.N1}, {KC.N0, KC.N1}, {KC.N1}, {}],
        )

        keyboard.test(
            'Shifted key + key rolled',
            [(1, True), (0, True), (1, False), (0, False)],
            [{KC.LSFT, KC.N1}, {KC.N0, KC.N1}, {KC.N0}, {}],
        )

        keyboard.test(
            'Shifted key + shift',
            [(1, True), (5, True), (5, False), (1, False)],
            [{KC.LSFT, KC.N1}, {KC.N1}, {}],
        )

        keyboard.test(
            'Shifted key + shift rolled',
            [(1, True), (5, True), (1, False), (5, False)],
            [{KC.LSFT, KC.N1}, {KC.LSFT}, {}],
        )

        keyboard.test(
            'Shifted key + unshifted key rolled',
            [(1, True), (6, True), (1, False), (6, False)],
            [{KC.LSFT, KC.N1}, {}, {KC.N1}, {}],
        )

        keyboard.test(
            'Unshifted key + shifted key rolled',
            [(6, True), (1, True), (6, False), (1, False)],
            [{KC.N1}, {}, {KC.LSFT, KC.N1}, {KC.LSFT}, {}],
        )

        keyboard.test(
            'Shift + shifted key',
            [(5, True), (1, True), (5, False), (1, False)],
            [{KC.LSFT}, {KC.LSFT, KC.N1}, {}],
        )

        keyboard.test(
            'Modified shifted key',
            [(2, True), (2, False)],
            [{KC.RALT, KC.LSFT, KC.N2}, {}],
        )

        keyboard.test(
            'Shifted key + modified shifted key rolled',
            [(1, True), (2, True), (1, False), (2, False)],
            [
                {KC.LSFT, KC.N1},
                {KC.RALT, KC.LSFT, KC.N1, KC.N2},
                {KC.RALT, KC.LSFT, KC.N2},
                {},
            ],
        )

        keyboard.test(
            'Modified modifier',
            [(3, True), (3, False)],
            [{KC.RALT, KC.LSFT}, {}],
        )

        keyboard.test(
            'Modified modifier + shifted key',
            [(3, True), (1, True), (1, False), (3, False)],
            [{KC.RALT, KC.LSFT}, {KC.RALT, KC.LSFT, KC.N1}, {KC.RALT, KC.LSFT}, {}],
        )

        keyboard.test(
            'Modified modified key',
            [(4, True), (4, False)],
            [{KC.RALT, KC.LSFT, KC.N4}, {}],
        )

        assert isinstance(KC.RALT(KC.RGUI), ModifiedKey)
        assert isinstance(KC.RALT(KC.Q), Key)
        assert not isinstance(KC.RALT(KC.Q), ModifierKey)
        self.assertEqual(KC.LSFT, KC.LSFT(KC.LSFT))
        self.assertEqual(
            KC.RALT(KC.LSFT).modifier.code, KC.RALT(KC.LSFT(KC.RALT)).modifier.code
        )


class TestKeys_dot(unittest.TestCase):
    def setUp(self):
        KC.clear()

    def test_expected_code_uppercase(self):
        assert 4 == KC.A.code

    def test_expected_code_lowercase(self):
        assert 4 == KC.a.code

    def test_case_ignored_alpha(self):
        upper_key = KC.A
        lower_key = KC.a
        assert upper_key is lower_key

    def test_case_requested_order_irrelevant(self):
        lower_key = KC.a
        upper_key = KC.A
        assert upper_key is lower_key

    def test_secondary_name(self):
        primary_key = KC.NO
        secondary_key = KC.XXXXXXX
        assert primary_key is secondary_key

    def test_invalid_key_upper(self):
        assert KC.INVALID_KEY == KC.NO

    def test_invalid_key_lower(self):
        assert KC.invalid_key == KC.NO

    def test_custom_key(self):
        created = make_key(
            names=('EURO', '€'),
            constructor=ModifiedKey,
            code=KC.N2.code,
            modifier=KC.LSFT(KC.ROPT).modifier,
        )
        assert created is KC.get('EURO')
        assert created is KC.get('€')

    def test_match_exactly_case(self):
        created = make_key(names=('ThIs_Is_A_StRaNgE_kEy',))
        assert created is KC.get('ThIs_Is_A_StRaNgE_kEy')


class TestKeys_index(unittest.TestCase):
    def setUp(self):
        KC.clear()

    def test_expected_code_uppercase(self):
        assert 4 == KC['A'].code

    def test_expected_code_lowercase(self):
        assert 4 == KC['a'].code

    def test_case_ignored_alpha(self):
        upper_key = KC['A']
        lower_key = KC['a']
        assert upper_key is lower_key

    def test_case_requested_order_irrelevant(self):
        lower_key = KC['a']
        upper_key = KC['A']
        assert upper_key is lower_key

    def test_invalid_key_upper(self):
        assert KC.INVALID_KEY == KC.NO

    def test_invalid_key_lower(self):
        assert KC.invalid_key == KC.NO

    def test_custom_key(self):
        created = make_key(
            names=('EURO', '€'),
            constructor=ModifiedKey,
            code=KC['N2'].code,
            modifier=KC.LSFT(KC.ROPT).modifier,
        )
        assert created is KC['EURO']
        assert created is KC['€']

    def test_match_exactly_case(self):
        created = make_key(names=('ThIs_Is_A_StRaNgE_kEy',))
        assert created is KC['ThIs_Is_A_StRaNgE_kEy']


class TestKeys_get(unittest.TestCase):
    def setUp(self):
        KC.clear()

    def test_expected_code_uppercase(self):
        assert 4 == KC.get('A').code

    def test_expected_code_lowercase(self):
        assert 4 == KC.get('a').code

    def test_case_ignored_alpha(self):
        upper_key = KC.get('A')
        lower_key = KC.get('a')
        assert upper_key is lower_key

    def test_case_requested_order_irrelevant(self):
        lower_key = KC.get('a')
        upper_key = KC.get('A')
        assert upper_key is lower_key

    def test_secondary_name(self):
        primary_key = KC.NO
        secondary_key = KC.XXXXXXX
        assert primary_key is secondary_key

    def test_invalid_key_upper(self):
        assert KC.get('INVALID_KEY') is KC.NO

    def test_invalid_key_lower(self):
        assert KC.get('not_a_valid_key') is KC.NO

    def test_custom_key(self):
        created = make_key(
            names=('EURO', '€'),
            constructor=ModifiedKey,
            code=KC.get('N2').code,
            modifier=KC.LSFT(KC.ROPT).modifier,
        )
        assert created is KC.get('EURO')
        assert created is KC.get('€')

    def test_match_exactly_case(self):
        created = make_key(names=('ThIs_Is_A_StRaNgE_kEy',))
        assert created is KC.get('ThIs_Is_A_StRaNgE_kEy')

    def test_underscore(self):
        assert KC.get('_')


# Some of these test appear silly, but they're testing we get the
# same, single, instance back when requested through KC and that
# order of request doesn't matter
class TestKeys_instances(unittest.TestCase):
    def setUp(self):
        KC.clear()

    def test_make_key_new_instance(self):
        key1 = make_key(names=(), constructor=KeyboardKey, code=1)
        key2 = make_key(names=(), constructor=KeyboardKey, code=1)
        assert key1 is not key2
        assert key1.code == key2.code

    def test_index_is_index(self):
        assert KC['A'] is KC['A']

    def test_index_is_dot(self):
        assert KC['A'] is KC.A

    def test_index_is_get(self):
        assert KC['A'] is KC.get('A')

    def test_dot_is_dot(self):
        assert KC.A is KC.A

    def test_dot_is_index(self):
        assert KC.A is KC['A']

    def test_dot_is_get(self):
        assert KC.A is KC.get('A')

    def test_get_is_get(self):
        assert KC.get('A') is KC.get('A')

    def test_get_is_index(self):
        assert KC.get('A') is KC['A']

    def test_get_is_dot(self):
        assert KC.get('A') is KC.A


if __name__ == '__main__':
    unittest.main()
