import unittest

from kmk.keys import KC
from kmk.modules.oneshot import OneShot
from tests.keyboard_test import KeyboardTest


class TestHoldTap(unittest.TestCase):
    def test_oneshot(self):
        keyboard = KeyboardTest(
            [OneShot()],
            [
                [
                    KC.A,
                    KC.B,
                    KC.C,
                    KC.D,
                    KC.OS(KC.E, tap_time=50),
                    KC.OS(KC.F, tap_time=50),
                ],
                [KC.N0, KC.N1, KC.N2, KC.N3, KC.N4],
            ],
            debug_enabled=False,
        )
        t_within = 40
        t_after = 60

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
