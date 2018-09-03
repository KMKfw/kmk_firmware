import board
import time

from kmk.circuitpython.matrix import MatrixScanner
from kmk.common.consts import DiodeOrientation
from kmk.common.keymap import Keymap


if __name__ == '__main__':
    cols = (board.A4, board.A5)
    rows = (board.D27, board.A6)

    matrix = MatrixScanner(
        cols=cols, rows=rows,
        diode_orientation=DiodeOrientation.COLUMNS,
    )

    keymap = Keymap([
        ['A', 'B'],
        ['C', 'D'],
    ])

    while True:
        keymap.parse(matrix.raw_scan())
        # Yield to the controller to allow things like the REPL to take over
        time.sleep(0.001)
