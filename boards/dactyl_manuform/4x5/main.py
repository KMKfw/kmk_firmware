from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.modules.modtap import ModTap
from kmk.extensions.media_keys import MediaKeys

keyboard = KMKKeyboard()

layers_ext = Layers()
keyboard.modules.append(layers_ext)

split = Split(
    data_pin=keyboard.data_pin
    #data_pin2=keyboard.data_pin2
)
keyboard.modules.append(split)

modtap = ModTap()
keyboard.modules.append(modtap)

keyboard.extensions.append(MediaKeys())

LT.ESC = KC.LT(1, KC.ESC)
LT.TAB = KC.LT(2, KC.TAB)
MT.SSPC = KC.MT(KC.SPC, KC.LSFT)
MT.SENT = KC.MT(KC.ENT, KC.RSFT)
MT.CHOM = KC.MT(KC.HOME, KC.LCTL)
MT.CEND = KC.MT(KC.END, KC.RCTL)
MT.ABSP = KC.MT(KC.BSPC, KC.LALT)
MT.ADEL = KC.MT(KC.DEL, KC.LALT)
MT.GLBR = KC.MT(KC.LBRC, KC.LGUI)
MT.GRBR = KC.MT(KC.RBRC, KC.RGUI)

keyboard.keymap = [
    [   #0
        KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                                            KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,
        KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                                            KC.H,    KC.J,    KC.K,    KC.L, KC.SCLN,
        KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,                                            KC.N,    KC.M, KC.COMM,  KC.DOT, KC.QUOT,
              KC.LEFT, KC.RGHT,                                                                               KC.UP, KC.DOWN,
                                          LT.ESC, MT.SSPC,                        MT.SENT, LT.TAB,
                                                  MT.CHOM, MT.ADEL,      MT.ABSP, MT.CEND,
                                                  KC.BSLS, MT.GLBR,      MT.GRBR, KC.SLSH
    ],
    [  #1
        KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.INS,                                        KC.NLCK,  KC.P7,  KC.P8,   KC.P9,  KC.PMNS,
        KC.F5,   KC.F6,   KC.F7,   KC.F8,  KC.PSCR,                                        KC.PAST,  KC.P4,  KC.P5,   KC.P6,  KC.PPLS,
        KC.F9,  KC.F10,  KC.F11,  KC.F12,  KC.PAUS,                                        KC.PSLS,  KC.P1,  KC.P2,   KC.P3,  KC.PENT,
               KC.BRID, KC.BRIU,                                                                             KC.P0, KC.PDOT,
                                           KC.TRNS, KC.TRNS,                        KC.TRNS, KC.MO(3),
                                                    KC.TRNS, KC.TRNS,      KC.TRNS, KC.TRNS,
                                                    KC.TRNS, KC.TRNS,      KC.TRNS, KC.TRNS
    ],
    [  #2
        KC.EXLM,   KC.AT, KC.HASH,  KC.DLR, KC.PERC,                                           KC.CIRC, KC.AMPR, KC.ASTR,  KC.GRV, KC.TILD,
        KC.N1,     KC.N2,   KC.N3,   KC.N4,   KC.N5,                                             KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,
        KC.TRNS, KC.MINS, KC.PLUS, KC.LPRN, KC.TRNS,                                           KC.TRNS, KC.RPRN, KC.UNDS,  KC.EQL, KC.TRNS,
                 KC.PGDN, KC.PGUP,                                                                               KC.TRNS, KC.SLCK,
                                            KC.MO(3), KC.TRNS,                        KC.TRNS, KC.TRNS,
                                                      KC.TRNS, KC.TRNS,      KC.TRNS, KC.TRNS,
                                                      KC.TRNS, KC.TRNS,      KC.TRNS, KC.TRNS
    ],
    [  #3
        KC.NO,   KC.NO,    KC.NO,   KC.NO, KC.NO,                                    KC.NO,   KC.NO,   KC.NO,   KC.NO, KC.NO,
        KC.NO, KC.BRID,  KC.BRIU, KC.MPLY, KC.NO,                                    KC.NO, KC.MUTE, KC.VOLU, KC.VOLD, KC.NO,
        KC.NO,   KC.NO,    KC.NO,   KC.NO, KC.NO,                                    KC.NO,   KC.NO,   KC.NO,   KC.NO, KC.NO,
                 KC.NO, KC.RESET,                                                                     KC.RLD,   KC.NO,
                                         KC.TRNS, KC.NO,                    KC.NO, KC.TRNS,
                                                  KC.NO, KC.NO,      KC.NO, KC.NO,
                                                  KC.NO, KC.NO,      KC.NO, KC.NO
    ]
]

if __name__ == '__main__':
    keyboard.go()
    