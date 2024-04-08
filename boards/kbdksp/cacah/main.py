print("Starting Cacah Keyboard")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler

keyboard = KMKKeyboard()

keyboard.col_pins = (
  board.GP18,
  board.GP19,
  board.GP0,
  board.GP1
)

keyboard.row_pins = (
  board.GP2,
  board.GP3,
  board.GP4,
  board.GP8,
  board.GP9
)

keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymap = [
  [
    KC.NLCK, KC.PSLS, KC.PAST, KC.PMNS,
    KC.P7, KC.P8, KC.P9, KC.PPLS,
    KC.P4, KC.P5, KC.P6, KC.NUBS,
    KC.P1, KC.P2, KC.P3, KC.PENT,
    KC.P0, KC.P0, KC.PDOT, KC.PENT
  ]
]

encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.GP16, board.GP17, None, False),)
encoder_handler.map = (
    ((KC.VOLD, KC.VOLU),),  # base layer
)

keyboard.modules.append(encoder_handler)

if __name__ == '__main__':
    keyboard.go()

