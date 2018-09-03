import digitalio

from kmk.common.consts import DiodeOrientation


class MatrixScanner:
    def __init__(self, cols, rows, diode_orientation=DiodeOrientation.COLUMNS):
        # A pin cannot be both a row and column, detect this by combining the
        # two tuples into a set and validating that the length did not drop
        #
        # repr() hackery is because CircuitPython Pin objects are not hashable
        unique_pins = {repr(c) for c in cols} | {repr(r) for r in rows}
        if len(unique_pins) != len(cols) + len(rows):
            raise ValueError('Cannot use a pin as both a column and row')

        self.cols = [digitalio.DigitalInOut(pin) for pin in cols]
        self.rows = [digitalio.DigitalInOut(pin) for pin in rows]
        self.diode_orientation = diode_orientation

        if self.diode_orientation == DiodeOrientation.COLUMNS:
            self.outputs = self.cols
            self.inputs = self.rows
        elif self.diode_orientation == DiodeOrientation.ROWS:
            self.outputs = self.rows
            self.inputs = self.cols
        else:
            raise ValueError('Invalid DiodeOrientation: {}'.format(
                self.diode_orientation,
            ))

        for pin in self.outputs:
            pin.switch_to_output()

        for pin in self.inputs:
            pin.switch_to_input(pull=digitalio.Pull.DOWN)

    def _normalize_matrix(self, matrix):
        '''
        We always want to internally look at a keyboard as a list of rows,
        where a "row" is a list of keycodes (columns).

        This will convert DiodeOrientation.COLUMNS matrix scans into a
        ROWS scan, so we never have to think about these things again.
        '''
        if self.diode_orientation == DiodeOrientation.ROWS:
            return matrix

        return [
            [col[col_entry] for col in matrix]
            for col_entry in range(max(len(col) for col in matrix))
        ]

    def raw_scan(self):
        matrix = []

        for opin in self.outputs:
            opin.value = True
            matrix.append([ipin.value for ipin in self.inputs])
            opin.value = False

        return self._normalize_matrix(matrix)
