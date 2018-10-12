import sys

import gc

from kmk.firmware import Firmware
from kmk.matrix import MatrixScanner
from kmk.micropython.pyb_hid import HIDHelper


def main():
    import kmk_keyboard_user
    cols = getattr(kmk_keyboard_user, 'cols')
    diode_orientation = getattr(kmk_keyboard_user, 'diode_orientation')
    keymap = getattr(kmk_keyboard_user, 'keymap')
    rows = getattr(kmk_keyboard_user, 'rows')

    debug_enable = getattr(kmk_keyboard_user, 'debug_enable', False)

    if debug_enable:
        from logging import DEBUG as log_level
    else:
        from logging import ERROR as log_level

    # This will run out of ram at this point unless you manually GC
    gc.collect()

    try:
        firmware = Firmware(
            keymap=keymap,
            row_pins=rows,
            col_pins=cols,
            diode_orientation=diode_orientation,
            hid=HIDHelper,
            log_level=log_level,
            matrix_scanner=MatrixScanner,
        )
        # This will run out of ram at this point unless you manually GC
        gc.collect()

        firmware.go()
    except Exception as e:
        sys.print_exception(e)
        sys.exit(1)
