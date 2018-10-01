from kmk.common.consts import DiodeOrientation


class AbstractMatrixScanner():
    def __init__(self, cols, rows, active_layers, diode_orientation=DiodeOrientation.COLUMNS):
        raise NotImplementedError('Abstract implementation')

    def scan_for_pressed(self):
        raise NotImplementedError('Abstract implementation')
