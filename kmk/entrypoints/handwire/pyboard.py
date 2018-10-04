import sys
from logging import DEBUG

import gc

from kmk.common.consts import UnicodeModes
from kmk.common.leader_mode import LeaderHelper
from kmk.firmware import Firmware
from kmk.micropython.pyb_hid import HIDHelper


def main():
    from kmk_keyboard_user import cols, diode_orientation, keymap, rows

    try:
        from kmk_keyboard_user import unicode_mode
    except Exception:
        unicode_mode = UnicodeModes.NOOP

    # This will run out of ram at this point unless you manually GC
    gc.collect()

    try:
        from kmk_keyboard_user import leader_mode_enter
    except Exception:
        leader_mode_enter = False

    try:
        firmware = Firmware(
            keymap=keymap,
            row_pins=rows,
            col_pins=cols,
            diode_orientation=diode_orientation,
            unicode_mode=unicode_mode,
            leader_mode_enter=leader_mode_enter,
            hid=HIDHelper,
            leader_helper=LeaderHelper,
            log_level=DEBUG,
        )

        firmware.go()
    except Exception as e:
        sys.print_exception(e)
        sys.exit(1)
