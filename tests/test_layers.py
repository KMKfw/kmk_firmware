import unittest

from kmk.keys import KC
from kmk.modules.layers import Layers
from tests.keyboard_test import KeyboardTest


class TestLayers(unittest.TestCase):
    def setUp(self):
        self.kb = KeyboardTest(
            [Layers()],
            [
                [
                    KC.N0,
                    KC.LM(1, KC.LCTL),
                    KC.LT(1, KC.N2, tap_interrupted=True, prefer_hold=True),
                    KC.LT(1, KC.N3, tap_interrupted=False, prefer_hold=True),
                ],
                [KC.A, KC.B, KC.C, KC.D],
            ],
            debug_enabled=False,
        )

    def test_layermod(self):
        self.kb.test(
            'Layer + Mod',
            [(1, True), (0, True), (1, False), (0, False)],
            [{KC.LCTL}, {KC.LCTL, KC.A}, {KC.A}, {}],
        )

    def test_layertap(self):
        self.kb.test(
            'Layertap roll',
            [(2, True), (0, True), (2, False), (0, False)],
            [{KC.N2}, {KC.N0, KC.N2}, {KC.N0}, {}],
        )

        self.kb.test(
            'Layertap tap interrupted',
            [(2, True), (0, True), 200, (0, False), (2, False)],
            [{KC.A}, {}],
        )

        self.kb.test(
            'Layertap tap interrupted by holdtap',
            [(3, True), (2, True), (2, False), (3, False)],
            [{KC.C}, {}],
        )


if __name__ == '__main__':
    unittest.main()
