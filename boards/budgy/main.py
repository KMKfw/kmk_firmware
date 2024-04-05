# Created by https://github.com/JakobEdvardsson/

import board
import digitalio

from kb import KMKKeyboard, isRight

from kmk.extensions.media_keys import MediaKeys
from kmk.modules.combos import Combos
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers as _Layers
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.split import Split, SplitSide, SplitType
from kmk.modules.tapdance import TapDance

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

holdtap = HoldTap()
mediaKeys = MediaKeys()
combos = Combos()
tapdance = TapDance()

mousekeys = MouseKeys(
    max_speed=25,
    acc_interval=17,  # Delta ms to apply acceleration
    move_step=1
)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


# Enable LED if on mouse layer
class Layers(_Layers):
    last_top_layer = 0

    def after_hid_send(self, keyboard):
        if keyboard.active_layers[0] != self.last_top_layer:
            self.last_top_layer = keyboard.active_layers[0]
            if self.last_top_layer == 6:  # mouse layer
                led.value = True
            else:
                led.value = False


layers = Layers()


keyboard.modules = [layers, split, holdtap, combos, mousekeys, tapdance]
keyboard.extensions.append(mediaKeys)

# Todo: Import either keymap_sw (for Swedish Colemak-DH) or keymap_us (for English qwerty)
# import keymap_us as keymap  # noqa: E402
import keymap_sw as keymap  # noqa: E402

# Combo layer
layers.combo_layers = keymap.COMBO_LAYER

# Combos
combos.combos = keymap.COMBOS

# Keymap
keyboard.keymap = keymap.KEYMAP

if __name__ == '__main__':
    keyboard.go()
