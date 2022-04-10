import keypad

from kmk.scanners import DiodeOrientation, Scanner


class KeypadScanner(Scanner):
    '''
    Translation layer around a CircuitPython 7 keypad scanner.

    :param pin_map: A sequence of (row, column) tuples for each key.
    :param kp: An instance of the keypad class.
    '''

    def __init__(self, pin_map, kp):
        self.pin_map = pin_map
        self.keypad = kp
        # for split keyboards, the offset value will be assigned in Split module
        self.offset = 0
        self.coord_mapping = tuple(range(self.key_count))

        self.curr_event = keypad.Event()

    @property
    def key_count(self):
        return self.keypad.key_count

    def scan_for_changes(self):
        '''
        Scan for key events and return a key report if an event exists.

        The key report is a byte array with contents [row, col, True if pressed else False]
        '''
        ev = self.curr_event
        has_event = self.keypad.events.get_into(ev)
        if has_event:
            if self.offset:
                return keypad.Event(ev.key_number + self.offset, ev.pressed)
            else:
                return ev


def MatrixScanner(row_pins, col_pins, direction=DiodeOrientation.COLUMNS):
    '''
    Row/Column matrix using the CircuitPython 7 keypad scanner.

    :param row_pins: A sequence of pins used for rows.
    :param col_pins: A sequence of pins used for columns.
    :param direction: The diode orientation of the matrix.
    '''
    pin_map = [
        (row, col) for row in range(len(row_pins)) for col in range(len(col_pins))
    ]
    kp = keypad.KeyMatrix(
        row_pins, col_pins, columns_to_anodes=(direction == DiodeOrientation.COLUMNS)
    )
    return KeypadScanner(pin_map, kp)


def KeysScanner(pins):
    '''
    GPIO-per-key 'matrix' using the native CircuitPython 7 keypad scanner.

    :param pins: An array of arrays of CircuitPython Pin objects, such that pins[r][c] is the pin for row r, column c.
    '''
    pin_map = [(row, col) for row in range(len(pins)) for col in range(len(pins[row]))]
    kp = keypad.Keys(
        [pins[r][c] for (r, c) in pin_map], value_when_pressed=False, pull=True
    )
    return KeypadScanner(pin_map, kp)
