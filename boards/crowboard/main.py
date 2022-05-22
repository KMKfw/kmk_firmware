import board
import busio as io


from kmk.kmk_keyboard import KMKKeyboard

from kmk.keys import KC
from kmk.scanners import DiodeOrientation

keyboard = KMKKeyboard()
from kmk.modules.layers import Layers
keyboard.modules.append(Layers())
from kmk.modules.modtap import ModTap
modtap = ModTap()
keyboard.modules.append(modtap)

keyboard.col_pins = (board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP18, board.GP19, board.GP20, board.GP21, board.GP22,)    # try D5 on Feather, keeboar
keyboard.row_pins = (board.GP14, board.GP15, board.GP16, board.GP17,)    # try D6 on Feather, keeboar
keyboard.diode_orientation = DiodeOrientation.COL2ROW


NONE = KC.NO
QWERTY = KC.MO(0)
LOWER = KC.MO(1)
RAISE = KC.MO(2)
ADJUST = KC.MO(3)
CAE = KC.LCTL(KC.LALT(KC.END))
CAD = KC.LCTL(KC.LALT(KC.DEL))



ZSFT = KC.MT(KC.Z, KC.LSFT, prefer_hold=True, tap_interrupted=False, tap_time=3000)
SLSHSFT = KC.MT(KC.SLSH, KC.LSFT, prefer_hold=True, tap_interrupted=False, tap_time=3000)
ALCTL = KC.MT(KC.A, KC.LCTRL, prefer_hold=False, tap_interrupted=False, tap_time=150)

keyboard.keymap = [
    [ #QWERTY
     KC.Q,  KC.W,  KC.E,     KC.R,    KC.T,     KC.Y,    KC.U,     KC.I,    KC.O,   KC.P, 
     ALCTL, KC.S,  KC.D,     KC.F,    KC.G,     KC.H,    KC.J,     KC.K,    KC.L,   KC.QUOT, 
     ZSFT,  KC.X,  KC.C,     KC.V,    KC.B,     KC.N,    KC.M,     KC.COMM, KC.DOT, SLSHSFT,
     NONE, NONE,   KC.LCTL,  LOWER,   KC.SPACE, KC.BSPC, RAISE, KC.RALT,    NONE,  NONE,
     
     ],
    [ #LOWER
     KC.N1,  KC.N2,  KC.N3,     KC.N4,    KC.N5,     KC.N6,    KC.N7,     KC.N8,    KC.N9,   KC.N0, 
     KC.TAB,  KC.LEFT,  KC.DOWN,     KC.UP,    KC.RIGHT,     KC.TRNS,    KC.MINUS,     KC.EQUAL,    KC.LBRC,   KC.RBRC, 
     KC.LCTL,  KC.GRAVE,  KC.LGUI,     KC.LALT,    KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS, 	KC.BSLS, KC.SCLN,
     KC.NO, KC.NO, KC.TRNS,     KC.TRNS,    KC.TRNS, KC.ENTER, ADJUST,     KC.TRNS,    KC.NO,  KC.NO,
     
     ],
    [ #RAISE
     KC.EXLM,  KC.AT,  KC.HASH,     KC.DLR,    KC.PERC,     KC.CIRC,    KC.AMPR,     KC.ASTR,    KC.LPRN,   KC.RPRN, 
     KC.ESC,  KC.TRNS,  KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS,    KC.UNDS,     KC.PLUS,    KC.LCBR,   KC.RCBR, 
     KC.CAPS,  KC.TILDE,  KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS, KC.PIPE, KC.COLN,
     KC.NO, KC.NO, KC.TRNS,     ADJUST,    KC.TRNS, KC.ENTER, KC.TRNS,     KC.DEL,    KC.NO,  KC.NO,
     
     ],
     [ #ADJUST
     KC.F1,  KC.F2,  KC.F3,     KC.F4,    KC.F5,     KC.F6,    KC.F7,     KC.F8,    KC.F9,   KC.F10, 
     KC.F11,  KC.F12,  KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS,    KC.TRNS,     CAE,    CAD,   CAD, 
     KC.TRNS,  KC.TRNS,  KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS,
     KC.NO, KC.NO, KC.TRNS,     KC.TRNS,    KC.TRNS, KC.ENTER, KC.TRNS,     KC.TRNS,    KC.NO,  KC.NO,
     
     ]
     
]

if __name__ == '__main__':
    keyboard.go()
