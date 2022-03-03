import keypad

from kmk.matrix import DiodeOrientation
from kmk.scanners import Scanner


class NativeKeypadScanner(Scanner):
    '''
    Translation layer around a CircuitPython 7 keypad scanner.

    :param pin_map: A sequence of (row, column) tuples for each key.
    :param kp: An instance of the keypad class.
    '''

    def __init__(self, pin_map, kp):
        self.pin_map = pin_map
        self.keypad = kp
        self.coord_mapping = list(range(len(pin_map)))

        self.curr_event = keypad.Event()

    def scan_for_changes(self):
        '''
        Scan for key events and return a key report if an event exists.

        The key report is a byte array with contents [row, col, True if pressed else False]
        '''
        ev = self.curr_event
        has_event = self.keypad.events.get_into(ev)
        if has_event:
            return ev


def keypad_matrix(row_pins, col_pins, direction=DiodeOrientation.COLUMNS):
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
    return NativeKeypadScanner(pin_map, kp)


def keys_scanner(pins):
    '''
    GPIO-per-key 'matrix' using the native CircuitPython 7 keypad scanner.

    :param pins: An array of arrays of CircuitPython Pin objects, such that pins[r][c] is the pin for row r, column c.
    '''
    pin_map = [(row, col) for row in range(len(pins)) for col in range(len(pins[row]))]
    kp = keypad.Keys(
        [pins[r][c] for (r, c) in pin_map], value_when_pressed=False, pull=True
    )
    return NativeKeypadScanner(pin_map, kp)
