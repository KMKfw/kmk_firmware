import digitalio


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
        rotaries=None,
    ):
        self.len_cols = len(cols)
        self.len_rows = len(rows)

        # Rotary encoders are one column each and 2 rows.
        # When the encoder is incremented column n from the last column and row
        # 1 is pressed and when decremented row 2 - n is the index of the encoder.
        if rotaries:
            assert (
                self.len_rows > 2
            ), 'There are less than 2 rows but there are rotary encoders, which need 2 or more rows'

            self.len_cols += len(rotaries)

        # A pin cannot be both a row and column, detect this by combining the
        # two tuples into a set and validating that the length did not drop
        #
        # repr() hackery is because CircuitPython Pin objects are not hashable
        unique_pins = {repr(c) for c in cols} | {repr(r) for r in rows}
        assert (
            len(unique_pins) + len(rotaries) == self.len_cols + self.len_rows
        ), 'Cannot use a pin as both a column and row'
        del unique_pins

        self.diode_orientation = diode_orientation

        # __class__.__name__ is used instead of isinstance as the MCP230xx lib
        # does not use the digitalio.DigitalInOut, but rather a self defined one:
        # https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx/blob/3f04abbd65ba5fa938fcb04b99e92ae48a8c9406/adafruit_mcp230xx/digital_inout.py#L33

        if self.diode_orientation == DiodeOrientation.COLUMNS:
            self.outputs = [
                x
                if x.__class__.__name__ is 'DigitalInOut'
                else digitalio.DigitalInOut(x)
                for x in cols
            ]
            self.inputs = [
                x
                if x.__class__.__name__ is 'DigitalInOut'
                else digitalio.DigitalInOut(x)
                for x in rows
            ]
            self.translate_coords = True
        elif self.diode_orientation == DiodeOrientation.ROWS:
            self.outputs = [
                x
                if x.__class__.__name__ is 'DigitalInOut'
                else digitalio.DigitalInOut(x)
                for x in rows
            ]
            self.inputs = [
                x
                if x.__class__.__name__ is 'DigitalInOut'
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

        self.rotaries = [
            {'obj': x, 'lastpos': x.position, 'state': 0} for x in rotaries
        ]

        self.rollover_cols_every_rows = rollover_cols_every_rows
        if self.rollover_cols_every_rows is None:
            self.rollover_cols_every_rows = self.len_rows

        self.len_state_arrays = self.len_cols * self.len_rows
        self.state = bytearray(self.len_state_arrays)
        self.report = bytearray(3)

    def scan_for_changes(self):
        '''
        Poll the matrix for changes and return either None (if nothing updated)
        or a bytearray (reused in later runs so copy this if you need the raw
        array itself for some crazy reason) consisting of (row, col, pressed)
        which are (int, int, bool)
        '''
        for index, encoder in enumerate(self.rotaries):
            newpos = encoder['obj'].position

            if (
                (newpos == encoder['lastpos'] and encoder['state'] == 0)
                or (newpos > encoder['lastpos'] and encoder['state'] > 0)
                or (newpos < encoder['lastpos'] and encoder['state'] < 0)
            ):
                encoder['lastpos'] = newpos
                continue

            self.report[1] = self.len_cols - index - 1

            if newpos == encoder['lastpos']:
                self.report[0] = 0 if encoder['state'] > 0 else 1
                self.report[2] = False

                encoder['state'] = 0
            elif newpos > encoder['lastpos']:
                if encoder['state'] < 0:
                    self.report[0] = 1
                    self.report[2] = False
                    encoder['state'] = 0
                    return self.report

                self.report[0] = 0
                self.report[2] = True

                encoder['state'] = 1
            elif newpos < encoder['lastpos']:
                if encoder['state'] < 0:
                    self.report[0] = 1
                    self.report[2] = False
                    encoder['state'] = 0
                    return self.report

                self.report[0] = 1
                self.report[2] = True

                encoder['state'] = -1

            encoder['lastpos'] = newpos
            return self.report

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
                return self.report
