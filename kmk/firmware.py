from kmk.common.keymap import Keymap

try:
    from kmk.circuitpython.matrix import MatrixScanner
except ImportError:
    from kmk.micropython.matrix import MatrixScanner


class Firmware:
    def __init__(self, keymap, row_pins, col_pins, diode_orientation):
        self.raw_keymap = keymap
        self.keymap = Keymap(keymap)
        self.matrix = MatrixScanner(col_pins, row_pins, diode_orientation)

    def go(self):
        while True:
            for event in self.keymap.parse(self.matrix.raw_scan()):
                print(event)
