import board
import digitalio

import pwmio
import time
from kb import KMKKeyboard

from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.modules.split import Split, SplitSide, SplitType

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
led.value = True

keyboard = KMKKeyboard()
keyboard.tap_time = 100

layers_ext = Layers()
modtap_ext = ModTap()

# TODO Comment one of these on each side
split_side = SplitSide.LEFT
split_side = SplitSide.RIGHT

data_pin = board.GP1 if split_side == SplitSide.LEFT else board.GP0
data_pin2 = board.GP0 if split_side == SplitSide.LEFT else board.GP1

split = Split(
    split_side=split_side,
    split_type=SplitType.UART,
    split_flip=True,
    data_pin=data_pin,
    data_pin2=data_pin2
)

rgb_ext = RGB(
    pixel_pin=board.GP6,
    num_pixels=6,
    animation_mode=AnimationModes.BREATHING_RAINBOW
)

keyboard.modules = [layers_ext, modtap_ext, split]
keyboard.extensions.append(rgb_ext)

if split_side == SplitSide.LEFT:
    buzzer = pwmio.PWMOut(board.GP8, variable_frequency=True)
    OFF = 0
    ON = 2**15
    buzzer.duty_cycle = ON
    buzzer.frequency = 2000
    time.sleep(0.2)
    buzzer.frequency = 1000
    time.sleep(0.2)
    buzzer.duty_cycle = OFF

LOWER = KC.MO(1)
RAISE = KC.MO(2)
ADJUST = KC.MO(3)
CT_TAB = KC.MT(KC.TAB, KC.LCTRL)
CT_QUOT = KC.MT(KC.QUOT, KC.LCTRL)
SF_MINS = KC.MT(KC.MINS, KC.LSHIFT)
SG_PSCR = KC.LSFT(KC.LGUI(KC.PSCR))
SF_PSCR = KC.LSFT(KC.PSCR)
CG_RGHT = KC.LCTRL(KC.LGUI(KC.RGHT))
RESET = KC.RESET
LANG1 = KC.LANG1
LANG2 = KC.LANG2

keyboard.keymap = [
    [  # QWERTY
        # ------+--------+--------+--------+--------+--------+                 +--------+--------+--------+--------+--------+--------+
        KC.GESC, KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                      KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.BSPC,\
        # ------+--------+--------+--------+--------+--------+                 +--------+--------+--------+--------+--------+--------+
        CT_TAB,  KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                      KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, CT_QUOT,\
        # ------+--------+--------+--------+--------+--------+                 +--------+--------+--------+--------+--------+--------+
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,                      KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, SF_MINS,\
        # ------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
                                   KC.LALT, LANG2,   LOWER,   KC.SPC,  KC.ENT,  RAISE,   LANG1,   KC.RALT
        # ------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
    ],
    [  # LOWER
        # ------+--------+--------+--------+--------+--------+                 +--------+--------+--------+--------+--------+--------+
        KC.BSLS, KC.CIRC, KC.EXLM, KC.AMPR, KC.PIPE, KC.DLR,                    KC.AT,   KC.ASTR, KC.PLUS, KC.EQL,  KC.PERC, KC.BSPC,\
        # ------+--------+--------+--------+--------+--------+                 +--------+--------+--------+--------+--------+--------+
        KC.TRNS, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                     KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.DQT,\
        # ------+--------+--------+--------+--------+--------+                 +--------+--------+--------+--------+--------+--------+
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.COLN, KC.LABK, KC.RABK, KC.QUES, KC.UNDS,\
        # ------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
                                   KC.LGUI, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, ADJUST,  KC.TRNS, KC.LGUI
        # ------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
    ],
    [  # RAISE
        # ------+--------+--------+--------+--------+--------+                 +--------+--------+--------+--------+--------+--------+
        KC.BSLS, KC.CIRC, KC.EXLM, KC.AMPR, KC.PIPE, KC.DLR,                    KC.AT,   KC.ASTR, KC.PLUS, KC.EQL,  KC.PERC, KC.BSPC,\
        # ------+--------+--------+--------+--------+--------+                 +--------+--------+--------+--------+--------+--------+
        KC.HASH, KC.GRV,  KC.LBRC, KC.RBRC, KC.LPRN, KC.RPRN,                   KC.PGUP, KC.HOME, KC.UP,   KC.END,  KC.TRNS, KC.DQT,\
        # ------+--------+--------+--------+--------+--------+                 +--------+--------+--------+--------+--------+--------+
        KC.TRNS, KC.TILD, KC.TRNS, KC.TRNS, KC.LCBR, KC.RCBR,                   KC.PGDN, KC.LEFT, KC.DOWN, KC.RGHT, KC.TRNS, KC.TRNS,\
        # ------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
                                   KC.LGUI, KC.TRNS, ADJUST,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.LGUI
        # ------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
    ],
    [  # ADJUST
        # ------+--------+--------+--------+--------+--------+                 +--------+--------+--------+--------+--------+--------+
        KC.TRNS, RESET,   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                  KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,\
        # ------+--------+--------+--------+--------+--------+                 +--------+--------+--------+--------+--------+--------+
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,\
        # ------+--------+--------+--------+--------+--------+                 +--------+--------+--------+--------+--------+--------+
        KC.TRNS, KC.TRNS, KC.VOLD, KC.VOLU, KC.MUTE, KC.TRNS,                   SG_PSCR, SF_PSCR, KC.CAPS, KC.TRNS, CG_RGHT, KC.TRNS,\
        # ------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
                                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
        # ------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
    ]
]

if __name__ == '__main__':
    keyboard.go()
