from kmk.consts import DiodeOrientation, UnicodeModes
from kmk.entrypoints.handwire.circuitpython_samd51 import main
from kmk.keycodes import KC
from kmk.macros.simple import send_string
from kmk.macros.unicode import unicode_string_sequence
from kmk.pins import Pin as P
from kmk.types import AttrDict

# physical, visible cols (SCK, MO, MI, RX, TX, D4)
# physical, visible rows (10, 11, 12, 13) (9, 6, 5, SCL)
cols = (P.SCK, P.MOSI, P.MISO, P.RX, P.TX, P.D4)
rows = (P.D10, P.D11, P.D12, P.D13, P.D9, P.D6, P.D5, P.SCL)

swap_indicies = {
    (3, 3): (3, 9),
    (3, 4): (3, 10),
    (3, 5): (3, 11),
}

rollover_cols_every_rows = 4

diode_orientation = DiodeOrientation.COLUMNS


# ------------------User level config variables ---------------------------------------
unicode_mode = UnicodeModes.LINUX
debug_enable = True

keymap = [
    [
        [KC.A, KC.E, KC.I, KC.M, KC.Q, KC.U, KC.N1, KC.N5, KC.N9,      KC.HASH,    KC.AMPR, KC.UNDS],
        [KC.B, KC.F, KC.J, KC.N, KC.R, KC.V, KC.N2, KC.N6, KC.N0,      KC.DOLLAR,  KC.ASTR, KC.LCBR],
        [KC.C, KC.G, KC.K, KC.O, KC.S, KC.W, KC.N3, KC.N7, KC.EXCLAIM, KC.PERCENT, KC.LPRN, KC.RCBR],
        [KC.D, KC.H, KC.L, KC.P, KC.T, KC.X, KC.N4, KC.N8, KC.AT,      KC.CIRC,    KC.RPRN, KC.PIPE],
    ],
]

if __name__ == '__main__':
    main()
