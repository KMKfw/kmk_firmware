import unittest

from kmk.keys import KC
from kmk.modules.combos import Chord, Combo, Combos, Sequence
from kmk.modules.layers import Layers
from tests.keyboard_test import KeyboardTest


class TestCombo(unittest.TestCase):
    def setUp(self):
        self.t_within = 2 * KeyboardTest.loop_delay_ms
        self.t_after = 7 * KeyboardTest.loop_delay_ms
        timeout = (self.t_after + self.t_within) // 2

        # overide default timeouts
        Combo.timeout = timeout
        Sequence.timeout = timeout

        combos = Combos()
        layers = Layers()
        KCMO = KC.MO(1)
        combos.combos = [
            Chord((KC.A, KC.B, KC.C), KC.Y),
            Chord((KC.A, KC.B), KC.X),
            Chord((KC.C, KC.D), KC.Z, timeout=2 * timeout),
            Chord((KC.C, KCMO), KC.Z),
            Chord((KC.F, KC.G), KC.Z, timeout=3 * timeout),
            Sequence((KC.N1, KC.N2, KC.N3), KC.Y),
            Sequence((KC.N1, KC.N2), KC.X),
            Sequence((KC.N3, KC.N4), KC.Z, timeout=2 * timeout),
            Sequence((KC.N1, KC.N1, KC.N1), KC.W),
            Sequence((KC.N3, KC.N2, KC.N1), KC.Y, fast_reset=False),
            Sequence((KC.LEADER, KC.N1), KC.V),
        ]
        self.keyboard = KeyboardTest(
            [combos, layers],
            [
                [KC.A, KC.B, KC.C, KC.D, KC.E, KCMO, KC.F, KC.G],
                [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.LEADER],
            ],
            debug_enabled=False,
        )

    def test_chord(self):
        keyboard = self.keyboard
        t_within = self.t_within
        t_after = self.t_after

        keyboard.test(
            'match: 2 combo, within timeout',
            [(0, True), t_within, (1, True), (0, False), (1, False), t_after],
            [{KC.X}, {}],
        )

        keyboard.test(
            'match: 3 combo, within timeout, shuffled',
            [
                (0, True),
                (2, True),
                (1, True),
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
                t_after,
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

        keyboard.test(
            'match: 2 combo, partial release and repeat',
            [
                (0, True),
                (1, True),
                t_after,
                (1, False),
                t_after,
                (1, True),
                (1, False),
                (0, False),
                t_after,
            ],
            [{KC.X}, {}, {KC.X}, {}],
        )

        keyboard.test(
            'match: 2 combo, partial release and repeat',
            [
                (0, True),
                (2, True),
                (1, True),
                t_after,
                (1, False),
                (0, False),
                t_after,
                (1, True),
                (0, True),
                (1, False),
                (0, False),
                (2, False),
                t_after,
            ],
            [{KC.Y}, {}, {KC.Y}, {}],
        )

        keyboard.test(
            'match: 2 combo + 2 combo, after timeout',
            [
                (0, True),
                (1, True),
                t_after,
                (2, True),
                (3, True),
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
            'no match: partial combo, after timeout',
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
            'no match: 2 combo + other within timeout',
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
            'no match: 2 combo after timeout',
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

        # test combos with layer switch
        keyboard.test(
            'match: Combo containing layer switch, within timeout',
            [
                (5, True),
                (2, True),
                (2, False),
                (5, False),
                t_after,
            ],
            [{KC.Z}, {}],
        )

        keyboard.test(
            'no match: Combo containing layer switch + other, within timeout',
            [
                (5, True),
                (0, True),
                (0, False),
                (5, False),
                t_after,
            ],
            [{KC.N1}, {}],
        )

        keyboard.test(
            'match: Other pressed and released before combo, delay after other press but within the combo timeout',
            [
                (1, True),
                t_within,
                t_within,
                (1, False),
                (7, True),
                (6, True),
                (6, False),
                (7, False),
                t_after,
            ],
            [{KC.B}, {}, {KC.Z}, {}],
        )

        keyboard.test(
            'match: Other pressed and released before combo, delay after other release but within the combo timeout',
            [
                (1, True),
                (1, False),
                t_within,
                t_within,
                (7, True),
                (6, True),
                (6, False),
                (7, False),
                t_after,
            ],
            [{KC.B}, {}, {KC.Z}, {}],
        )
        keyboard.test(
            'match: Other pressed and released before combo, delay after other pressed but within the combo timeout, other is part of another combo',
            [
                (0, True),
                t_within,
                t_within,
                (0, False),
                (7, True),
                (6, True),
                (6, False),
                (7, False),
                t_after,
            ],
            [{KC.A}, {}, {KC.Z}, {}],
        )
        keyboard.test(
            'match: Other pressed and released before combo, delay after other release but within the combo timeout, other is part of another combo',
            [
                (0, True),
                (0, False),
                t_within,
                t_within,
                (7, True),
                (6, True),
                (6, False),
                (7, False),
                t_after,
            ],
            [{KC.A}, {}, {KC.Z}, {}],
        )

    def test_sequence(self):
        keyboard = self.keyboard
        t_within = self.t_within
        t_after = self.t_after

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
                t_after,
            ],
            [{KC.W}, {}],
        )

        keyboard.test(
            'match: 3 sequence hold + other, within timeout',
            [
                (0, True),
                (0, False),
                (0, True),
                (0, False),
                (0, True),
                t_after,
                (4, True),
                (0, False),
                (4, False),
                t_after,
            ],
            [{KC.W}, {KC.W, KC.N5}, {KC.N5}, {}],
        )

        keyboard.test(
            'match: 3 sequence, partial release and repeat',
            [
                (2, True),
                (1, True),
                (0, True),
                (0, False),
                (1, False),
                (1, True),
                (0, True),
                (1, False),
                (2, False),
                (0, False),
                t_after,
            ],
            [{KC.Y}, {}, {KC.Y}, {}],
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
