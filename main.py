import board


from kb import KMKKeyboard, isRight

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide, SplitType

keyboard = KMKKeyboard()
keyboard.tap_time = 100

layers = Layers()

split_side = SplitSide.RIGHT if isRight else SplitSide.LEFT

data_pin = board.GP1 if split_side == SplitSide.LEFT else board.GP0
data_pin2 = board.GP0 if split_side == SplitSide.LEFT else board.GP1

split = Split(
    split_side=split_side,
    split_type=SplitType.UART,
    split_flip=False,
    data_pin=data_pin,
    data_pin2=data_pin2
)
keyboard.modules = [layers, split]



# Same as the default Corne/crkbd keymap by foostan and drashna
keyboard.keymap = [
     [  #QWERTY
        KC.Q,    KC.W,    KC.F,    KC.P,    KC.B,                         KC.J,    KC.L,   KC.U,   KC.Y, KC.NO,\
        KC.A,    KC.S,    KC.S,    KC.T,    KC.G,                         KC.M,    KC.N,   KC.E,   KC.I, KC.O,\
        KC.Z,    KC.X,    KC.C,    KC.D,    KC.V,                         KC.K,    KC.H,   KC.NO,  KC.NO, KC.NO,\
                            KC.BSPACE,    KC.TAB,                         KC.ENTER, KC.SPACE,
    ]
]

if __name__ == '__main__':
    keyboard.go()
