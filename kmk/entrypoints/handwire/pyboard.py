import sys

import gc

from kmk.common.leader_mode import LeaderHelper
from kmk.firmware import Firmware
from kmk.micropython.matrix import MatrixScanner
from kmk.micropython.pyb_hid import HIDHelper


def main():
    import kmk_keyboard_user
    cols = getattr(kmk_keyboard_user, 'cols')
    diode_orientation = getattr(kmk_keyboard_user, 'diode_orientation')
    keymap = getattr(kmk_keyboard_user, 'keymap')
    rows = getattr(kmk_keyboard_user, 'rows')

    DEBUG_ENABLE = getattr(kmk_keyboard_user, 'DEBUG_ENABLE', False)

    if DEBUG_ENABLE:
        from logging import DEBUG
    else:
        from logging import ERROR as DEBUG

    # This will run out of ram at this point unless you manually GC
    gc.collect()

    try:
        firmware = Firmware(
            keymap=keymap,
            row_pins=rows,
            col_pins=cols,
            diode_orientation=diode_orientation,
            hid=HIDHelper,
            leader_helper=LeaderHelper,
            log_level=DEBUG,
            matrix_scanner=MatrixScanner,
        )
        # This will run out of ram at this point unless you manually GC
        gc.collect()

        firmware.go()
    except Exception as e:
        sys.print_exception(e)
        sys.exit(1)
