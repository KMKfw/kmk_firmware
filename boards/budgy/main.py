# Created by https://github.com/JakobEdvardsson/

import board

from kb import KMKKeyboard, isRight

from kmk.extensions.media_keys import MediaKeys
from kmk.modules.combos import Combos
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide, SplitType

keyboard = KMKKeyboard()

# Split
split_side = SplitSide.RIGHT if isRight else SplitSide.LEFT

data_pin = board.GP1 if split_side == SplitSide.LEFT else board.GP0
data_pin2 = board.GP0 if split_side == SplitSide.LEFT else board.GP1

split = Split(
    split_side=split_side,
    split_type=SplitType.UART,
    split_flip=False,
    data_pin=data_pin,
    data_pin2=data_pin2,
)

layers = Layers()
holdtap = HoldTap()
mediaKeys = MediaKeys()
combos = Combos()

keyboard.modules = [layers, split, holdtap, mediaKeys, combos]


# Todo: Import either keymap_sw (for Swedish Colemak-DH) or keymap_us (for English qwerty)


import keymap_us as keymap  # noqa: E402

# import keymap_sw as keymap # noqa: E402


# Combo layer
layers.combo_layers = keymap.COMBO_LAYER

# Combos
combos.combos = keymap.COMBOS

# Keymap
keyboard.keymap = keymap.KEYMAP

if __name__ == '__main__':
    keyboard.go()
