from kmk.common.consts import DiodeOrientation


class AbstractMatrixScanner():
    def __init__(self, cols, rows, active_layers, diode_orientation=DiodeOrientation.COLUMNS):
        raise NotImplementedError('Abstract implementation')

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
        raise NotImplementedError('Abstract implementation')
