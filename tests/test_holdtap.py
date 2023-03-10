import unittest

from kmk.keys import KC
from kmk.modules.holdtap import HoldTap, HoldTapRepeat
from kmk.modules.layers import Layers
from tests.keyboard_test import KeyboardTest


class TestHoldTap(unittest.TestCase):
    def setUp(self):
        KC.clear()

        self.t_within = 2 * KeyboardTest.loop_delay_ms
        self.t_after = 5 * KeyboardTest.loop_delay_ms
        tap_time = (self.t_after + self.t_within) // 2

        # overide default timeouts
        HoldTap.tap_time = tap_time

    def test_holdtap(self):
        t_within = self.t_within
        t_after = self.t_after

        keyboard = KeyboardTest(
            [Layers(), HoldTap()],
            [
                [
                    KC.HT(KC.A, KC.LCTL),
                    KC.LT(1, KC.B),
                    KC.C,
                    KC.D,
                ],
                [KC.N1, KC.N2, KC.N3, KC.N4],
            ],
            debug_enabled=False,
        )

        keyboard.test(
            'HT tap behaviour', [(0, True), t_within, (0, False)], [{KC.A}, {}]
        )

        keyboard.test(
            'HT hold behaviour', [(0, True), t_after, (0, False)], [{KC.LCTL}, {}]
        )

        # TODO test multiple mods being held

        # HT
        keyboard.test(
            'HT within tap time sequential -> tap behavior',
            [(0, True), t_within, (0, False), (3, True), (3, False)],
            [{KC.A}, {}, {KC.D}, {}],
        )

        keyboard.test(
            'HT within tap time rolling -> hold behavior',
            [(0, True), t_within, (3, True), t_after, (0, False), (3, False)],
            [{KC.LCTL}, {KC.LCTL, KC.D}, {KC.D}, {}],
        )

        keyboard.test(
            'HT within tap time nested -> hold behavior',
            [(0, True), t_within, (3, True), (3, False), t_after, (0, False)],
            [{KC.LCTL}, {KC.LCTL, KC.D}, {KC.LCTL}, {}],
        )

        keyboard.test(
            'HT after tap time sequential -> hold behavior',
            [(0, True), t_after, (0, False), (3, True), (3, False)],
            [{KC.LCTL}, {}, {KC.D}, {}],
        )

        keyboard.test(
            'HT after tap time rolling -> hold behavior',
            [(0, True), t_after, (3, True), (0, False), (3, False)],
            [{KC.LCTL}, {KC.LCTL, KC.D}, {KC.D}, {}],
        )

        keyboard.test(
            'HT after tap time nested -> hold behavior',
            [(0, True), t_after, (3, True), (3, False), (0, False)],
            [{KC.LCTL}, {KC.LCTL, KC.D}, {KC.LCTL}, {}],
        )

        # LT
        keyboard.test(
            'LT within tap time sequential -> tap behavior',
            [(1, True), t_within, (1, False), (3, True), (3, False)],
            [{KC.B}, {}, {KC.D}, {}],
        )

        keyboard.test(
            'LT within tap time rolling -> tap behavior',
            [(1, True), t_within, (3, True), t_after, (1, False), (3, False)],
            [{KC.B}, {KC.B, KC.D}, {KC.D}, {}],
        )

        keyboard.test(
            'LT within tap time nested -> tap behavior',
            [(1, True), t_within, (3, True), (3, False), t_after, (1, False)],
            [{KC.B}, {KC.B, KC.D}, {KC.B}, {}],
        )

        keyboard.test(
            'LT after tap time sequential -> hold behavior',
            [(1, True), t_after, (1, False), (3, True), (3, False)],
            [{KC.D}, {}],
        )

        keyboard.test(
            'LT after tap time rolling -> hold behavior',
            [(1, True), t_after, (3, True), (1, False), (3, False)],
            [{KC.N4}, {}],
        )

        keyboard.test(
            'LT after tap time nested -> hold behavior',
            [(1, True), t_after, (3, True), (3, False), (1, False)],
            [{KC.N4}, {}],
        )

        keyboard.test(
            'LT after tap time nested -> hold behavior',
            [
                (0, True),
                t_after,
                (1, True),
                t_after,
                (3, True),
                (3, False),
                (1, False),
                (0, False),
            ],
            [{KC.LCTL}, {KC.LCTL, KC.N4}, {KC.LCTL}, {}],
        )

    def test_holdtap_chain(self):
        t_after = self.t_after

        keyboard = KeyboardTest(
            [HoldTap()],
            [
                [
                    KC.N0,
                    KC.HT(KC.N1, KC.LCTL),
                    KC.HT(KC.N2, KC.LSFT, tap_interrupted=True),
                    KC.HT(
                        KC.N3,
                        KC.LALT,
                        prefer_hold=False,
                        tap_interrupted=True,
                    ),
                ],
            ],
            debug_enabled=False,
        )

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
            [
                {KC.LCTL},
                {KC.LCTL, KC.N3},
                {KC.LCTL, KC.N0, KC.N3},
                {KC.LCTL, KC.N0},
                {KC.N0},
                {},
            ],
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
                {KC.LALT},
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

    def test_holdtap_repeat(self):
        t_within = self.t_within
        t_after = self.t_after

        keyboard = KeyboardTest(
            [HoldTap()],
            [
                [
                    KC.HT(KC.A, KC.B, repeat=HoldTapRepeat.ALL),
                    KC.HT(KC.A, KC.B, repeat=HoldTapRepeat.TAP),
                    KC.HT(KC.A, KC.B, repeat=HoldTapRepeat.HOLD),
                ]
            ],
            debug_enabled=False,
        )

        keyboard.test(
            'repeat tap',
            [
                (0, True),
                (0, False),
                t_within,
                (0, True),
                t_after,
                (0, False),
                (0, True),
                (0, False),
                t_after,
            ],
            [{KC.A}, {}, {KC.A}, {}, {KC.A}, {}],
        )

        keyboard.test(
            'repeat hold',
            [
                (0, True),
                t_after,
                (0, False),
                t_within,
                (0, True),
                (0, False),
                (0, True),
                (0, False),
                t_after,
            ],
            [{KC.B}, {}, {KC.B}, {}, {KC.B}, {}],
        )

        keyboard.test(
            'no repeat after tap_time',
            [
                (0, True),
                (0, False),
                t_after,
                (0, True),
                t_after,
                (0, False),
                t_after,
                (0, True),
                (0, False),
                t_after,
            ],
            [{KC.A}, {}, {KC.B}, {}, {KC.A}, {}],
        )

        keyboard.test(
            'tap repeat / no hold repeat ',
            [(1, True), t_after, (1, False), (1, True), (1, False)],
            [{KC.B}, {}, {KC.A}, {}],
        )

        keyboard.test(
            'hold repeat / no tap repeat ',
            [(2, True), (2, False), (2, True), t_after, (2, False)],
            [{KC.A}, {}, {KC.B}, {}],
        )
