import digitalio

from kmk.consts import DiodeOrientation


class MatrixScanner:
    def __init__(
        self, cols, rows,
        diode_orientation=DiodeOrientation.COLUMNS,
        rollover_cols_every_rows=None,
        swap_indicies=None,
    ):
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

        if self.diode_orientation == DiodeOrientation.COLUMNS:
            self.outputs = self.cols
            self.inputs = self.rows
            self.translate_coords = True
        elif self.diode_orientation == DiodeOrientation.ROWS:
            self.outputs = self.rows
            self.inputs = self.cols
            self.translate_coords = False
        else:
            raise ValueError('Invalid DiodeOrientation: {}'.format(
                self.diode_orientation,
            ))

        for pin in self.outputs:
            pin.switch_to_output()

        for pin in self.inputs:
            pin.switch_to_input(pull=digitalio.Pull.DOWN)

        self.swap_indicies = {}
        if swap_indicies is not None:
            for k, v in swap_indicies.items():
                self.swap_indicies[self._intify_coordinate(*k)] = v
                self.swap_indicies[self._intify_coordinate(*v)] = k

        self.rollover_cols_every_rows = rollover_cols_every_rows
        if self.rollover_cols_every_rows is None:
            self.rollover_cols_every_rows = self.len_rows

        self.len_state_arrays = self.len_cols * self.len_rows
        self.state = bytearray(self.len_state_arrays)
        self.report = bytearray(3)

    def _intify_coordinate(self, row, col):
        return row << 8 | col

    def scan_for_pressed(self):
        ba_idx = 0
        any_changed = False

        for oidx, opin in enumerate(self.outputs):
            opin.value(True)

            for iidx, ipin in enumerate(self.inputs):
                old_val = self.state[ba_idx]
                new_val = ipin.value()

                if old_val != new_val:
                    if self.translate_coords:
                        new_oidx = oidx + self.len_cols * (iidx // self.rollover_cols_every_rows)
                        new_iidx = iidx - self.rollover_cols_every_rows * (
                            iidx // self.rollover_cols_every_rows
                        )

                        self.report[0] = new_iidx
                        self.report[1] = new_oidx
                    else:
                        self.report[0] = oidx
                        self.report[1] = iidx

                    swap_src = self._intify_coordinate(self.report[0], self.report[1])
                    if swap_src in self.swap_indicies:
                        tgt_row, tgt_col = self.swap_indicies[swap_src]
                        self.report[0] = tgt_row
                        self.report[1] = tgt_col

                    self.report[2] = new_val
                    self.state[ba_idx] = new_val
                    any_changed = True
                    break

                ba_idx += 1

            opin.value(False)

            if any_changed:
                break

        if any_changed:
            return self.report
