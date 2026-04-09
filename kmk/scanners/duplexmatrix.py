import digitalio

from keypad import Event as KeyEvent

from kmk.scanners import Scanner


def ensure_DIO(x):
    # __class__.__name__ is used instead of isinstance as the MCP230xx lib
    # does not use the digitalio.DigitalInOut, but rather a self defined one:
    # https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx/blob/3f04abbd65ba5fa938fcb04b99e92ae48a8c9406/adafruit_mcp230xx/digital_inout.py#L33
    if x.__class__.__name__ == 'DigitalInOut':
        return x
    else:
        return digitalio.DigitalInOut(x)


class DuplexMatrixScanner(Scanner):
    '''
    Duplex (bidirectional) matrix scanner.
    It maps:
    Col0->Row0 = 0, Row0->Col0 = 1
    Col1->Row0 = 2, Row0->Col1 = 3
    and so on.
    '''

    def __init__(self, rows, cols, pull=digitalio.Pull.UP, offset=0):
        self.len_rows = len(rows)
        self.len_cols = len(cols)
        self.pull = pull
        self.offset = offset

        # A pin cannot be both a row and column, detect this by combining the
        # two tuples into a set and validating that the length did not drop
        #
        # repr() hackery is because CircuitPython Pin objects are not hashable
        unique_pins = {repr(c) for c in cols} | {repr(r) for r in rows}
        assert (
            len(unique_pins) == self.len_cols + self.len_rows
        ), 'Cannot use a pin as both a column and row'
        del unique_pins

        self.dio_rows = [ensure_DIO(r) for r in rows]
        self.dio_cols = [ensure_DIO(c) for c in cols]

        # Initialize all pins as inputs
        for pin in self.dio_rows + self.dio_cols:
            pin.switch_to_input(pull=self.pull)

        # Total keys = rows * cols * 2 (bidirectional)
        self._key_count = self.len_rows * self.len_cols * 2
        initial_state_value = b'\x01' if self.pull is digitalio.Pull.UP else b'\x00'
        self.state = bytearray(initial_state_value) * self._key_count

    @property
    def key_count(self):
        return self._key_count

    def _scan_direction(self, outputs, inputs, base_offset):
        '''
        Generic scan for one direction (COL2ROW or ROW2COL)
        outputs: list of pins to drive
        inputs: list of pins to read
        base_offset: 0 or 1 for key_number calculation
        '''
        for o_idx, o_pin in enumerate(outputs):
            o_pin.switch_to_output()
            o_pin.value = False if self.pull == digitalio.Pull.UP else True

            for i_idx, i_pin in enumerate(inputs):
                new_val = int(i_pin.value)
                width = len(outputs)
                key_number = (i_idx * width + o_idx) * 2 + base_offset + self.offset
                old_val = self.state[key_number]

                if old_val != new_val:
                    if self.pull is digitalio.Pull.UP:
                        pressed = not new_val
                    else:
                        pressed = new_val
                    self.state[key_number] = new_val
                    o_pin.switch_to_input(pull=self.pull)
                    return KeyEvent(key_number, pressed)

            o_pin.switch_to_input(pull=self.pull)
        return None

    def scan_for_changes(self):
        # First scan
        event = self._scan_direction(self.dio_cols, self.dio_rows, base_offset=1)
        if event:
            return event

        # Second scan
        return self._scan_direction(self.dio_rows, self.dio_cols, base_offset=0)
