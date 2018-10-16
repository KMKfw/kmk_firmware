import digitalio

from kmk.consts import DiodeOrientation
from kmk.event_defs import matrix_changed


class MatrixScanner:
    def __init__(self, cols, rows, diode_orientation=DiodeOrientation.COLUMNS):
        # A pin cannot be both a row and column, detect this by combining the
        # two tuples into a set and validating that the length did not drop
        #
        # repr() hackery is because CircuitPython Pin objects are not hashable
        unique_pins = {repr(c) for c in cols} | {repr(r) for r in rows}
        if len(unique_pins) != len(cols) + len(rows):
            raise ValueError('Cannot use a pin as both a column and row')

        self.cols = cols
        self.rows = rows
        self.len_cols = len(cols)
        self.len_rows = len(rows)

        self.diode_orientation = diode_orientation
        self.last_pressed_len = 0

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

        import kmk_keyboard

        self.swap_indicies = getattr(kmk_keyboard, 'swap_indicies', {})
        self.rollover_cols_every_rows = getattr(
            kmk_keyboard,
            'rollover_cols_every_rows',
            self.len_rows,
        )

        for k, v in self.swap_indicies.items():
            self.swap_indicies[v] = k

    def scan_for_pressed(self):
        pressed = []

        for oidx, opin in enumerate(self.outputs):
            opin.value(True)

            for iidx, ipin in enumerate(self.inputs):
                if ipin.value():
                    if self.diode_orientation == DiodeOrientation.ROWS:
                        report_tuple = (oidx, iidx)
                    else:
                        new_oidx = oidx + self.len_cols * (iidx // self.rollover_cols_every_rows)
                        new_iidx = iidx - self.rollover_cols_every_rows * (
                            iidx // self.rollover_cols_every_rows
                        )
                        report_tuple = (new_iidx, new_oidx)

                    if report_tuple in self.swap_indicies:
                        report_tuple = self.swap_indicies[report_tuple]

                    pressed.append(report_tuple)

            opin.value(False)

        if len(pressed) != self.last_pressed_len:
            self.last_pressed_len = len(pressed)
            return matrix_changed(pressed)

        return None  # The default, but for explicitness
