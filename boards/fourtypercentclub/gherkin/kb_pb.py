import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation

# For PB Gherkin (version with no LEDs and where switches can be mounted in 4 orientations)
# and Adafruit KB2040


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.A0, board.SCK, board.MISO, board.MOSI, board.D10)
    col_pins = (
        board.D8,
        board.D7,
        board.D6,
        board.D5,
        board.D4,
        board.D3,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    i2c = board.I2C
