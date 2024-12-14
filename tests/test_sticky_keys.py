import unittest

from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.sticky_keys import StickyKeys
from kmk.modules.tapdance import TapDance
from tests.keyboard_test import KeyboardTest

t_within = 2 * KeyboardTest.loop_delay_ms
t_holdtap = 4 * KeyboardTest.loop_delay_ms
t_sticky = 6 * KeyboardTest.loop_delay_ms
t_after = 11 * KeyboardTest.loop_delay_ms


class TestStickyKey(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        KC.clear()
        sticky_keys = StickyKeys(release_after=t_sticky)

        tapdance = TapDance()
        tapdance.tap_time = t_holdtap

        holdtap = HoldTap()
        holdtap.tap_time = t_holdtap

        cls.keyboard = KeyboardTest(
            [Layers(), holdtap, tapdance, sticky_keys],
            [
                [
                    KC.SK(KC.N0),
                    KC.SK(KC.N1),
                    KC.N2,
                    KC.N3,
                ],
                [
                    KC.SK(KC.MO(4)),
                    KC.MO(4),
                    KC.N2,
                    KC.SK(KC.N3),
                ],
                [
                    KC.SK(KC.N0, defer_release=True),
                    KC.SK(KC.N1, defer_release=True, retap_cancel=False),
                    KC.N2,
                    KC.N3,
                ],
                [
                    KC.TD(
                        KC.SK(KC.N0),
                        KC.SK(KC.A),
                    ),
                    KC.HT(KC.X, KC.Y),
                    KC.N2,
                    KC.N3,
                ],
                [
                    KC.SK(KC.A),
                    KC.B,
                    KC.C,
                    KC.D,
                ],
                [
                    KC.SK(KC.N0, retap_cancel=True),
                    KC.SK(KC.N1, retap_cancel=False),
                    KC.N2,
                    KC.N3,
                ],
            ],
            debug_enabled=False,
        )

    def test_sticky_key(self):
        self.keyboard.keyboard.active_layers = [0]
        keyboard = self.keyboard

        keyboard.test(
            'no stick, release after timeout',
            [(0, True), (0, False), t_after, (2, True), (2, False)],
            [{KC.N0}, {}, {KC.N2}, {}],
        )

        keyboard.test(
            'hold',
            [(0, True), t_after, (0, False)],
            [{KC.N0}, {}],
        )

        keyboard.test(
            'stick within timeout',
            [(0, True), (0, False), t_within, (2, True), (2, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N0}, {}],
        )

        keyboard.test(
            'stick, release other after timeout',
            [(0, True), (0, False), (2, True), t_after, (2, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N0}, {}],
        )

        keyboard.test(
            'stick, multiple consecutive other',
            [(0, True), (0, False), (2, True), (2, False), (3, True), (3, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N0}, {}, {KC.N3}, {}],
        )

        keyboard.test(
            'stick, multiple nested other',
            [(0, True), (0, False), (2, True), (3, True), (3, False), (2, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N2}, {KC.N2, KC.N3}, {KC.N2}, {}],
        )

        keyboard.test(
            'stick, multiple interleaved other',
            [(0, True), (0, False), (2, True), (3, True), (2, False), (3, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N2}, {KC.N2, KC.N3}, {KC.N3}, {}],
        )

        keyboard.test(
            'stick w prev active, release prev after SK',
            [(3, True), (0, True), (0, False), (3, False), (2, True), (2, False)],
            [{KC.N3}, {KC.N0, KC.N3}, {KC.N0}, {KC.N0, KC.N2}, {KC.N0}, {}],
        )

        keyboard.test(
            'stick w prev active, release prev during SK',
            [(3, True), (0, True), (3, False), (0, False), (2, True), (2, False)],
            [{KC.N3}, {KC.N0, KC.N3}, {KC.N0}, {KC.N0, KC.N2}, {KC.N0}, {}],
        )

        keyboard.test(
            'stick w prev active, release prev after other press',
            [(3, True), (0, True), (0, False), (2, True), (3, False), (2, False)],
            [
                {KC.N3},
                {KC.N0, KC.N3},
                {KC.N0, KC.N2, KC.N3},
                {KC.N0, KC.N2},
                {KC.N2},
                {},
            ],
        )

        keyboard.test(
            'hold after timeout, nested other',
            [(0, True), t_after, (2, True), (2, False), (0, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N0}, {}],
        )

        keyboard.test(
            'hold after timeout, interleaved other',
            [(0, True), t_after, (2, True), (0, False), (2, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N2}, {}],
        )

        keyboard.test(
            'hold within timeout, interleaved other',
            [(0, True), (2, True), (0, False), t_after, (2, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N2}, {}],
        )

        keyboard.test(
            'hold within timeout, nested other',
            [(0, True), (2, True), (2, False), t_after, (0, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N0}, {}],
        )

        keyboard.test(
            'hold with multiple interrupt keys',
            [(0, True), (2, True), (2, False), (3, True), (3, False), (0, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N0}, {KC.N0, KC.N3}, {KC.N0}, {}],
        )

        keyboard.test(
            'hold multiple, tap interrupt, release one held, tap interrupt',
            [
                (0, True),
                (1, True),
                (2, True),
                (2, False),
                (1, False),
                (3, True),
                (3, False),
                (0, False),
            ],
            [
                {KC.N0},
                {KC.N0, KC.N1},
                {KC.N0, KC.N1, KC.N2},
                {KC.N0, KC.N1},
                {KC.N0},
                {KC.N0, KC.N3},
                {KC.N0},
                {},
            ],
        )

    def test_sticky_key_stack(self):
        self.keyboard.keyboard.active_layers = [0]
        keyboard = self.keyboard

        keyboard.test(
            'no stack after timeout',
            [
                (0, True),
                (0, False),
                t_after,
                (1, True),
                (1, False),
            ],
            [{KC.N0}, {}, {KC.N1}, {}],
        )

        keyboard.test(
            'stack release after timeout',
            [(0, True), (0, False), t_within, (1, True), (1, False)],
            [{KC.N0}, {KC.N0, KC.N1}, {KC.N0}, {}],
        )

        keyboard.test(
            'stack within timeout, reset first SK',
            [
                (0, True),
                (0, False),
                t_within,
                (1, True),
                (1, False),
                t_within,
                (2, True),
                (2, False),
            ],
            [
                {KC.N0},
                {KC.N0, KC.N1},
                {KC.N0, KC.N1, KC.N2},
                {KC.N0, KC.N1},
                {KC.N0},
                {},
            ],
        )

        keyboard.test(
            'stack, after timeout',
            [
                (0, True),
                (0, False),
                (1, True),
                (1, False),
                t_after,
                (2, True),
                (2, False),
            ],
            [{KC.N0}, {KC.N0, KC.N1}, {KC.N0}, {}, {KC.N2}, {}],
        )

        keyboard.test(
            'stack and roll',
            [
                (0, True),
                (0, False),
                (1, True),
                (1, False),
                (2, True),
                (3, True),
                (2, False),
                (3, False),
            ],
            [
                {KC.N0},
                {KC.N0, KC.N1},
                {KC.N0, KC.N1, KC.N2},
                {KC.N0, KC.N2},
                {KC.N2},
                {KC.N2, KC.N3},
                {KC.N3},
                {},
            ],
        )

    def test_sticky_layer(self):
        keyboard = self.keyboard
        self.keyboard.keyboard.active_layers = [1]

        keyboard.test(
            'sticky layer',
            [(0, True), (0, False), (1, True), (1, False), (2, True), (2, False)],
            [{KC.B}, {}, {KC.N2}, {}],
        )

        keyboard.test(
            'hold layer',
            [(0, True), (1, True), (1, False), (0, False), (2, True), (2, False)],
            [{KC.B}, {}, {KC.N2}, {}],
        )

        keyboard.test(
            'stick from other layer',
            [(1, True), (0, True), (0, False), (1, False), (2, True), (2, False)],
            [{KC.A}, {KC.A, KC.N2}, {KC.A}, {}],
        )

        keyboard.test(
            'stack with SK on other layer',
            [(0, True), (0, False), (0, True), (0, False), (1, True), (1, False)],
            [{KC.A}, {KC.A, KC.B}, {KC.A}, {}],
        )

        keyboard.test(
            'stack with layer change',
            [
                (1, True),
                (0, True),
                (0, False),
                (1, False),
                (3, True),
                (3, False),
                (2, True),
                (2, False),
            ],
            [
                {KC.A},
                {KC.A, KC.N3},
                {KC.A, KC.N2, KC.N3},
                {KC.A, KC.N3},
                {KC.A},
                {},
            ],
        )

    def test_sticky_key_deferred(self):
        self.keyboard.keyboard.active_layers = [2]
        keyboard = self.keyboard

        keyboard.test(
            'release after timeout',
            [(0, True), (0, False), t_after],
            [{KC.N0}, {}],
        )

        keyboard.test(
            'stick within timeout',
            [(0, True), (0, False), (2, True), (2, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N0}, {}],
        )

        keyboard.test(
            'hold, release interleaved',
            [(0, True), (2, True), (0, False), (2, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N2}, {}],
        )

        keyboard.test(
            'stick, multiple consecutive other',
            [(0, True), (0, False), (2, True), (2, False), (3, True), (3, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N0}, {}, {KC.N3}, {}],
        )

        keyboard.test(
            'stick, multiple nested other',
            [(0, True), (0, False), (2, True), (3, True), (3, False), (2, False)],
            [
                {KC.N0},
                {KC.N0, KC.N2},
                {KC.N0, KC.N2, KC.N3},
                {KC.N0, KC.N2},
                {KC.N0},
                {},
            ],
        )

        keyboard.test(
            'stick, multiple interleaved other',
            [(0, True), (0, False), (2, True), (3, True), (2, False), (3, False)],
            [
                {KC.N0},
                {KC.N0, KC.N2},
                {KC.N0, KC.N2, KC.N3},
                {KC.N0, KC.N3},
                {KC.N0},
                {},
            ],
        )

        keyboard.test(
            'stick, multiple interleaved other after timeout',
            [
                (0, True),
                (0, False),
                (2, True),
                t_after,
                (3, True),
                (2, False),
                (3, False),
            ],
            [
                {KC.N0},
                {KC.N0, KC.N2},
                {KC.N0, KC.N2, KC.N3},
                {KC.N0, KC.N3},
                {KC.N0},
                {},
            ],
        )

        keyboard.test(
            'stick stack, multiple interleaved other',
            [
                (0, True),
                (0, False),
                (1, True),
                (1, False),
                (2, True),
                (3, True),
                (2, False),
                (3, False),
            ],
            [
                {KC.N0},
                {KC.N0, KC.N1},
                {KC.N0, KC.N1, KC.N2},
                {KC.N0, KC.N1, KC.N2, KC.N3},
                {KC.N0, KC.N1, KC.N3},
                {KC.N0, KC.N1},
                {KC.N0},
                {},
            ],
        )

        keyboard.test(
            'hold stack, interleave hold release',
            [
                (0, True),
                (0, False),
                (1, True),
                (2, True),
                (3, True),
                (1, False),
                (2, False),
                (3, False),
            ],
            [
                {KC.N0},
                {KC.N0, KC.N1},
                {KC.N0, KC.N1, KC.N2},
                {KC.N0, KC.N1, KC.N2, KC.N3},
                {KC.N0, KC.N2, KC.N3},
                {KC.N0, KC.N3},
                {KC.N0},
                {},
            ],
        )

        keyboard.test(
            'stick stack, retap_cancel, multiple interleaved other',
            [
                (0, True),
                (0, False),
                (1, True),
                (1, False),
                (0, True),
                (0, False),
                (2, True),
                (3, True),
                (2, False),
                (3, False),
            ],
            [
                {KC.N0},
                {KC.N0, KC.N1},
                {KC.N1},
                {KC.N1, KC.N2},
                {KC.N1, KC.N2, KC.N3},
                {KC.N1, KC.N3},
                {KC.N1},
                {},
            ],
        )

        keyboard.test(
            'stick stack, retap_cancel, multiple interleaved other',
            [
                (0, True),
                (0, False),
                (1, True),
                (1, False),
                (2, True),
                (3, True),
                (0, True),
                (0, False),
                (2, False),
                (3, False),
            ],
            [
                {KC.N0},
                {KC.N0, KC.N1},
                {KC.N0, KC.N1, KC.N2},
                {KC.N0, KC.N1, KC.N2, KC.N3},
                {KC.N1, KC.N2, KC.N3},
                {KC.N1, KC.N3},
                {KC.N1},
                {},
            ],
        )

        keyboard.test(
            'hold multiple, tap interrupt, release one held, tap interrupt',
            [
                (0, True),
                (1, True),
                (2, True),
                (2, False),
                (1, False),
                (3, True),
                (3, False),
                (0, False),
            ],
            [
                {KC.N0},
                {KC.N0, KC.N1},
                {KC.N0, KC.N1, KC.N2},
                {KC.N0, KC.N1},
                {KC.N0},
                {KC.N0, KC.N3},
                {KC.N0},
                {},
            ],
        )

    def test_sticky_key_in_tapdance(self):
        self.keyboard.keyboard.active_layers = [3]
        keyboard = self.keyboard

        keyboard.test(
            'tap 1x, no stick',
            [(0, True), (0, False), t_after, (2, True), (2, False)],
            [{KC.N0}, {}, {KC.N2}, {}],
        )

        keyboard.test(
            'tap 1x, stick',
            [(0, True), (0, False), t_within, (2, True), (2, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N0}, {}],
        )

        keyboard.test(
            'hold 1x, stick',
            [(0, True), t_holdtap, (0, False), (2, True), (2, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N0}, {}],
        )

        keyboard.test(
            'hold 1x after timeout',
            [(0, True), t_after, (0, False), (2, True), (2, False)],
            [{KC.N0}, {}, {KC.N2}, {}],
        )

        keyboard.test(
            'hold 1x, interleaved',
            [(0, True), (2, True), (0, False), (2, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N2}, {}],
        )

        keyboard.test(
            'tap 2x, stick',
            [(0, True), (0, False), (0, True), (0, False), (2, True), (2, False)],
            [{KC.A}, {KC.A, KC.N2}, {KC.A}, {}],
        )

        keyboard.test(
            'stick stack from same tapdance',
            [
                (0, True),
                (0, False),
                t_holdtap,
                (0, True),
                (0, False),
                (0, True),
                (0, False),
                (2, True),
                (2, False),
            ],
            [{KC.N0}, {KC.N0, KC.A}, {KC.N0, KC.A, KC.N2}, {KC.N0, KC.A}, {KC.N0}, {}],
        )

    def test_sticky_key_retap_cancel(self):
        self.keyboard.keyboard.active_layers = [5]
        keyboard = self.keyboard

        keyboard.test(
            'retap_cancel',
            [(0, True), (0, False), (0, True), (0, False), (2, True), (2, False)],
            [{KC.N0}, {}, {KC.N2}, {}],
        )

        keyboard.test(
            'no retap_cancel',
            [(1, True), (1, False), (1, True), (1, False), (2, True), (2, False)],
            [{KC.N1}, {KC.N1, KC.N2}, {KC.N1}, {}],
        )

        keyboard.test(
            'stack, retap_cancel renew timeout',
            [
                (0, True),
                (0, False),
                (1, True),
                (1, False),
                t_holdtap,
                (0, True),
                (0, False),
                t_holdtap,
                (2, True),
                (2, False),
            ],
            [{KC.N0}, {KC.N0, KC.N1}, {KC.N1}, {KC.N1, KC.N2}, {KC.N1}, {}],
        )

        keyboard.test(
            'stick, interleaved retap_cancel',
            [(0, True), (0, False), (2, True), (0, True), (0, False), (2, False)],
            [{KC.N0}, {KC.N0, KC.N2}, {KC.N2}, {}],
        )

    def test_sticky_key_w_holdtap(self):
        self.keyboard.keyboard.active_layers = [3]
        keyboard = self.keyboard

        keyboard.test(
            'stick, tap',
            [(0, True), (0, False), (1, True), (1, False)],
            [{KC.N0}, {KC.N0, KC.X}, {KC.N0}, {}],
        )

        keyboard.test(
            'stick, hold',
            [(0, True), (0, False), (1, True), t_after, (1, False)],
            [{KC.N0}, {KC.N0, KC.Y}, {KC.N0}, {}],
        )
