import unittest

from kmk.keys import KC
from kmk.modules.rapidfire import RapidFire
from tests.keyboard_test import KeyboardTest

t_interval = 4 * KeyboardTest.loop_delay_ms
t_timeout = 10 * KeyboardTest.loop_delay_ms
t_hold = t_timeout + 5 * t_interval + KeyboardTest.loop_delay_ms


class TestKeyRepeat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        KC.clear()

        cls.keyboard = KeyboardTest(
            [RapidFire()],
            [
                [
                    KC.RF(KC.N0, interval=t_interval, timeout=t_timeout),
                    KC.RF(KC.N1, interval=t_interval, timeout=t_timeout, toggle=True),
                ],
            ],
            debug_enabled=False,
        )

    def test_rapidfire(self):
        self.keyboard.test(
            '',
            [(0, True), (0, False)],
            [{KC.N0}, {}],
        )

        self.keyboard.test(
            '',
            [(0, True), t_timeout // 2, (0, False)],
            [{KC.N0}, {}],
        )

        self.keyboard.test(
            '',
            [(0, True), t_timeout + t_interval // 2, (0, False)],
            [{KC.N0}, {}, {KC.N0}, {}],
        )

        self.keyboard.test(
            '',
            [(0, True), t_timeout + (3 * t_interval) // 2, (0, False)],
            [{KC.N0}, {}, {KC.N0}, {}, {KC.N0}, {}],
        )

        self.keyboard.test(
            '',
            [(0, True), t_hold, (0, False)],
            [
                {KC.N0},
                {},
                {KC.N0},
                {},
                {KC.N0},
                {},
                {KC.N0},
                {},
                {KC.N0},
                {},
                {KC.N0},
                {},
            ],
        )

        self.keyboard.test(
            '',
            [
                (1, True),
                t_timeout + t_interval // 2,
                (1, False),
                3 * t_interval,
                (1, True),
                (1, False),
            ],
            [
                {KC.N1},
                {},
                {KC.N1},
                {},
                {KC.N1},
                {},
                {KC.N1},
                {},
                {KC.N1},
                {},
            ],
        )
