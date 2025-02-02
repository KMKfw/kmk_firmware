import board
import digitalio

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners.keypad import KeysScanner

# VBus pin config
VBUS_PIN = board.VBUS_SENSE  # RPi Pico
# VBUS_PIN = board.A3      # WeAct RP2040 + resistors on Piantor PCB

# split side detection using vbus sense
vbus = digitalio.DigitalInOut(VBUS_PIN)
vbus.direction = digitalio.Direction.INPUT
isRight = not vbus.value

# alternate option: set side based on drive names
# name = str(getmount('/').label)
# isRight = True if name.endswith('R') else False

# GPIO to key mapping, Left
# fmt:off
_KEY_CFG_LEFT = [
    board.GP6,  board.GP5,  board.GP4,  board.GP3,  board.GP2,
    board.GP11, board.GP10, board.GP9,  board.GP8,  board.GP7,
    board.GP15, board.GP14, board.GP13, board.GP12, board.GP16,
                                        board.GP17, board.GP18,
]
# fmt:on

# GPIO to key mapping, Left
# fmt:off
_KEY_CFG_RIGHT = [
    board.GP2,  board.GP3,  board.GP4,  board.GP5,  board.GP6,
    board.GP7,  board.GP8,  board.GP9,  board.GP10, board.GP11,
    board.GP16, board.GP12, board.GP13, board.GP14, board.GP15,
    board.GP18, board.GP17,
]
# fmt:on


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        # create and register the scanner
        self.matrix = KeysScanner(
            pins=_KEY_CFG_RIGHT if isRight else _KEY_CFG_LEFT,
            value_when_pressed=False,
        )

        # fmt: off
        self.coord_mapping = [
             0,  1,  2,  3,  4,   17, 18, 19, 20, 21,
             5,  6,  7,  8,  9,   22, 23, 24, 25, 26,
            10, 11, 12, 13, 14,   27, 28, 29, 30, 31,
                        15, 16,   32, 33
        ]
        # fmt: on
