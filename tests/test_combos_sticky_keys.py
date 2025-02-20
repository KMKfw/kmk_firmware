import unittest

from kmk.keys import KC
from kmk.modules.combos import Chord, Combo, Combos
from kmk.modules.sticky_keys import StickyKeys
from tests.keyboard_test import KeyboardTest

t_within = 2 * KeyboardTest.loop_delay_ms
t_combo = 6 * KeyboardTest.loop_delay_ms
t_sticky = 8 * KeyboardTest.loop_delay_ms
t_after = 11 * KeyboardTest.loop_delay_ms

# overide default timeouts
Combo.timeout = t_combo

combos = Combos()
combos.combos = [
    Chord((KC.N0, KC.N1), KC.A),
]

sticky_keys = StickyKeys(release_after=t_sticky)

kb = KeyboardTest(
    [combos, sticky_keys],
    [[KC.N0, KC.N1, KC.SK(KC.LSFT)]],
    debug_enabled=True,
)


class TestCombo(unittest.TestCase):
    def test_0(self):
        kb.test(
            '',
            [(2, True), (2, False), (0, True), (1, True), (0, False), (1, False)],
            [{KC.LSFT}, {KC.LSFT, KC.A}, {KC.LSFT}, {}],
        )

    def test_1(self):
        kb.test(
            '',
            [(2, True), (0, True), (2, False), (1, True), (0, False), (1, False)],
            [{KC.LSFT}, {KC.LSFT, KC.N0}, {KC.N0}, {KC.N0, KC.N1}, {KC.N1}, {}],
        )

    def test_2(self):
        kb.test(
            '',
            [
                (2, True),
                t_after,
                (0, True),
                (1, True),
                (2, False),
                (0, False),
                (1, False),
            ],
            [{KC.LSFT}, {KC.LSFT, KC.A}, {KC.A}, {}],
        )
