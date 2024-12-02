import unittest

from kmk.keys import KC
from kmk.modules.layers import Layers
from tests.keyboard_test import KeyboardTest


class TestHoldTapLayers(unittest.TestCase):
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


class TestLayers(unittest.TestCase):
    def setUp(self):
        self.kb = KeyboardTest(
            [Layers()],
            [
                [
                    KC.N0,
                    KC.DF(2),
                    KC.MO(1),
                    KC.TG(1),
                    KC.TO(2),
                ],
                [KC.N1, KC.DF(0), KC.FD(2), KC.TRNS, KC.TO(1)],
                [KC.N2, KC.DF(0), KC.TO(0)],
            ],
            debug_enabled=False,
        )

    def test_fd_layer(self):
        self.kb.test('', [(3, True), (3, False)], [{}])
        self.assertEqual(self.kb.keyboard.active_layers, [1, 0])
        self.kb.test('', [(2, True), (2, False)], [{}])
        self.assertEqual(self.kb.keyboard.active_layers, [2, 0])
        self.kb.test('', [(2, True), (2, False)], [{}])

    def test_df_layer(self):
        self.kb.test(
            '',
            [(1, True), (0, True)],
            [{KC.N2}],
        )
        self.assertEqual(self.kb.keyboard.active_layers, [2])
        self.kb.test(
            '',
            [(1, False), (0, False)],
            [{}],
        )
        self.assertEqual(self.kb.keyboard.active_layers, [2])
        self.kb.test('', [(1, True), (1, False)], [{}])

    def test_mo_layer(self):
        self.assertEqual(self.kb.keyboard.active_layers, [0])
        self.kb.test(
            '',
            [(2, True), (0, True)],
            [{KC.N1}],
        )
        self.assertEqual(self.kb.keyboard.active_layers, [1, 0])
        self.kb.test(
            '',
            [(2, False), (0, False)],
            [{}],
        )
        self.assertEqual(self.kb.keyboard.active_layers, [0])
        self.kb.test(
            '',
            [(2, True), (4, True)],
            [{}],
        )
        self.assertEqual(self.kb.keyboard.active_layers, [1])
        self.kb.test(
            '',
            [(2, False), (4, False)],
            [{}],
        )
        self.assertEqual(self.kb.keyboard.active_layers, [1])
        self.kb.test('', [(1, True), (1, False)], [{}])

    def test_tg_layer(self):
        self.kb.test(
            '',
            [(3, True), (0, True)],
            [{KC.N1}],
        )
        self.assertEqual(self.kb.keyboard.active_layers, [1, 0])
        self.kb.test(
            '',
            [(3, False), (0, False)],
            [{}],
        )
        self.assertEqual(self.kb.keyboard.active_layers, [1, 0])
        self.kb.test(
            '',
            [(3, True)],
            [{}],
        )
        self.assertEqual(self.kb.keyboard.active_layers, [0])

    def test_to_layer(self):
        self.kb.test(
            '',
            [(4, True), (0, True)],
            [{KC.N2}],
        )
        self.assertEqual(self.kb.keyboard.active_layers, [2])
        self.kb.test(
            '',
            [(4, False), (0, False)],
            [{}],
        )
        self.assertEqual(self.kb.keyboard.active_layers, [2])
        self.kb.test('', [(1, True), (1, False)], [{}])


if __name__ == '__main__':
    unittest.main()
