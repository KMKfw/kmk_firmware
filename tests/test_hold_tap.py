import unittest

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.modules.oneshot import OneShot
from tests.keyboard_test import KeyboardTest


class TestHoldTap(unittest.TestCase):
    def test_holdtap(self):
        keyboard = KeyboardTest(
            [Layers(), ModTap(), OneShot()],
            [
                [KC.MT(KC.A, KC.LCTL), KC.LT(1, KC.B), KC.C, KC.D, KC.OS(KC.E)],
                [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5],
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
            'MT within tap time rolling -> hold behavior',
            [(0, True), 100, (3, True), 250, (0, False), (3, False)],
            [{KC.LCTL}, {KC.LCTL, KC.D}, {KC.D}, {}],
        )

        keyboard.test(
            'MT within tap time nested -> hold behavior',
            [(0, True), 100, (3, True), (3, False), 250, (0, False)],
            [{KC.LCTL}, {KC.LCTL, KC.D}, {KC.LCTL}, {}],
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

        keyboard.test(
            'LT after tap time nested -> hold behavior',
            [
                (0, True),
                350,
                (1, True),
                350,
                (3, True),
                (3, False),
                (1, False),
                (0, False),
            ],
            [{KC.LCTL}, {KC.LCTL, KC.N4}, {KC.LCTL}, {}],
        )

    def test_holdtap_chain(self):
        keyboard = KeyboardTest(
            [ModTap()],
            [
                [
                    KC.N0,
                    KC.MT(KC.N1, KC.LCTL, tap_time=50),
                    KC.MT(KC.N2, KC.LSFT, tap_interrupted=True, tap_time=50),
                    KC.MT(
                        KC.N3,
                        KC.LALT,
                        prefer_hold=False,
                        tap_interrupted=True,
                        tap_time=50,
                    ),
                ],
            ],
            debug_enabled=False,
        )
        # t_within = 40
        t_after = 60

        keyboard.test(
            'chained 0',
            [(1, True), (2, True), (0, True), (0, False), (2, False), (1, False)],
            [
                {KC.LCTL},
                {KC.LCTL, KC.LSFT},
                {KC.LCTL, KC.LSFT, KC.N0},
                {KC.LCTL, KC.LSFT},
                {KC.LCTL},
                {},
            ],
        )

        keyboard.test(
            'chained 1',
            [(2, True), (1, True), (0, True), (0, False), (1, False), (2, False)],
            [
                {KC.LCTL},
                {KC.LCTL, KC.LSFT},
                {KC.LCTL, KC.LSFT, KC.N0},
                {KC.LCTL, KC.LSFT},
                {KC.LSFT},
                {},
            ],
        )

        keyboard.test(
            'chained 2',
            [(1, True), (2, True), (0, True), (1, False), (2, False), (0, False)],
            [
                {KC.LCTL},
                {KC.LCTL, KC.LSFT},
                {KC.LCTL, KC.LSFT, KC.N0},
                {KC.LSFT, KC.N0},
                {KC.N0},
                {},
            ],
        )

        keyboard.test(
            'chained 3',
            [(1, True), (3, True), (0, True), (0, False), (1, False), (3, False)],
            [
                {KC.LCTL},
                {KC.LCTL, KC.N3},
                {KC.LCTL, KC.N3, KC.N0},
                {KC.LCTL, KC.N3},
                {KC.N3},
                {},
            ],
        )

        keyboard.test(
            'chained 4',
            [(1, True), (3, True), (0, True), (3, False), (1, False), (0, False)],
            [{KC.LCTL}, {KC.LCTL, KC.N3, KC.N0}, {KC.LCTL, KC.N0}, {KC.N0}, {}],
        )

        keyboard.test(
            'chained 5',
            [(3, True), (1, True), (0, True), (0, False), (1, False), (3, False)],
            [
                {KC.LCTL},
                {KC.LCTL, KC.N3},
                {KC.LCTL, KC.N3, KC.N0},
                {KC.LCTL, KC.N3},
                {KC.N3},
                {},
            ],
        )

        keyboard.test(
            'chained 6',
            [
                (3, True),
                (1, True),
                t_after,
                (0, True),
                (0, False),
                (1, False),
                (3, False),
            ],
            [
                {KC.LCTL, KC.LALT},
                {KC.LCTL, KC.LALT, KC.N0},
                {KC.LCTL, KC.LALT},
                {KC.LALT},
                {},
            ],
        )

        keyboard.test(
            'chained 7',
            [
                (1, True),
                (3, True),
                t_after,
                (0, True),
                (0, False),
                (1, False),
                (3, False),
            ],
            [
                {KC.LCTL},
                {KC.LCTL, KC.LALT},
                {KC.LCTL, KC.LALT, KC.N0},
                {KC.LCTL, KC.LALT},
                {KC.LALT},
                {},
            ],
        )

        keyboard.test(
            'chained 8',
            [(2, True), (3, True), (0, True), (0, False), (2, False), (3, False)],
            [
                {KC.LSFT},
                {KC.LSFT, KC.N3},
                {KC.LSFT, KC.N3, KC.N0},
                {KC.LSFT, KC.N3},
                {KC.N3},
                {},
            ],
        )

        # TODO test TT

    def test_oneshot(self):
        keyboard = KeyboardTest(
            [Layers(), ModTap(), OneShot()],
            [
                [
                    KC.MT(KC.A, KC.LCTL),
                    KC.LT(1, KC.B),
                    KC.C,
                    KC.D,
                    KC.OS(KC.E, tap_time=50),
                ],
                [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5],
            ],
            debug_enabled=False,
        )
        t_within = 40
        t_after = 60

        # OS
        keyboard.test(
            'OS timed out',
            [(4, True), (4, False), t_after],
            [{KC.E}, {}],
        )

        keyboard.test(
            'OS interrupt within tap time',
            [(4, True), (4, False), t_within, (3, True), (3, False)],
            [{KC.E}, {KC.D, KC.E}, {}],
        )

        keyboard.test(
            'OS interrupt, multiple within tap time',
            [(4, True), (4, False), (3, True), (3, False), (2, True), (2, False)],
            [{KC.E}, {KC.D, KC.E}, {}, {KC.C}, {}],
        )

        keyboard.test(
            'OS interrupt, multiple interleaved',
            [(4, True), (4, False), (3, True), (2, True), (2, False), (3, False)],
            [{KC.E}, {KC.D, KC.E}, {KC.C, KC.D}, {KC.D}, {}],
        )

        keyboard.test(
            'OS interrupt, multiple interleaved',
            [(4, True), (4, False), (3, True), (2, True), (3, False), (2, False)],
            [{KC.E}, {KC.D, KC.E}, {KC.C, KC.D}, {KC.C}, {}],
        )

        keyboard.test(
            'OS interrupt within tap time, hold',
            [(4, True), (3, True), (4, False), t_after, (3, False)],
            [{KC.E}, {KC.D, KC.E}, {KC.D}, {}],
        )

        keyboard.test(
            'OS hold with multiple interrupt keys',
            [
                (4, True),
                t_within,
                (3, True),
                (3, False),
                (2, True),
                (2, False),
                (4, False),
            ],
            [{KC.E}, {KC.D, KC.E}, {KC.E}, {KC.C, KC.E}, {KC.E}, {}],
        )


if __name__ == '__main__':
    unittest.main()
