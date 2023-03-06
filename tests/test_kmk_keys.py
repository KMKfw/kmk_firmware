import unittest

from kmk.keys import KC, Key, ModifierKey, make_key
from tests.keyboard_test import KeyboardTest


class TestKmkKeys(unittest.TestCase):
    def test_basic_kmk_keyboard(self):
        keyboard = KeyboardTest(
            [],
            [
                [
                    KC.HASH,
                    KC.RALT(KC.HASH),
                    KC.RALT(KC.LSFT(KC.N3)),
                    KC.RALT(KC.LSFT),
                    # Note: this is correct, if unusual, syntax. It's a useful test because it failed silently on previous builds.
                    KC.RALT(KC.LSFT)(KC.N3),
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
            'AltGr+Shifted key',
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
            'AltGr+Shift+key',
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
            'AltGr+Shift+key, alternate chaining',
            [(4, True), (4, False)],
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
            'AltGr',
            [(5, True), (5, False)],
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
            KC.N2.code,
            names=(
                'EURO',
                '€',
            ),
            has_modifiers={KC.LSFT.code, KC.ROPT.code},
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
            KC['N2'].code,
            names=(
                'EURO',
                '€',
            ),
            has_modifiers={KC['LSFT'].code, KC['ROPT'].code},
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
            KC.get('N2').code,
            names=(
                'EURO',
                '€',
            ),
            has_modifiers={KC.get('LSFT').code, KC.get('ROPT').code},
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
        key1 = make_key(code=1)
        key2 = make_key(code=1)
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
