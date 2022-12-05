import unittest

from kmk.keys import KC
from kmk.modules.layers import Layers
from tests.keyboard_test import KeyboardTest


class TestLayers(unittest.TestCase):
    def setUp(self):
        KC.clear()
        self.kb = KeyboardTest(
            [Layers()],
            [
                [KC.N0, KC.LM(1, KC.LCTL)],
                [KC.A, KC.B],
            ],
            debug_enabled=False,
        )

    def test_layermod(self):
        self.kb.test(
            'Layer + Mod',
            [(1, True), (0, True), (1, False), (0, False)],
            [{KC.LCTL}, {KC.LCTL, KC.A}, {KC.A}, {}],
        )


if __name__ == '__main__':
    unittest.main()
