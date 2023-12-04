from kb import KMKKeyboard
from kmk.keys import KC, make_key
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.hex_compose import HexCompose
from kmk.modules.tapdance import TapDance
from kmk.modules.oneshot import OneShot
from kmk.extensions.rgb import RGB, AnimationModes
from kmk.consts import UnicodeMode

from kmk.handlers.sequences import unicode_string_sequence

keyboard = KMKKeyboard(active_encoders=[0], landscape_layout=True)

keyboard.unicode_mode = UnicodeMode.RALT

keyboard.modules += [
    Layers(), 
    OneShot(), 
    HoldTap(), 
    TapDance(), 
    HexCompose(encoding='utf8')
]

rgb = RGB(
    pixel_pin=keyboard.pixel_pin, 
    num_pixels=8,
    animation_mode=AnimationModes.BREATHING,
    animation_speed=3,
    breathe_center=2,
)
keyboard.extensions.append(rgb)
        

def set_backlight(hsv):
    rgb.hue, rgb.sat, rgb.val = hsv


XXXXX = KC.NO
_____ = KC.TRANSPARENT

SPC_ENTER = KC.HT(KC.SPACE, KC.ENTER)
SHFT_CTL = KC.TD(KC.LSHIFT, KC.LCTL)

OS_NUM = KC.OS(KC.MO(2), tap_time=None)
OS_ALPHA = KC.OS(KC.MO(4), tap_time=None)
OS_SYM = KC.OS(KC.MO(6), tap_time=None)

TO_HEX = KC.TO(0)
TO_NUM = KC.TO(2)
TO_ALPHA = KC.TO(4)

colors = dict(
    hex=(180,255,50), 
    num=(265,255,50), 
    alpha=(95,255,50)
)
set_backlight(colors['hex'])
TO_HEX.after_press_handler(lambda *_: set_backlight(colors['hex']))
TO_NUM.after_press_handler(lambda *_: set_backlight(colors['num']))
TO_ALPHA.after_press_handler(lambda *_: set_backlight(colors['alpha']))

# encoder direction does left/right or up/down with alt
keyboard.encoders.map = [
    [(KC.LEFT, KC.RIGHT, XXXXX)],
    [(KC.UP, KC.DOWN, XXXXX)],
] * 4

# encoder button cycles modes (hex, numpad, alpha)
keyboard.keymap = [
    # -----------------------------------------------------------
    # 0: hex
    [
        KC.HEX7,    KC.HEX8,    KC.HEX9,    TO_NUM,     XXXXX,
        KC.HEX4,    KC.HEX5,    KC.HEX6,    KC.HEXA,    KC.HEXB,
        KC.HEX1,    KC.HEX2,    KC.HEX3,    KC.HEXC,    KC.HEXD,
KC.LT(1, OS_SYM),   KC.HEX0,    SPC_ENTER,  KC.HEXE,    KC.HEXF,
    ],
    # 1: hex alt
    [
        XXXXX,      XXXXX,      XXXXX,      XXXXX,      XXXXX,
        XXXXX,      XXXXX,      XXXXX,      OS_ALPHA,   XXXXX,
        XXXXX,      XXXXX,      XXXXX,      XXXXX,      XXXXX,
        XXXXX,      OS_NUM,     XXXXX,      XXXXX,      KC.BSPC
    ],
    # -----------------------------------------------------------
    # 2: numpad
    [
        KC.N7,      KC.N8,      KC.N9,      TO_ALPHA,   XXXXX,
        KC.N4,      KC.N5,      KC.N6,      KC.SLSH,    KC.ASTR,
        KC.N1,      KC.N2,      KC.N3,      KC.MINUS,   KC.PLUS,
KC.LT(3, OS_SYM),   KC.N0,      SPC_ENTER,  KC.EQUAL,   KC.BSPC,
    ],
    # 3: numpad alt
    [
        KC.HOME,    KC.UP,      KC.PGUP,    XXXXX,      XXXXX,
        KC.LEFT,    KC.COMMA,   KC.RIGHT,   OS_ALPHA,   XXXXX,
        KC.END,     KC.DOWN,    KC.PGDN,    XXXXX,      XXXXX,
        XXXXX,      KC.DOT,     KC.TAB,     XXXXX,      KC.ESC,
    ],
    # -----------------------------------------------------------
    # 4: alpha
    [
        KC.S,       KC.T,       KC.U,       TO_HEX,     XXXXX,
        KC.I,       KC.L,       KC.N,       KC.O,       KC.R,
        KC.A,       KC.C,       KC.D,       KC.E,       KC.H,
KC.LT(5, OS_SYM),   SHFT_CTL,   SPC_ENTER,  KC.COMM,    KC.BSPC,
    ],
    # 5: alpha alt 
    [
        KC.X,       KC.Y,       KC.Z,       XXXXX,      XXXXX,
        KC.M,       KC.P,       KC.Q,       KC.V,       KC.W,
        KC.B,       KC.F,       KC.G,       KC.J,       KC.K,
        XXXXX,      OS_NUM,     KC.TAB,     KC.DOT,     KC.ESC,
    ],
    # -----------------------------------------------------------
    # 6: symbols
    [
        KC.QUOT,    KC.LPRN,    KC.RPRN,    XXXXX,      XXXXX,
        KC.DLR,     KC.PERC,    KC.AMPR,    KC.LBRC,    KC.RBRC,
        KC.EXLM,    KC.DQT,     KC.HASH,    KC.SCLN,    KC.EQUAL,
        KC.MO(7),   KC.SLSH,    SPC_ENTER,  KC.COMM,    KC.DOT,
    ],
    # 7: symbols alt
    [
        KC.GRV,     KC.ASTR,    KC.UNDS,    XXXXX,      XXXXX,
        KC.BSLS,    KC.PIPE,    KC.CIRC,    KC.LCBR,    KC.RCBR,
        KC.TILD,    KC.AT,      KC.MINUS,   KC.COLN,    KC.PLUS,
        XXXXX,      KC.QUES,    KC.TAB,     KC.LABK,    KC.RABK,
    ],
]


if __name__ == '__main__':
    keyboard.go()
