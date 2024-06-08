import board

from kb import KMKKeyboard

from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.extensions.peg_rgb_matrix import Rgb_matrix
from kmk.hid import HIDModes
from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide

keyboard = KMKKeyboard()
holdtap = HoldTap()
layers = Layers()
keyboard.modules.append(layers)
keyboard.modules.append(holdtap)

display = Display(
    display=SSD1306(sda=board.D4, scl=board.D5),
    entries=[TextEntry(text='Layer: ', x=0, y=32, y_anchor='B')]
    + [TextEntry(text=str(_), x=40, y=32, layer=_) for _ in range(9)],
)
keyboard.extensions.append(display)

# Default RGB matrix colours
rgb = Rgb_matrix(
    ledDisplay=[
        [85, 0, 255],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [85, 0, 255],
        [85, 0, 255],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [85, 0, 255],
        [85, 0, 255],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [85, 0, 255],
        [85, 0, 255],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [85, 0, 255],
        [85, 0, 255],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [85, 0, 255],
        [85, 0, 255],
        [85, 0, 255],
        [85, 0, 255],
        [0, 255, 234],
        [0, 255, 234],
        [85, 0, 255],
        [85, 0, 255],
        [85, 0, 255],
        [85, 0, 255],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [85, 0, 255],
        [85, 0, 255],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [0, 255, 234],
        [85, 0, 255],
    ],
    split=True,
    rightSide=False,
    disable_auto_write=True,
)
keyboard.extensions.append(rgb)

# TODO Comment one of these on each side
split_side = SplitSide.LEFT
# split_side = SplitSide.RIGHT
split = Split(data_pin=keyboard.rx, data_pin2=keyboard.tx, uart_flip=False)
keyboard.modules.append(split)

# fmt:off
keyboard.keymap = [
    [
        KC.ESC,  KC.N1,   KC.N2,   KC.N3,    KC.N4,   KC.N5,                    KC.N6,   KC.N7,    KC.N8,   KC.N9, KC.N0,    KC.GRV,
        KC.TAB,  KC.Q,    KC.W,    KC.E,     KC.R,    KC.T,                     KC.Y,    KC.U,     KC.I,    KC.O,  KC.P,     KC.MINS,
        KC.LCTL, KC.A,    KC.S,    KC.D,     KC.F,    KC.G,                     KC.H,    KC.J,     KC.K,    KC.L,  KC.SCLN,  KC.QUOT,
        KC.LSFT, KC.Z,    KC.X,    KC.C,     KC.V,    KC.B,   KC.LBRC, KC.RBRC, KC.N,    KC.M,  KC.COMMA, KC.DOT,  KC.SLSH,  KC.RSFT,
                                   KC.LGUI, KC.MO(1), KC.LCTL, KC.SPC, KC.ENT,  KC.MO(2), KC.BSPC, KC.RGUI,
        # Encoders
        KC.AUDIO_VOL_UP,
        KC.AUDIO_VOL_DOWN,
        KC.MEDIA_PREV_TRACK,
        KC.MEDIA_NEXT_TRACK,
    ],
    [
        KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,                     KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11, KC.F12,
        KC.TRNS, KC.TRNS, KC.UP,   KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.EQL, KC.TRNS,
        KC.TRNS, KC.LEFT, KC.DOWN, KC.RGHT, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
                                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.DEL,  KC.TRNS,
        # Encoders
        KC.AUDIO_VOL_UP,
        KC.AUDIO_VOL_DOWN,
        KC.MEDIA_PREV_TRACK,
        KC.MEDIA_NEXT_TRACK,
    ],
    [
        KC.N2,   KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC,                   KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.TILD,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.PLUS, KC.UNDS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.COLN, KC.DQT,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.LCBR, KC.RCBR, KC.TRNS, KC.TRNS, KC.LABK, KC.RABK, KC.QUES, KC.TRNS,
                                   KC.LGUI, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.AUDIO_VOL_UP,
        KC.AUDIO_VOL_DOWN,
        KC.MEDIA_PREV_TRACK,
        KC.MEDIA_NEXT_TRACK,
    ],
    [
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
                                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        # Encoders
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
    ],
    [
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
                                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        # Encoders
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
    ],
    [
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
                                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        # Encoders
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
    ],
    [
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
                                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        # Encoders
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
    ],
    [
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
                                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        # Encoders
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
    ],
]
# fmt:on

if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.USB)
