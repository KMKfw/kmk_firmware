print("Starting")

import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.modules.layers import Layers
from storage import getmount
from kmk.extensions.RGB import RGB, AnimationModes

keyboard = KMKKeyboard()
keyboard.debug_enabled = True
keyboard.modules.append(Layers())

split_side = SplitSide.LEFT if str(getmount('/').label)[-1] == 'L' else SplitSide.RIGHT

split = Split(split_type=SplitType.UART,
              split_side=split_side,
              data_pin=board.GP0,
              data_pin2=board.GP1,
              use_pio=True,
              uart_flip=split_side is SplitSide.RIGHT)

keyboard.modules.append(split)

_______ = KC.TRNS
XXXXXXX = KC.NO
FnKey = KC.MO(1)

keyboard.diode_orientation = DiodeOrientation.COL2ROW
keyboard.col_pins = (
            board.GP29,
            board.GP28,
            board.GP27,
            board.GP7,
            board.GP2,
            board.GP3,
            board.GP11,
            board.GP12,
            board.GP13,
)
if split_side is SplitSide.RIGHT:
    keyboard.row_pins = (
                board.GP8,
                board.GP9,
                board.GP16,            
                board.GP19,
                board.GP26,
                board.GP17,
    )
else:
    keyboard.row_pins = (
                board.GP26,
                board.GP25,
                board.GP19,
                board.GP24,
                board.GP17,
                board.GP16,
    )

keyboard.keymap = [
    [
        KC.MUTE, KC.ESC, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5, KC.F6,              KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12, KC.DEL, KC.INS,
        KC.F1, KC.F2, KC.GRV, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6,         KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS, KC.EQL, KC.BSPC, KC.HOME,
        KC.F3, KC.F4, KC.TAB, KC.Q, KC.W, KC.E, KC.R, KC.T,                     KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRC, KC.RBRC, KC.BSLS, KC.END,
        KC.F5, KC.F6, KC.CAPS, KC.A, KC.S, KC.D, KC.F, KC.G,                    KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT, KC.ENT, KC.PGUP,
        KC.F7, KC.F8, KC.LSFT, KC.Z, KC.X, KC.C, KC.V, KC.B,                    KC.N, KC.M, KC.COMM, KC.DOT, KC.SLSH, KC.RSFT, KC.UP, KC.PGDN,
        KC.F9, KC.F10, KC.LCTL, KC.LALT, KC.LGUI, KC.MO(1), KC.SPC,     KC.MO(1), KC.SPC, KC.RALT, KC.RCTL, KC.RGUI, KC.LEFT, KC.DOWN, KC.RGHT
    ]
]


keyboard.coord_mapping = [0,  2, 3, 4, 5, 6, 7, 8,                 91, 92, 93, 94, 95, 96, 97, 98,
                          9, 10, 11, 12, 13, 14, 15, 16, 17,          72, 73, 74, 75, 76, 77, 79, 80,
                          18, 19, 20, 21, 22, 23, 24, 25,           81, 82, 83, 84, 85, 86, 87, 88, 89,
                          27, 28, 29, 30, 31, 32, 33, 34,              99, 100, 101, 102, 103, 104, 106, 107,
                          36, 37, 38, 40, 41, 42, 43, 44,            63, 64, 65, 66, 67, 69, 70, 71,
                          45, 46, 47, 48, 49, 50, 52,                 55, 56, 57, 58, 60, 61, 62]

keyboard.extensions = []


if __name__ == '__main__':
    keyboard.go()
    