import machine

from kmk.common.abstract.matrix_scanner import AbstractMatrixScanner
from kmk.common.consts import DiodeOrientation


class MatrixScanner(AbstractMatrixScanner):
    def __init__(self, cols, rows, diode_orientation=DiodeOrientation.COLUMNS):
        # A pin cannot be both a row and column, detect this by combining the
        # two tuples into a set and validating that the length did not drop
        unique_pins = set(cols) | set(rows)
        if len(unique_pins) != len(cols) + len(rows):
            raise ValueError('Cannot use a pin as both a column and row')

        self.cols = [machine.Pin(pin) for pin in cols]
        self.rows = [machine.Pin(pin) for pin in rows]
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
            pin.init(machine.Pin.OUT)
            pin.off()

        for pin in self.inputs:
            pin.init(machine.Pin.IN, machine.Pin.PULL_DOWN)
            pin.off()

    def _normalize_matrix(self, matrix):
        return super()._normalize_matrix(matrix)

    def raw_scan(self):
        matrix = []

        for opin in self.outputs:
            opin.value(1)
            matrix.append([bool(ipin.value()) for ipin in self.inputs])
            opin.value(0)

        return self._normalize_matrix(matrix)
