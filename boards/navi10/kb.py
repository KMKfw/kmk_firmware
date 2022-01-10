import board
import digitalio

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    led = digitalio.DigitalInOut(board.D9)
    led.direction = digitalio.Direction.OUTPUT
    led.value = False
    row_pins = (board.D10, board.MOSI, board.MISO, board.D8)
    col_pins = (
        board.D4,
        board.D7,
        board.SCK,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    i2c = board.I2C
