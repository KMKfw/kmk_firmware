import unittest

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from tests.keyboard_test import KeyboardTest


class TestHoldTap(unittest.TestCase):
    def test_basic_kmk_keyboard(self):
        keyboard = KeyboardTest(
            [Layers(), ModTap()],
            [
                [KC.MT(KC.A, KC.LCTL), KC.LT(1, KC.B), KC.C, KC.D],
                [KC.N1, KC.N2, KC.N3, KC.N4],
            ],
            debug_enabled=False,
        )

        keyboard.test('MT tap behaviour', [(0, True), 100, (0, False)], [{KC.A}, {}])

        keyboard.test(
            'MT hold behaviour', [(0, True), 350, (0, False)], [{KC.LCTL}, {}]
        )

        # TODO test multiple mods being held

        # MT
        keyboard.test(
            'MT within tap time sequential -> tap behavior',
            [(0, True), 100, (0, False), (3, True), (3, False)],
            [{KC.A}, {}, {KC.D}, {}],
        )

        keyboard.test(
            'MT within tap time rolling -> tap behavior',
            [(0, True), 100, (3, True), 250, (0, False), (3, False)],
            [{KC.A}, {KC.A, KC.D}, {KC.D}, {}],
        )

        keyboard.test(
            'MT within tap time nested -> tap behavior',
            [(0, True), 100, (3, True), (3, False), 250, (0, False)],
            [{KC.A}, {KC.A, KC.D}, {KC.A}, {}],
        )

        keyboard.test(
            'MT after tap time sequential -> hold behavior',
            [(0, True), 350, (0, False), (3, True), (3, False)],
            [{KC.LCTL}, {}, {KC.D}, {}],
        )

        keyboard.test(
            'MT after tap time rolling -> hold behavior',
            [(0, True), 350, (3, True), (0, False), (3, False)],
            [{KC.LCTL}, {KC.LCTL, KC.D}, {KC.D}, {}],
        )

        keyboard.test(
            'MT after tap time nested -> hold behavior',
            [(0, True), 350, (3, True), (3, False), (0, False)],
            [{KC.LCTL}, {KC.LCTL, KC.D}, {KC.LCTL}, {}],
        )

        # LT
        keyboard.test(
            'LT within tap time sequential -> tap behavior',
            [(1, True), 100, (1, False), (3, True), (3, False)],
            [{KC.B}, {}, {KC.D}, {}],
        )

        keyboard.test(
            'LT within tap time rolling -> tap behavior',
            [(1, True), 100, (3, True), 250, (1, False), (3, False)],
            [{KC.B}, {KC.B, KC.D}, {KC.D}, {}],
        )

        keyboard.test(
            'LT within tap time nested -> tap behavior',
            [(1, True), 100, (3, True), (3, False), 250, (1, False)],
            [{KC.B}, {KC.B, KC.D}, {KC.B}, {}],
        )

        keyboard.test(
            'LT after tap time sequential -> hold behavior',
            [(1, True), 350, (1, False), (3, True), (3, False)],
            [{KC.D}, {}],
        )

        keyboard.test(
            'LT after tap time rolling -> hold behavior',
            [(1, True), 350, (3, True), (1, False), (3, False)],
            [{KC.N4}, {}],
        )

        keyboard.test(
            'LT after tap time nested -> hold behavior',
            [(1, True), 350, (3, True), (3, False), (1, False)],
            [{KC.N4}, {}],
        )

        # TODO test TT


if __name__ == '__main__':
    unittest.main()
