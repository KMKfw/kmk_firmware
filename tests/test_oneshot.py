import unittest

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.oneshot import OneShot
from tests.keyboard_test import KeyboardTest


class TestOneshot(unittest.TestCase):
    def test_oneshot(self):
        t_within = 2 * KeyboardTest.loop_delay_ms
        t_after = 7 * KeyboardTest.loop_delay_ms
        timeout = (t_after + t_within) // 2

        # overide default timeouts
        OneShot.tap_time = timeout

        keyboard = KeyboardTest(
            [Layers(), OneShot()],
            [
                [
                    KC.OS(KC.MO(1)),
                    KC.MO(1),
                    KC.C,
                    KC.D,
                    KC.OS(KC.E),
                    KC.OS(KC.F),
                ],
                [KC.N0, KC.N1, KC.N2, KC.N3, KC.OS(KC.LSFT), KC.TRNS],
            ],
            debug_enabled=False,
        )

        keyboard.test(
            'OS timed out',
            [(4, True), (4, False), t_after],
            [{KC.E}, {}],
        )

        keyboard.test(
            'OS interrupt within tap time',
            [(4, True), (4, False), t_within, (3, True), (3, False)],
            [{KC.E}, {KC.D, KC.E}, {KC.E}, {}],
        )

        keyboard.test(
            'OS interrupt, multiple within tap time',
            [(4, True), (4, False), (3, True), (3, False), (2, True), (2, False)],
            [{KC.E}, {KC.D, KC.E}, {KC.E}, {}, {KC.C}, {}],
        )

        keyboard.test(
            'OS interrupt, multiple interleaved',
            [(4, True), (4, False), (3, True), (2, True), (2, False), (3, False)],
            [{KC.E}, {KC.D, KC.E}, {KC.D}, {KC.C, KC.D}, {KC.D}, {}],
        )

        keyboard.test(
            'OS interrupt, multiple interleaved',
            [(4, True), (4, False), (3, True), (2, True), (3, False), (2, False)],
            [{KC.E}, {KC.D, KC.E}, {KC.D}, {KC.C, KC.D}, {KC.C}, {}],
        )

        keyboard.test(
            'OS interrupt within tap time, hold',
            [(4, True), (3, True), (4, False), t_after, (3, False)],
            [{KC.E}, {KC.D, KC.E}, {KC.D}, {}],
        )

        keyboard.test(
            'OS interrupt within tap time, hold',
            [(4, True), (4, False), (3, True), t_after, (3, False)],
            [{KC.E}, {KC.D, KC.E}, {KC.E}, {}],
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

        keyboard.test(
            'OS stacking within timeout reset',
            [
                (4, True),
                (4, False),
                t_within,
                (5, True),
                (5, False),
                t_within,
                (3, True),
                (3, False),
            ],
            [{KC.E}, {KC.E, KC.F}, {KC.E, KC.F, KC.D}, {KC.E, KC.F}, {KC.E}, {}],
        )

        keyboard.test(
            'OS stacking timed out',
            [
                (4, True),
                (4, False),
                (5, True),
                (5, False),
                t_after,
                (3, True),
                (3, False),
            ],
            [{KC.E}, {KC.E, KC.F}, {KC.E}, {}, {KC.D}, {}],
        )

        keyboard.test(
            'OS stacking with OS-layer',
            [
                (0, True),
                (0, False),
                (4, True),
                (4, False),
                (1, True),
                (1, False),
            ],
            [{KC.LSFT}, {KC.LSFT, KC.N1}, {KC.LSFT}, {}],
        )

        keyboard.test(
            'OS stacking with layer change',
            [
                (1, True),
                (4, True),
                (4, False),
                (1, False),
                (4, True),
                (4, False),
                (2, True),
                (2, False),
            ],
            [
                {KC.LSFT},
                {KC.LSFT, KC.E},
                {KC.LSFT, KC.E, KC.C},
                {KC.LSFT, KC.E},
                {KC.LSFT},
                {},
            ],
        )
