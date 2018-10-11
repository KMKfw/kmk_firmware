import sys

from kmk.circuitpython.hid import HIDHelper
from kmk.common.consts import UnicodeModes
from kmk.common.matrix import MatrixScanner
from kmk.firmware import Firmware


def main():
    import kmk_keyboard_user
    cols = getattr(kmk_keyboard_user, 'cols')
    diode_orientation = getattr(kmk_keyboard_user, 'diode_orientation')
    keymap = getattr(kmk_keyboard_user, 'keymap')
    rows = getattr(kmk_keyboard_user, 'rows')

    DEBUG_ENABLE = getattr(kmk_keyboard_user, 'DEBUG_ENABLE', False)

    if DEBUG_ENABLE:
        from logging import DEBUG as log_level
    else:
        from logging import ERROR as log_level

    try:
        from kmk_keyboard_user import unicode_mode
    except Exception:
        unicode_mode = UnicodeModes.NOOP

    try:
        firmware = Firmware(
            keymap=keymap,
            row_pins=rows,
            col_pins=cols,
            diode_orientation=diode_orientation,
            unicode_mode=unicode_mode,
            log_level=log_level,
            matrix_scanner=MatrixScanner,
            hid=HIDHelper,
        )

        firmware.go()
    except Exception as e:
        sys.print_exception(e)
        sys.exit(1)
