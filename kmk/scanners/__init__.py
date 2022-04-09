def intify_coordinate(row, col, len_cols):
    return len_cols * row + col


class DiodeOrientation:
    '''
    Orientation of diodes on handwired boards. You can think of:
    COLUMNS = vertical
    ROWS = horizontal

    COL2ROW and ROW2COL are equivalent to their meanings in QMK.
    '''

    COLUMNS = 0
    ROWS = 1
    COL2ROW = COLUMNS
    ROW2COL = ROWS


class Scanner:
    '''
    Base class for scanners.
    '''

    def __init__(self):
        self.coord_mapping = None

    def scan_for_changes(self):
        '''
        Scan for key events and return a key report if an event exists.

        The key report is a byte array with contents [row, col, True if pressed else False]
        '''
        pass
