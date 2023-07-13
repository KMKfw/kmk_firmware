from kmk.keys import KC, make_key
from kmk.modules.combos import Combos, Chord, Sequence
combos = Combos()

make_key(
    names=('MYKEY',),
    on_press=lambda *args: print('I pressed MYKEY'),
)

combos.combos = [
    Chord((KC.A, KC.B), KC.LSFT),
    Chord((KC.A, KC.B, KC.C), KC.LALT),
    Chord((0, 1), KC.ESC, match_coord=True),
    Chord((8, 9, 10), KC.MO(4), match_coord=True),
    Sequence((KC.LEADER, KC.A, KC.B), KC.C),
    Sequence((KC.E, KC.F), KC.MYKEY, timeout=500, per_key_timeout=False, fast_reset=False)
]