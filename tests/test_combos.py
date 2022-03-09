import unittest

from kmk.keys import KC
from kmk.modules.combos import Chord, Combos, Sequence
from tests.keyboard_test import KeyboardTest


class TestCombo(unittest.TestCase):
    def test_basic_kmk_keyboard(self):
        combos = Combos()
        combos.combos = [
            Chord((KC.A, KC.B, KC.C), KC.Y),
            Chord((KC.A, KC.B), KC.X),
            Chord((KC.C, KC.D), KC.Z, timeout=80),
            Sequence((KC.N1, KC.N2, KC.N3), KC.Y, timeout=50),
            Sequence((KC.N1, KC.N2), KC.X, timeout=50),
            Sequence((KC.N3, KC.N4), KC.Z, timeout=100),
            Sequence((KC.N1, KC.N1, KC.N1), KC.W, timeout=50),
            Sequence((KC.LEADER, KC.N1), KC.V, timeout=50),
        ]
        keyboard = KeyboardTest(
            [combos],
            [
                [KC.A, KC.B, KC.C, KC.D, KC.E, KC.F],
                [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.LEADER],
            ],
            debug_enabled=False,
        )

        t_within = 40
        t_after = 60

        # test combos
        keyboard.test(
            'match: 2 combo, within timeout',
            [(0, True), t_within, (1, True), (0, False), (1, False), t_after],
            [{KC.X}, {}],
        )

        keyboard.test(
            'match: 3 combo, within timout, shuffled',
            [
                (0, True),
                (2, True),
                (1, True),
                t_within,
                (1, False),
                (0, False),
                (2, False),
                t_after,
            ],
            [{KC.Y}, {}],
        )

        keyboard.test(
            'match: 2 combo + overlap, after timeout',
            [
                (0, True),
                (1, True),
                (0, False),
                (1, False),
                t_after,
                (2, True),
                (2, False),
                2 * t_after,
            ],
            [{KC.X}, {}, {KC.C}, {}],
        )

        keyboard.test(
            'match: 2 combo + overlap, interleaved, after timeout',
            [
                (0, True),
                (1, True),
                t_after,
                (2, True),
                2 * t_after,
                (0, False),
                (2, False),
                (1, False),
                t_after,
            ],
            [{KC.X}, {KC.X, KC.C}, {KC.C}, {}],
        )

        keyboard.test(
            'match: 2 combo hold + other, interleaved, after timeout',
            [
                (0, True),
                (1, True),
                t_after,
                (4, True),
                (4, False),
                (0, False),
                (1, False),
                t_after,
            ],
            [{KC.X}, {KC.X, KC.E}, {KC.X}, {}],
        )

        keyboard.test(
            'match: 2 combo hold + overlap, interleaved, after timeout',
            [
                (0, True),
                (1, True),
                t_after,
                (2, True),
                (2, False),
                2 * t_after,
                (0, False),
                (1, False),
                t_after,
            ],
            [{KC.X}, {KC.X, KC.C}, {KC.X}, {}],
        )

        keyboard.test(
            'match: other + 2 combo, after timeout',
            [
                (4, True),
                t_after,
                (0, True),
                (1, True),
                t_after,
                (1, False),
                (4, False),
                (0, False),
                t_after,
            ],
            [{KC.E}, {KC.E, KC.X}, {KC.E}, {}],
        )

        keyboard.test(
            'match: 2 combo + other, after timeout',
            [
                (0, True),
                (1, True),
                t_after,
                (4, True),
                (1, False),
                (4, False),
                (0, False),
                t_after,
            ],
            [{KC.X}, {KC.E, KC.X}, {KC.E}, {}],
        )

        #
        keyboard.test(
            'match: 2 combo + 2 combo, after timeout',
            [
                (0, True),
                (1, True),
                t_after,
                (2, True),
                (3, True),
                2 * t_after,
                (0, False),
                (1, False),
                (2, False),
                (3, False),
                t_after,
            ],
            [{KC.X}, {KC.X, KC.Z}, {KC.Z}, {}],
        )

        keyboard.test(
            'match: 2 combo hold + 2 combo, after timeout',
            [
                (0, True),
                (1, True),
                t_after,
                (2, True),
                (3, True),
                2 * t_after,
                (2, False),
                (3, False),
                t_after,
                (0, False),
                (1, False),
                t_after,
            ],
            [{KC.X}, {KC.X, KC.Z}, {KC.X}, {}],
        )

        keyboard.test(
            'no match: partial combor, after timeout',
            [(0, True), (0, False), t_after],
            [{KC.A}, {}],
        )

        keyboard.test(
            'no match: partial combo, repeated',
            [
                (0, True),
                (0, False),
                t_within,
                (0, True),
                (0, False),
                t_within,
                (0, True),
                (0, False),
                t_after,
            ],
            [{KC.A}, {}, {KC.A}, {}, {KC.A}, {}],
        )

        keyboard.test(
            'no match: partial combo, repeated',
            [
                t_after,
                (0, True),
                (0, False),
                (1, True),
                (1, False),
                t_within,
                (0, True),
                (0, False),
                t_after,
            ],
            [{KC.A}, {}, {KC.B}, {}, {KC.A}, {}],
        )

        keyboard.test(
            'no match: 3 combo after timout',
            [
                (0, True),
                (2, True),
                t_after,
                (1, True),
                t_after,
                (1, False),
                (0, False),
                (2, False),
                t_after,
            ],
            [{KC.A}, {KC.A, KC.C}, {KC.A, KC.C, KC.B}, {KC.A, KC.C}, {KC.C}, {}],
        )

        keyboard.test(
            'no match: other + 2 combo within timeout',
            [
                (4, True),
                t_within,
                (0, True),
                (1, True),
                t_after,
                (1, False),
                (4, False),
                (0, False),
                t_after,
            ],
            [{KC.E}, {KC.E, KC.A}, {KC.E, KC.A, KC.B}, {KC.E, KC.A}, {KC.A}, {}],
        )

        keyboard.test(
            'no match: 2 + other combo within timeout',
            [
                (0, True),
                t_within,
                (1, True),
                (4, True),
                t_after,
                (1, False),
                (4, False),
                (0, False),
                t_after,
            ],
            [{KC.A}, {KC.A, KC.B}, {KC.A, KC.B, KC.E}, {KC.A, KC.E}, {KC.A}, {}],
        )

        keyboard.test(
            'no match: 2 Combo after timeout',
            [(0, True), (0, False), t_after, (1, True), (1, False), t_after],
            [{KC.A}, {}, {KC.B}, {}],
        )

        keyboard.test(
            'no match: Combo + other, within timeout',
            [
                (0, True),
                (1, True),
                (4, True),
                (0, False),
                (1, False),
                (4, False),
                t_after,
            ],
            [{KC.A}, {KC.A, KC.B}, {KC.A, KC.B, KC.E}, {KC.B, KC.E}, {KC.E}, {}],
        )

        keyboard.test(
            'no match: Combo + other, within timeout',
            [
                (0, True),
                (4, True),
                (1, True),
                (0, False),
                (1, False),
                (4, False),
                t_after,
            ],
            [{KC.A}, {KC.A, KC.E}, {KC.A, KC.B, KC.E}, {KC.B, KC.E}, {KC.E}, {}],
        )

        # test sequences
        keyboard.keyboard.active_layers = [1]
        keyboard.test(
            'match: leader sequence, within timeout',
            [(5, True), (5, False), t_within, (0, True), (0, False), t_after],
            [{KC.V}, {}],
        )

        keyboard.test(
            'match: 2 sequence, within timeout',
            [(0, True), (0, False), t_within, (1, True), (1, False), t_after],
            [{KC.X}, {}],
        )

        keyboard.test(
            'match: 2 sequence, within long timeout',
            [(2, True), (2, False), 2 * t_within, (3, True), (3, False), 2 * t_after],
            [{KC.Z}, {}],
        )

        keyboard.test(
            'match: 3 sequence, within timeout',
            [
                (0, True),
                (0, False),
                t_within,
                (1, True),
                (1, False),
                t_within,
                (2, True),
                (2, False),
                t_after,
            ],
            [{KC.Y}, {}],
        )

        keyboard.test(
            'match: 3 sequence, same key, within timeout',
            [
                (0, True),
                (0, False),
                t_within,
                (0, True),
                (0, False),
                t_within,
                (0, True),
                (0, False),
                t_within,
                t_after,
            ],
            [{KC.W}, {}],
        )

        keyboard.test(
            'no match: 2 sequence, after timeout',
            [(0, True), (0, False), t_after, (1, True), (1, False), t_after],
            [{KC.N1}, {}, {KC.N2}, {}],
        )

        keyboard.test(
            'no match: 2 sequence, out of order',
            [(1, True), (1, False), t_within, (0, True), (0, False), t_after],
            [{KC.N2}, {}, {KC.N1}, {}],
        )


if __name__ == '__main__':
    unittest.main()
