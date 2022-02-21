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
