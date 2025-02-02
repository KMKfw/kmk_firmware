# Isopad pinout
# Credit: u/bomtarnes aka The Keyboard Magpie
from kmk.kmk_keyboard import KMKKeyboard as _KMKeyboard
from kmk.quickpin.pro_micro.kb2040 import pinout as pins
from kmk.scanners.keypad import KeysScanner

# GPIO to key mapping - there's one key
# fmt: off
_KEY_CFG = [
        pins[19]
]


# fmt: on
class KMKKeyboard(_KMKeyboard):
    def __init__(self):
        super().__init__()

        # create and register the scanner
        self.matrix = KeysScanner(_KEY_CFG, value_when_pressed=False)
