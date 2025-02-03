import board
import digitalio

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.led = digitalio.DigitalInOut(board.D9)
        self.led.direction = digitalio.Direction.OUTPUT
        self.led.value = False
        self.row_pins = (board.D10, board.MOSI, board.MISO, board.D8)
        self.col_pins = (
            board.D4,
            board.D7,
            board.SCK,
        )
        self.diode_orientation = DiodeOrientation.COLUMNS
        self.i2c = board.I2C
