import supervisor

from kb import KMKKeyboard

from kmk.extensions.peg_oled_display import (
    Oled,
    OledData,
    OledDisplayMode,
    OledReactionType,
)
from kmk.extensions.peg_rgb_matrix import Rgb_matrix
from kmk.handlers.sequences import send_string
from kmk.hid import HIDModes
from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide, SplitType

keyboard = KMKKeyboard()
holdtap = HoldTap()
layers = Layers()
keyboard.modules.append(layers)
keyboard.modules.append(holdtap)

oled = Oled(
    OledData(
        corner_one={0: OledReactionType.STATIC, 1: ['qwertyzzzz']},
        corner_two={
            0: OledReactionType.LAYER,
            1: ['1', '2', '3', '4', '5', '6', '7', '8'],
        },
        corner_three={
            0: OledReactionType.LAYER,
            1: ['base', 'raise', 'lower', 'adjust', '5', '6', '7', '8'],
        },
        corner_four={
            0: OledReactionType.LAYER,
            1: ['qwertyzzz', 'nums', 'shifted', 'leds', '5', '6', '7', '8'],
        },
    ),
    toDisplay=OledDisplayMode.TXT,
    flip=False,
)
keyboard.extensions.append(oled)

# Default RGB matrix colours
rgb = Rgb_matrix(
    ledDisplay=[
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
        [80, 0, 80],
    ],
    split=True,
    rightSide=False,
    disable_auto_write=True,
)
keyboard.extensions.append(rgb)

# TODO Comment one of these on each side
split_side = SplitSide.LEFT
# split_side = SplitSide.RIGHT
split = Split(data_pin=keyboard.data_pin)
keyboard.modules.append(split)

keyboard.keymap = [
    [
        KC.F1,
        KC.F2,
        KC.F3,
        KC.F4,
        KC.F5,
        KC.F6,
        KC.F7,
        KC.F8,
        KC.F9,
        KC.F10,
        KC.F11,
        KC.F12,
        KC.ESC,
        KC.N1,
        KC.N2,
        KC.N3,
        KC.N4,
        KC.N5,
        KC.N6,
        KC.N7,
        KC.N8,
        KC.N9,
        KC.N0,
        KC.GRV,
        KC.TAB,
        KC.Q,
        KC.W,
        KC.E,
        KC.R,
        KC.T,
        KC.NO,
        KC.NO,
        KC.Y,
        KC.U,
        KC.I,
        KC.O,
        KC.P,
        KC.MINS,
        KC.LCTL,
        KC.A,
        KC.S,
        KC.D,
        KC.F,
        KC.G,
        KC.NO,
        KC.NO,
        KC.H,
        KC.J,
        KC.K,
        KC.L,
        KC.SCLN,
        KC.QUOT,
        KC.LSFT,
        KC.Z,
        KC.X,
        KC.C,
        KC.V,
        KC.B,
        KC.LBRC,
        KC.RBRC,
        KC.N,
        KC.M,
        KC.COMMA,
        KC.DOT,
        KC.SLSH,
        KC.RSFT,
        KC.NO,
        KC.NO,
        KC.NO,
        KC.LGUI,
        KC.MO(1),
        KC.LCTL,
        KC.SPC,
        KC.ENT,
        KC.MO(2),
        KC.BSPC,
        KC.RGUI,
        KC.NO,
        KC.NO,
        KC.NO,
    ],
    [
        KC.F1,
        KC.F2,
        KC.F3,
        KC.F4,
        KC.F5,
        KC.F6,
        KC.F7,
        KC.F8,
        KC.F9,
        KC.F10,
        KC.F11,
        KC.F12,
        KC.TRNS,
        KC.TRNS,
        KC.UP,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.EQL,
        KC.TRNS,
        KC.TRNS,
        KC.LEFT,
        KC.DOWN,
        KC.RGHT,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.LEFT,
        KC.DOWN,
        KC.RGHT,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.DEL,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
    ],
    [
        KC.N2,
        KC.EXLM,
        KC.AT,
        KC.HASH,
        KC.DLR,
        KC.PERC,
        KC.CIRC,
        KC.AMPR,
        KC.ASTR,
        KC.LPRN,
        KC.RPRN,
        KC.TILD,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.PLUS,
        KC.UNDS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.LCBR,
        KC.RCBR,
        KC.TRNS,
        KC.TRNS,
        KC.LABK,
        KC.RABK,
        KC.QUES,
        KC.TRNS,
    ],
    [
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
    ],
    [
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
    ],
    [
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
    ],
    [
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
    ],
    [
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
    ],
]
if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.USB)
