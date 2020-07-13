import digitalio
import gc


def intify_coordinate(row, col):
    return row << 8 | col


class DiodeOrientation:
    '''
    Orientation of diodes on handwired boards. You can think of:
    COLUMNS = vertical
    ROWS = horizontal
    '''

    COLUMNS = 0
    ROWS = 1


class MatrixScanner:
    def __init__(
        self,
        cols,
        rows,
        diode_orientation=DiodeOrientation.COLUMNS,
        rollover_cols_every_rows=None,
        seesaw=None,
    ):
        self.seesaw = seesaw

        self.len_cols = len(cols)
        self.len_rows = len(rows)

        # A pin cannot be both a row and column, detect this by combining the
        # two tuples into a set and validating that the length did not drop
        #
        # repr() hackery is because CircuitPython Pin objects are not hashable
        unique_pins = {repr(c) for c in cols} | {repr(r) for r in rows}
        assert (
            len(unique_pins) == self.len_cols + self.len_rows
        ), 'Cannot use a pin as both a column and row'
        del unique_pins
        gc.collect()

        self.diode_orientation = diode_orientation

        if self.diode_orientation == DiodeOrientation.COLUMNS:
            self.outputs = [self._getio(x) for x in cols]
            self.inputs = [self._getio(x) for x in rows]
            self.translate_coords = True
        elif self.diode_orientation == DiodeOrientation.ROWS:
            self.outputs = [self._getio(x) for x in rows]
            self.inputs = [self._getio(x) for x in cols]
            self.translate_coords = False
        else:
            raise ValueError(
                'Invalid DiodeOrientation: {}'.format(self.diode_orientation)
            )

        for pin in self.outputs:
            pin.switch_to_output()

        for pin in self.inputs:
            pin.switch_to_input(pull=digitalio.Pull.DOWN)

        self.rollover_cols_every_rows = rollover_cols_every_rows
        if self.rollover_cols_every_rows is None:
            self.rollover_cols_every_rows = self.len_rows

        self.len_state_arrays = self.len_cols * self.len_rows
        self.state = bytearray(self.len_state_arrays)
        self.report = bytearray(3)

    def _getio(self, pin):
        '''
        Get a DigitalInOut object for 'pin'.  If it is a simple number, then it
        is assumed to be a pin on an attached seesaw; otherwise, it is a standard
        DigitalInOut.
        '''

        if isinstance(pin, int):
            import adafruit_seesaw.digitalio

            return adafruit_seesaw.digitalio.DigitalIO(self.seesaw, pin)

        return digitalio.DigitalInOut(pin)

    def scan_for_changes(self):
        '''
        Poll the matrix for changes and return either None (if nothing updated)
        or a bytearray (reused in later runs so copy this if you need the raw
        array itself for some crazy reason) consisting of (row, col, pressed)
        which are (int, int, bool)
        '''
        ba_idx = 0
        any_changed = False

        for oidx, opin in enumerate(self.outputs):
            opin.value = True

            for iidx, ipin in enumerate(self.inputs):
                # cast to int to avoid
                #
                # >>> xyz = bytearray(3)
                # >>> xyz[2] = True
                # Traceback (most recent call last):
                #   File "<stdin>", line 1, in <module>
                # OverflowError: value would overflow a 1 byte buffer
                #
                # I haven't dived too far into what causes this, but it's
                # almost certainly because bool types in Python aren't just
                # aliases to int values, but are proper pseudo-types
                new_val = int(ipin.value)
                old_val = self.state[ba_idx]

                if old_val != new_val:
                    if self.translate_coords:
                        new_oidx = oidx + self.len_cols * (
                            iidx // self.rollover_cols_every_rows
                        )
                        new_iidx = iidx - self.rollover_cols_every_rows * (
                            iidx // self.rollover_cols_every_rows
                        )

                        self.report[0] = new_iidx
                        self.report[1] = new_oidx
                    else:
                        self.report[0] = oidx
                        self.report[1] = iidx

                    self.report[2] = new_val
                    self.state[ba_idx] = new_val

                    any_changed = True
                    break

                ba_idx += 1

            opin.value = False
            if any_changed:
                break

        if any_changed:
            return self.report
