import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.layers import Layers
from kmk.modules.combos import Combos

keyboard = KMKKeyboard()

combos = Combos()

keyboard.modules.append(Layers())
keyboard.modules.append(combos)

keyboard.col_pins = (
    board.GP1,
    board.GP14,
    board.GP10,
    board.GP9,
    board.GP8,
    board.GP7,
    board.GP6,
    board.GP5,
    board.GP4,
    board.GP3,
    board.GP2,
    board.GP0
    )

keyboard.row_pins = (
    board.GP15,
    board.GP11,
    board.GP12,
    board.GP13,
    board.GP16,
    board.GP17,
    board.GP18,
    board.GP19
    )

# Choose your layout here
# ==================================

import layout_swe as keyboard_layout
#import layout_uk as keyboard_layout

# ==================================

combos.combos = keyboard_layout.COMBOS
keyboard.keymap = keyboard_layout.KEYMAP


if __name__ == '__main__':
    keyboard.go()