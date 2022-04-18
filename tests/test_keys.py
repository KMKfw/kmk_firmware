import unittest

from kmk.keys import KC, make_key


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
        with self.assertRaises(ValueError):
            KC.INVALID_KEY

    def test_invalid_key_lower(self):
        with self.assertRaises(ValueError):
            KC.invalid_key


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
        with self.assertRaises(ValueError):
            KC['NOT_A_VALID_KEY']

    def test_invalid_key_lower(self):
        with self.assertRaises(ValueError):
            KC['not_a_valid_key']

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
        assert None == KC.get('INVALID_KEY')

    def test_invalid_key_lower(self):
        assert None == KC.get('not_a_valid_key')

# Some of these test appear silly, but they're testing we get the
# same, single, instance back when requested through KC and that
# order of request doesn't matter
class TestKeys(unittest.TestCase):
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