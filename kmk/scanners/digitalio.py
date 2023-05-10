import digitalio

from keypad import Event as KeyEvent

from kmk.scanners import DiodeOrientation, Scanner


class MatrixScanner(Scanner):
    def __init__(
        self,
        cols,
        rows,
        diode_orientation=DiodeOrientation.COLUMNS,
        pull=digitalio.Pull.DOWN,
        rollover_cols_every_rows=None,
        offset=0,
    ):
        self.len_cols = len(cols)
        self.len_rows = len(rows)
        self.pull = pull
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
            self.anodes = [
                x
                if x.__class__.__name__ == 'DigitalInOut'
                else digitalio.DigitalInOut(x)
                for x in cols
            ]
            self.cathodes = [
                x
                if x.__class__.__name__ == 'DigitalInOut'
                else digitalio.DigitalInOut(x)
                for x in rows
            ]
            self.translate_coords = True
        elif self.diode_orientation == DiodeOrientation.ROWS:
            self.anodes = [
                x
                if x.__class__.__name__ == 'DigitalInOut'
                else digitalio.DigitalInOut(x)
                for x in rows
            ]
            self.cathodes = [
                x
                if x.__class__.__name__ == 'DigitalInOut'
                else digitalio.DigitalInOut(x)
                for x in cols
            ]
            self.translate_coords = False
        else:
            raise ValueError(f'Invalid DiodeOrientation: {self.diode_orienttaion}')

        if self.pull == digitalio.Pull.DOWN:
            self.outputs = self.anodes
            self.inputs = self.cathodes
        elif self.pull == digitalio.Pull.UP:
            self.outputs = self.cathodes
            self.inputs = self.anodes
        else:
            raise ValueError(f'Invalid pull: {self.pull}')

        for pin in self.outputs:
            pin.switch_to_output()

        for pin in self.inputs:
            pin.switch_to_input(pull=self.pull)

        self.rollover_cols_every_rows = rollover_cols_every_rows
        if self.rollover_cols_every_rows is None:
            self.rollover_cols_every_rows = self.len_rows

        self._key_count = self.len_cols * self.len_rows
        initial_state_value = b'\x01' if self.pull is digitalio.Pull.UP else b'\x00'
        self.state = bytearray(initial_state_value) * self.key_count

    @property
    def key_count(self):
        return self._key_count

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
            opin.value = self.pull is not digitalio.Pull.UP

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

                    if self.pull is digitalio.Pull.UP:
                        pressed = not new_val
                    else:
                        pressed = new_val
                    self.state[ba_idx] = new_val

                    any_changed = True
                    break

                ba_idx += 1

            opin.value = self.pull is digitalio.Pull.UP
            if any_changed:
                break

        if any_changed:
            key_number = self.len_cols * row + col + self.offset
            return KeyEvent(key_number, pressed)
