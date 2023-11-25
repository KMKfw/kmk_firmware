import board

from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.scanners import DiodeOrientation

keyboard = KMKKeyboard()

keyboard.modules.append(Layers())

holdtap = HoldTap()
keyboard.modules.append(holdtap)


NONE = KC.NO
QWERTY = KC.MO(0)
LOWER = KC.MO(1)
RAISE = KC.MO(2)
ADJUST = KC.MO(3)
CAE = KC.LCTL(KC.LALT(KC.END))
CAD = KC.LCTL(KC.LALT(KC.DEL))



ZSFT = KC.HT(KC.Z, KC.LSFT, prefer_hold=True, tap_interrupted=False, tap_time=3000)
SLSHSFT = KC.HT(KC.SLSH, KC.LSFT, prefer_hold=True, tap_interrupted=False, tap_time=3000)
ALCTL = KC.HT(KC.A, KC.LCTRL, prefer_hold=False, tap_interrupted=False, tap_time=150)

# flake8: noqa: E261
keyboard.keymap = [
    [ # QWERTY
     KC.Q,  KC.W,  KC.E,     KC.R,    KC.T,     KC.Y,    KC.U,     KC.I,    KC.O,   KC.P,
     ALCTL, KC.S,  KC.D,     KC.F,    KC.G,     KC.H,    KC.J,     KC.K,    KC.L,   KC.QUOT,
     ZSFT,  KC.X,  KC.C,     KC.V,    KC.B,     KC.N,    KC.M,     KC.COMM, KC.DOT, SLSHSFT,
     NONE, NONE,   KC.LCTL,  LOWER,   KC.SPACE, KC.BSPC, RAISE, KC.RALT,    NONE,  NONE,

     ],
    [ # LOWER
     KC.N1,  KC.N2,  KC.N3,     KC.N4,    KC.N5,     KC.N6,    KC.N7,     KC.N8,    KC.N9,   KC.N0,
     KC.TAB,  KC.LEFT,  KC.DOWN,     KC.UP,    KC.RIGHT,     KC.TRNS,    KC.MINUS,     KC.EQUAL,    KC.LBRC,   KC.RBRC,
     KC.LCTL,  KC.GRAVE,  KC.LGUI,     KC.LALT,    KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS, 	KC.BSLS, KC.SCLN,
     KC.NO, KC.NO, KC.TRNS,     KC.TRNS,    KC.TRNS, KC.ENTER, ADJUST,     KC.TRNS,    KC.NO,  KC.NO,

     ],
    [ # RAISE
     KC.EXLM,  KC.AT,  KC.HASH,     KC.DLR,    KC.PERC,     KC.CIRC,    KC.AMPR,     KC.ASTR,    KC.LPRN,   KC.RPRN,
     KC.ESC,  KC.TRNS,  KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS,    KC.UNDS,     KC.PLUS,    KC.LCBR,   KC.RCBR,
     KC.CAPS,  KC.TILDE,  KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS, KC.PIPE, KC.COLN,
     KC.NO, KC.NO, KC.TRNS,     ADJUST,    KC.TRNS, KC.ENTER, KC.TRNS,     KC.DEL,    KC.NO,  KC.NO,

     ],
     [ # ADJUST
     KC.F1,  KC.F2,  KC.F3,     KC.F4,    KC.F5,     KC.F6,    KC.F7,     KC.F8,    KC.F9,   KC.F10,
     KC.F11,  KC.F12,  KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS,    KC.TRNS,     CAE,    CAD,   CAD,
     KC.TRNS,  KC.TRNS,  KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS,
     KC.NO, KC.NO, KC.TRNS,     KC.TRNS,    KC.TRNS, KC.ENTER, KC.TRNS,     KC.TRNS,    KC.NO,  KC.NO,

     ]
]

# Uncomment for Trackball
# from kmk.modules.pimoroni_trackball import Trackball, TrackballMode
# import busio as io

# i2c1 = io.I2C(scl=board.GP3, sda=board.GP2)
# trackball = Trackball(i2c1, mode=TrackballMode.MOUSE_MODE)
# keyboard.modules.append(trackball)
# trackball.set_rgbw(255, 255, 255, 30)
# trackball.set_red(20)
# trackball.set_green(100)
# trackball.set_blue(100)
# trackball.set_white(40)

# uncomment for Encoders
# from kmk.modules.encoder import EncoderHandler
# encoder_handler = EncoderHandler()
# keyboard.modules = [encoder_handler]
# encoder_handler.pins = ((board.GP12, board.GP13, None, False), (board.GP27, board.GP26, None, False),)

# encoder_handler.map = [(( KC.VOLD, KC.VOLU),(KC.VOLD, KC.VOLU),), # Layer 1
#                      ((KC.VOLD, KC.VOLU),(KC.VOLD, KC.VOLU),), # Layer 2
#                      ((KC.VOLD, KC.VOLU),(KC.VOLD, KC.VOLU),), # Layer 3
#                      ((KC.VOLD, KC.VOLU),(KC.VOLD, KC.VOLU),), # Layer 4
#                      ]

# keyboard.debug_enabled = True

if __name__ == '__main__':
    keyboard.go()
