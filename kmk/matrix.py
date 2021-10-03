import digitalio

from kmk.scanners import Scanner


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


class KeyEvent:
    def __init__(self, key_number, pressed):
        self.key_number = key_number
        self.pressed = pressed


class MatrixScanner(Scanner):
    def __init__(
        self,
        cols,
        rows,
        diode_orientation=DiodeOrientation.COLUMNS,
        rollover_cols_every_rows=None,
        offset=0,
    ):
        self.len_cols = len(cols)
        self.len_rows = len(rows)
        self.offset = offset

        # A pin cannot be both a row and column, detect this by combining the
        # two tuples into a set and validating that the length did not drop
        #
        # repr() hackery is because CircuitPython Pin objects are not hashable
        unique_pins = {repr(c) for c in cols} | {repr(r) for r in rows}
        assert (
            len(unique_pins) == self.len_cols + self.len_rows
        ), 'Cannot use a pin as both a column and row'
        del unique_pins

        self.diode_orientation = diode_orientation

        # __class__.__name__ is used instead of isinstance as the MCP230xx lib
        # does not use the digitalio.DigitalInOut, but rather a self defined one:
        # https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx/blob/3f04abbd65ba5fa938fcb04b99e92ae48a8c9406/adafruit_mcp230xx/digital_inout.py#L33

        if self.diode_orientation == DiodeOrientation.COLUMNS:
            self.outputs = [
                x
                if x.__class__.__name__ == 'DigitalInOut'
                else digitalio.DigitalInOut(x)
                for x in cols
            ]
            self.inputs = [
                x
                if x.__class__.__name__ == 'DigitalInOut'
                else digitalio.DigitalInOut(x)
                for x in rows
            ]
            self.translate_coords = True
        elif self.diode_orientation == DiodeOrientation.ROWS:
            self.outputs = [
                x
                if x.__class__.__name__ == 'DigitalInOut'
                else digitalio.DigitalInOut(x)
                for x in rows
            ]
            self.inputs = [
                x
                if x.__class__.__name__ == 'DigitalInOut'
                else digitalio.DigitalInOut(x)
                for x in cols
            ]
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

                        row = new_iidx
                        col = new_oidx
                    else:
                        row = oidx
                        col = iidx

                    pressed = new_val
                    self.state[ba_idx] = new_val

                    any_changed = True
                    break

                ba_idx += 1

            opin.value = False
            if any_changed:
                break

        if any_changed:
            key_number = self.len_cols * row + col + self.offset
            return KeyEvent(key_number, pressed)
