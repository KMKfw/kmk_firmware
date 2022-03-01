import digitalio

from kmk.matrix import KeyEvent
from kmk.scanners import Scanner


def range_rev(start, stop):
    return range(stop - 1, start - 1, -1)


def mapping_up_down(cols, rows):
    '''
    Maps keys according to the following diagram:

       1 2 3
     +------
    1| A A A
    2| A A A
     |
    1| B B B
    2| B B B
    '''

    coord_mapping = list(range(2 * cols * rows))
    return coord_mapping


def mapping_up_down_mirrored(cols, rows):
    '''
    Maps keys according to the following diagram:

       1 2 3
     +------
    1| A A A
    2| A A A
     |
    2| B B B
    1| B B B
    '''

    coord_mapping = []
    coord_mapping.extend(range(cols * rows))
    coord_mapping.extend(range_rev(cols * rows, 2 * cols * rows))
    return coord_mapping


def mapping_left_right(cols, rows):
    '''
    Maps keys according to the following diagram:

       1 2 3  1 2 3
     +-------------
    1| A A A  B B B
    2| A A A  B B B
    '''

    size = cols * rows
    coord_mapping = []
    for y in range(rows):
        yy = y * cols
        coord_mapping.extend(range(yy, yy + cols))
        coord_mapping.extend(range(yy + size, yy + cols + size))
    return coord_mapping


def mapping_left_right_mirrored(cols, rows):
    '''
    Maps keys according to the following diagram:

       1 2 3  3 2 1
     +-------------
    1| A A A  B B B
    2| A A A  B B B
    '''

    size = cols * rows
    coord_mapping = []
    for y in range(rows):
        yy = y * 2 * cols
        coord_mapping.extend(range(yy, yy + cols))
        coord_mapping.extend(range_rev(yy + size, yy + cols + size))
    return coord_mapping


def mapping_interleave_cols(cols, rows):
    '''
    Maps keys according to the following diagram:

       1 1 2 2 3 3
     +-------------
    1| A B A B A B
    2| A B A B A B
    '''

    coord_mapping = []
    mat = cols * rows
    for i in range(mat):
        coord_mapping.append(i)
        coord_mapping.append(i + mat)
    return coord_mapping


# these two are actually equivalent
mapping_interleave_rows = mapping_left_right


class BidirectionalScanner(Scanner):
    '''
    A Scanner for Keyboard Matrices with Diodes in both directions.

    In a bidirectional matrix, each (col, row) crossing can be used twice -
    once with a ROW2COL diode ("A"), and once with a COL2ROW diode ("B").

    The raw key numbers returned by this scanner are based on this layout ("up_down"):

        C1  C2  C3
      +-----------
    R1| A0  A1  A2
    R2| A3  A4  A5
      +-----------
    R1| B6  B7  B8
    R1| B9 B10 B11

    If the physical layout of the matrix is different, you can pass a function
    for `mapping`. The function is passed `len_cols` and `len_rows` and should
    return a `coord_mapping` list.
    Various common mappings are provided in this module, see:
    - `kmk.scanners.bidirectional.mapping_left_right`
    - `kmk.scanners.bidirectional.mapping_left_right_mirrored`
    - `kmk.scanners.bidirectional.mapping_up_down`
    - `kmk.scanners.bidirectional.mapping_up_down_mirrored`
    - `kmk.scanners.bidirectional.mapping_interleave_rows`
    - `kmk.scanners.bidirectional.mapping_interleave_cols`

    :param cols: A sequence of pins that are the columns for matrix A.
    :param rows: A sequence of pins that are the rows for matrix A.
    :param mapping: A coord_mapping generator function, see above.
    '''

    def __init__(self, cols, rows, mapping=mapping_up_down):
        self.len_cols = len(cols)
        self.len_rows = len(rows)
        self.half_size = self.len_cols * self.len_rows

        self.coord_mapping = mapping(self.len_cols, self.len_rows)

        # A pin cannot be both a row and column, detect this by combining the
        # two tuples into a set and validating that the length did not drop
        #
        # repr() hackery is because CircuitPython Pin objects are not hashable
        unique_pins = {repr(c) for c in cols} | {repr(r) for r in rows}
        assert (
            len(unique_pins) == self.len_cols + self.len_rows
        ), 'Cannot use a pin as both a column and row'
        del unique_pins

        # __class__.__name__ is used instead of isinstance as the MCP230xx lib
        # does not use the digitalio.DigitalInOut, but rather a self defined one:
        # https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx/blob/3f04abbd65ba5fa938fcb04b99e92ae48a8c9406/adafruit_mcp230xx/digital_inout.py#L33

        self.cols = [
            x if x.__class__.__name__ == 'DigitalInOut' else digitalio.DigitalInOut(x)
            for x in cols
        ]
        self.rows = [
            x if x.__class__.__name__ == 'DigitalInOut' else digitalio.DigitalInOut(x)
            for x in rows
        ]

        self.len_state_arrays = self.half_size * 2
        self.state = bytearray(self.len_state_arrays)

    def scan_for_changes(self):
        ba_idx = -1
        any_changed = False

        for (inputs, outputs, flip) in [
            (self.rows, self.cols, False),
            (self.cols, self.rows, True),
        ]:
            for pin in outputs:
                pin.switch_to_output()

            for pin in inputs:
                pin.switch_to_input(pull=digitalio.Pull.DOWN)

            for oidx, opin in enumerate(outputs):
                opin.value = True

                for iidx, ipin in enumerate(inputs):
                    if flip:
                        ba_idx = oidx * len(inputs) + iidx + self.half_size
                    else:
                        ba_idx = iidx * len(outputs) + oidx

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
                        self.state[ba_idx] = new_val
                        any_changed = True
                        break

                opin.value = False
                if any_changed:
                    break

            if any_changed:
                return KeyEvent(ba_idx, self.state[ba_idx])
