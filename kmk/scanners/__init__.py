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

    # for split keyboards, the offset value will be assigned in Split module
    offset = 0

    @property
    def coord_mapping(self):
        return tuple(range(self.offset, self.offset + self.key_count))

    @property
    def key_count(self):
        raise NotImplementedError

    def scan_for_changes(self):
        '''
        Scan for key events and return a key report if an event exists.

        The key report is a byte array with contents [row, col, True if pressed else False]
        '''
        raise NotImplementedError
