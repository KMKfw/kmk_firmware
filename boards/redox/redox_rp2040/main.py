import board
from kb import KMKKeyboard
from kmk.consts import UnicodeMode
from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.split import Split, SplitSide, SplitType
from storage import getmount

keyboard = KMKKeyboard()
keyboard.debug_enabled = True
keyboard.unicode_mode = UnicodeMode.LINUX
keyboard.extensions.append(MediaKeys())
keyboard.modules.append(HoldTap())
keyboard.modules.append(Layers())
keyboard.modules.append(MouseKeys())

split_side = SplitSide.RIGHT if str(getmount('/').label)[-1] == 'R' else SplitSide.LEFT

if split_side == SplitSide.LEFT:
    data_pin = board.GP0
    data_pin2 = board.GP1
else:
    data_pin = board.GP1
    data_pin2 = board.GP0

split = Split(
    split_side=split_side,
    split_target_left=False,
    split_type=SplitType.UART,
    split_flip=True,
    uart_interval=20,
    data_pin=data_pin,
    data_pin2=data_pin2,
    use_pio=True,
)
keyboard.modules.append(split)


keyboard.keymap = [
    [
        # QWERTY
    # fmt: off
#  |--------|--------|--------|--------|--------|--------|--------|                          |--------|--------|--------|--------|--------|--------|--------|
    KC.NO   ,KC.N1   ,KC.N2   ,KC.N3   ,KC.N4   ,KC.N5   ,KC.MO(1),                           KC.MO(1),KC.N6   ,KC.N7   ,KC.N8   ,KC.N9   ,KC.N0   ,KC.NO   ,
#  |--------|--------|--------|--------|--------|--------|--------|                          |--------|--------|--------|--------|--------|--------|--------|
    KC.TAB  ,KC.Q    ,KC.W    ,KC.E    ,KC.R    ,KC.T    ,KC.LBRC ,                           KC.RBRC ,KC.Y    ,KC.U    ,KC.I    ,KC.O    ,KC.P    ,KC.EQL  ,
#  |--------|--------|--------|--------|--------|--------|--------|                          |--------|--------|--------|--------|--------|--------|--------|
    KC.ESC  ,KC.A    ,KC.S    ,KC.D    ,KC.F    ,KC.G    ,                                             KC.H    ,KC.J    ,KC.K    ,KC.L    ,KC.SCLN ,KC.QUOT ,
#  |--------|--------|--------|--------|--------|--------|--------|--------|        |--------|--------|--------|--------|--------|--------|--------|--------|
    KC.LSFT ,KC.Z    ,KC.X    ,KC.C    ,KC.V    ,KC.B    ,KC.NO   ,KC.PGDN ,         KC.HOME ,KC.NO   ,KC.N    ,KC.M    ,KC.COMM ,KC.DOT  ,KC.SLSH ,KC.RSFT ,
#  |--------|--------|--------|--------|--------|--------|--------|--------|        |--------|--------|--------|--------|--------|--------|--------|--------|
    KC.LGUI ,KC.PPLS ,KC.PMNS ,KC.NO   ,     KC.BSPC     ,KC.NO   ,KC.DEL  ,         KC.RALT ,KC.ENT  ,     KC.SPC      ,KC.LEFT ,KC.DOWN ,KC.UP   ,KC.RGHT ,
#  |--------|--------|--------|--------|-----------------|--------|--------|        |--------|--------|-----------------|--------|--------|--------|--------|
    ],



]

if __name__ == '__main__':
    keyboard.go()

