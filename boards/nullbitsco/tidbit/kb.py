import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.modules.encoder import EncoderHandler
from kmk.quickpin.pro_micro.bitc_promicro import pinout as pins
from kmk.scanners import DiodeOrientation

# fmt:off
encoder_pinout = [
    (pins[13],  pins[14],   None),      # enc 0, button mapped in matrix
    (pins[10],  pins[11],   None),      # enc 1 (optional)
    (pins[5],   pins[4],    None),      # enc 2 (optional)
    (pins[0],   pins[1],    None),      # enc 3 (optional)
]
# fmt:on


class KMKKeyboard(_KMKKeyboard):
    '''
    Create a nullbits tidbit keyboard.
    optional constructor arguments:

    active_encoders=[0, 2] to list installed encoder positions (first=0)
        then declare keyboard.encoders.map = [(KC.<left> , KC.<right>, None), (...)]
    landscape_layout=True to orient USB port top right rather than left (default)
    '''

    def __init__(self, active_encoders=[0], landscape_layout=False):
        super().__init__()

        # led = digitalio.DigitalInOut(board.D21)
        # led.direction = digitalio.Direction.OUTPUT
        # led.value = False
        self.row_pins = (
            pins[15],
            pins[9],
            pins[8],
            pins[7],
            pins[6],
        )
        self.col_pins = (
            pins[19],
            pins[18],
            pins[17],
            pins[16],
        )
        self.pixel_pin = pins[12]
        self.diode_orientation = DiodeOrientation.ROW2COL
        self.i2c = board.I2C  # TODO ??

        if landscape_layout:
            self.coord_mapping = [
                row * len(self.col_pins) + col
                for col in range(len(self.col_pins))
                for row in reversed(range(len(self.row_pins)))
            ]

        if active_encoders:
            self.encoders = EncoderHandler()
            self.encoders.pins = tuple([encoder_pinout[i] for i in active_encoders])
            self.modules.append(self.encoders)
