import board
import digitalio

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.modules.encoder import EncoderHandler
from kmk.quickpin.pro_micro.bitc_promicro import pinout as pins
from kmk.scanners import DiodeOrientation
from kmk.scanners.digitalio import MatrixScanner

# bitc pro pinout: https://nullbits.co/static/img/bitc_pro_pinout.png
# nibble/tidbit pinout: https://github.com/nullbitsco/docs/blob/main/nibble/build_guide_img/mcu_pinouts.png
# key - diode mapping https://nullbits.co/static/file/NIBBLE_diode_key.pdf
# row connects to anode end, col connects to cathode end

# also defined: board.LED_RED, board.LED_GREEN, and board.LED_BLUE == board.LED
row_pins = (pins[15], pins[14], pins[13], pins[12], pins[6])  # GPIO 22,20,23,21,4
col_mux_pins = (pins[19], pins[18], pins[17], pins[16])  # GPIO 29..26
encoder_pins = (pins[10], pins[11], None)  # GPIO 8,9, button in key matrix
pixel_pin = pins[9]  # GPIO 7
# LED R, G, B pins: GPIO 6, 5, 3
# extension pins GPIO 11, 12, 13, 14


class KMKKeyboard(_KMKKeyboard):
    '''
    Create a nullbits nibble keyboard.
    optional constructor arguments:

    encoder=True if encoder installed
        then declare keyboard.encoders.map = [(KC.<left> , KC.<right>, None), (...)]
    '''

    pixel_pin = pixel_pin
    i2c = board.I2C  # TODO ??

    def __init__(self, encoder=False):
        super().__init__()

        self.matrix = MatrixScanner(
            col_mux_pins,
            row_pins,
            diode_orientation=DiodeOrientation.ROW2COL,  # row is anode, col is cathode
            pull=digitalio.Pull.UP,
            multiplexed=True,
        )

        if encoder:
            self.encoders = EncoderHandler()
            self.encoders.pins = (encoder_pins,)
            self.modules.append(self.encoders)
